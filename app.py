import os
import typing
import random
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import gradio as gr

from planqk.service.client import PlanqkServiceClient

consumer_key = os.getenv("CONSUMER_KEY", None)
consumer_secret = os.getenv("CONSUMER_SECRET", None)
service_endpoint = os.getenv(
    "SERVICE_ENDPOINT",
    "https://gateway.platform.planqk.de/anaqor/fleet-route-planning/1.0.0",
)

title = "Demo: Quantum Route Planning"
description = """
    This demo shows how to use the PlanQK Platform to solve a simple quantum route planning problem. The problem 
    is to find the shortest route between two points on a grid. The grid is represented by a graph, where each 
    node is a point on the grid and each edge is a connection between two points. The graph is given as an 
    adjacency matrix. The quantum algorithm is based on the Grover algorithm. The algorithm is implemented as a 
    service on the PlanQK Platform. The demo uses the service to solve the route planning problem.
    """


def create_graph(
    address_weights_array: list[list[typing.Any]], routes_list: list[typing.Dict]
):
    matplotlib.use("SVG")

    G = nx.empty_graph()

    for item in address_weights_array:
        G.add_edge(int(item[0]), int(item[1]), weight=float(item[2]))

    pos = nx.spring_layout(G, seed=42)

    # draw nodes
    nx.draw_networkx_nodes(
        G, pos, node_size=2000, node_color="white", edgecolors="black", linewidths=3
    )
    # draw node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    courier_routes = {}
    all_edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    for route in routes_list:
        route_edges = [eval(item) for item in route["naive_route_edges"]]
        courier_routes[route["cluster_id"]] = []
        for u, v in route_edges:
            if (u, v) in all_edges or (v, u) in all_edges:
                courier_routes[route["cluster_id"]].append((u, v))
                # remove (u, v) from all_edges
                all_edges.remove((u, v)) if (u, v) in all_edges else None
                all_edges.remove((v, u)) if (v, u) in all_edges else None

    # draw courier routes
    for route in courier_routes.values():
        # random color
        color = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        nx.draw_networkx_edges(
            G, pos, edgelist=route, width=6, style="dashed", edge_color=color
        )

    # draw remaining edges
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, width=3, alpha=0.5)

    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")

    return plt


def run_service(
    number_couriers: int, address_weights_array: list[list[typing.Any]], solver: str
):
    client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

    weight_dict = {}
    for item in address_weights_array:
        weight_dict[str((item[0], item[1]))] = item[2]

    data = {
        "weight_dict": weight_dict,
    }
    params = {
        "solver": "sim_anneal",
        "n_clusters": int(number_couriers),
        "num_sweeps_sa": 300,
        "num_reads_sa": 10000,
        "num_reads_qa": 1000,
        "annealing_time": 20,
    }
    print(f"data={data}", f"params={params}")

    job = client.start_execution(data=data, params=params)
    job_result = client.get_result(job.id)

    print(job_result)
    routes_list = job_result["result"]["routes_list"]

    result = ""
    for route in routes_list:
        nodes = eval(route["route_nodes"])
        result += f"{route['cluster_id']}: {nodes}"
        result += "\n"

    plt = create_graph(address_weights_array, routes_list)

    return result, plt


demo = gr.Interface(
    run_service,
    [
        gr.Number(value=2, label="Number of Couriers"),
        gr.Dataframe(
            label="Weights between Addresses",
            headers=["Address A", "Address B", "Weight"],
            value=[
                [0, 1, 0.11],
                [0, 2, 0.44],
                [0, 3, 0.27],
                [0, 4, 0.13],
                [1, 2, 0.62],
                [1, 3, 0.2],
                [2, 4, 0.41],
                [3, 4, 0.71],
            ],
            col_count=(3, "fixed"),
            type="array",
        ),
        gr.Dropdown(
            label="Solver",
            choices=["Simulated Annealer", "Hybrid Annealer", "Quantum Annealer"],
            value="Simulated Annealer",
        ),
    ],
    [
        gr.Textbox(label="Courier Routes"),
        gr.Plot(label="Courier Route Graph"),
    ],
    examples=[
        [
            2,
            [
                [0, 1, 0.55],
                [0, 2, 0.34],
                [0, 3, 0.56],
                [0, 4, 0.53],
                [1, 2, 0.62],
                [1, 3, 0.2],
                [2, 4, 0.41],
                [3, 4, 0.71],
            ],
            "Simulated Annealer",
        ],
        [
            2,
            [
                [0, 1, 0.11],
                [0, 2, 0.44],
                [0, 3, 0.27],
                [0, 4, 0.63],
                [1, 2, 0.62],
                [1, 3, 0.2],
                [2, 4, 0.41],
                [3, 4, 0.71],
            ],
            "Hybrid Annealer",
        ],
    ],
    title=title,
    description=description,
    allow_flagging="never",
)

demo.launch()
