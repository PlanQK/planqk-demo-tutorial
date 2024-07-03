import random
import matplotlib
import matplotlib.pyplot as plt
import typing
import networkx as nx

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
