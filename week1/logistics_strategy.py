"""
logistics_strategy_execution.py
Week 1: Logistics Strategy Execution Pipeline
"""

from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import numpy as np
import pandas as pd
from scipy.stats import norm


# 1. DATA PREPROCESSING
def process_logistics_telematics(df):
    df = df.copy()
    df["order_timestamp"] = pd.to_datetime(df["order_timestamp"])
    df["dispatch_timestamp"] = pd.to_datetime(df["dispatch_timestamp"])

    # Calculate actual lead time in hours
    df["actual_lead_time_hrs"] = (
        df["dispatch_timestamp"] - df["order_timestamp"]
    ).dt.total_seconds() / 3600.0

    # Keep valid coordinates and positive lead times
    valid_coords = (
        df["dest_latitude"].between(18.0, 22.0)
        & df["dest_longitude"].between(72.0, 76.0)
        & (df["actual_lead_time_hrs"] > 0)
    )
    clean_df = df[valid_coords].copy()

    # Fill missing payload using category median
    clean_df["payload_kg"] = (
        clean_df.groupby("product_category")["payload_kg"]
        .transform(lambda x: x.fillna(x.median()))
    )

    # Create time-based features
    clean_df["dispatch_hour"] = clean_df["dispatch_timestamp"].dt.hour
    clean_df["dispatch_dayofweek"] = clean_df["dispatch_timestamp"].dt.dayofweek
    clean_df["is_weekend"] = (
        clean_df["dispatch_dayofweek"].isin([5, 6]).astype(int)
    )

    return clean_df


# 2. DYNAMIC SAFETY STOCK
def calculate_dynamic_safety_stock(
    demand_mean, demand_std, lead_time_days,
    lead_time_std, service_level=0.95
):
    z_score = norm.ppf(service_level)

    demand_variance = lead_time_days * (demand_std ** 2)
    lead_time_variance = (demand_mean ** 2) * (lead_time_std ** 2)

    total_sigma = np.sqrt(
        demand_variance + lead_time_variance
    )

    safety_stock = z_score * total_sigma
    reorder_point = (demand_mean * lead_time_days) + safety_stock

    return {
        "service_level": service_level,
        "safety_stock_units": round(float(safety_stock), 2),
        "reorder_point_units": round(float(reorder_point), 2),
    }


# 3. CAPACITATED VEHICLE ROUTING
def solve_capacitated_vrp(
    distance_matrix, demands, vehicle_capacities, depot_index=0
):
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        len(vehicle_capacities),
        depot_index
    )
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    distance_callback_index = routing.RegisterTransitCallback(
        distance_callback
    )
    routing.SetArcCostEvaluatorOfAllVehicles(
        distance_callback_index
    )

    # Demand callback
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback
    )

    # Vehicle capacity constraint
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        vehicle_capacities,
        True,
        "Capacity"
    )

    # Search strategy
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)
    return manager, routing, solution


# 4. MAIN EXECUTION
if __name__ == "__main__":

    print("=" * 65)
    print("OUTPUT 1: Data Cleaning & Feature Engineering")
    print("=" * 65)

    sample_raw_data = pd.DataFrame({
        "order_id": [
            "ORD-101", "ORD-102", "ORD-103", "ORD-104", "ORD-105"
        ],
        "product_category": [
            "Electronics", "Apparel", "Electronics",
            "Automotive", "Apparel"
        ],
        "order_timestamp": [
            "2026-02-10 08:00:00",
            "2026-02-10 09:30:00",
            "2026-02-10 10:15:00",
            "2026-02-14 11:00:00",
            "2026-02-15 14:00:00"
        ],
        "dispatch_timestamp": [
            "2026-02-10 12:30:00",
            "2026-02-10 15:45:00",
            "2026-02-10 13:00:00",
            "2026-02-14 17:30:00",
            "2026-02-15 18:00:00"
        ],
        "dest_latitude": [19.0760, 18.5204, 0.0000, 21.1458, 19.9975],
        "dest_longitude": [72.8777, 73.8567, 0.0000, 72.8028, 73.7898],
        "payload_kg": [15.2, np.nan, 8.4, 45.0, 6.2],
    })

    cleaned_result = process_logistics_telematics(sample_raw_data)

    print(f"Raw Input Rows: {len(sample_raw_data)}")
    print(f"Cleaned Rows: {len(cleaned_result)}")
    print(cleaned_result[
        [
            "order_id", "product_category",
            "actual_lead_time_hrs", "payload_kg",
            "dispatch_hour", "is_weekend"
        ]
    ])

    print("\n" + "=" * 65)
    print("OUTPUT 2: Dynamic Safety Stock & Reorder Point")
    print("=" * 65)

    stock_analysis = calculate_dynamic_safety_stock(
        demand_mean=140.0,
        demand_std=22.5,
        lead_time_days=4.5,
        lead_time_std=1.2,
        service_level=0.95,
    )

    for key, value in stock_analysis.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 65)
    print("OUTPUT 3: Capacitated Vehicle Routing")
    print("=" * 65)

    distance_matrix = [
        [0, 14, 25, 18, 30],
        [14, 0, 16, 22, 28],
        [25, 16, 0, 15, 12],
        [18, 22, 15, 0, 19],
        [30, 28, 12, 19, 0],
    ]

    node_demands = [0, 6, 7, 5, 8]
    capacities = [15, 15]

    manager, routing, solution = solve_capacitated_vrp(
        distance_matrix,
        node_demands,
        capacities,
        depot_index=0
    )

    if solution:
        for vehicle_id in range(len(capacities)):
            index = routing.Start(vehicle_id)
            route = []
            route_load = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route_load += node_demands[node]
                route.append(
                    f"Node {node} (Load: {node_demands[node]})"
                )
                index = solution.Value(routing.NextVar(index))

            route.append(f"Node {manager.IndexToNode(index)}")

            print(
                f"Vehicle {vehicle_id + 1} Route: "
                f"{' -> '.join(route)}"
            )
            print(
                f"Total Carried Payload: "
                f"{route_load} / {capacities[vehicle_id]} units\n"
            )
