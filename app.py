import gradio as gr
import google_maps_service
import route_planning_service
import map_creator

title = "Demo: Quantum Route Planning"
description = """
    This interactive demo uses the [Fleet Route Planning Service](https://platform.planqk.de/marketplace/apis/8c63c4ed-97cb-4496-a27d-cfc7330fd66c),to plan routes for several couriers in the Berlin district of Pankow. 
    The routes are optimized to minimize the total distance traveled by the couriers while ensuring that each delivery address is visited exactly once.
    You can adjust the number of couriers and the delivery addresses to see how the routes change.
    """

def run_service(number_couriers: int, delivery_addresses: list[str]):
    delivery_addresses_flattened = [item for sublist in delivery_addresses for item in sublist]

    address_distances, address_coordinates = google_maps_service.get_address_distances_and_coordinates(delivery_addresses_flattened)
    routes = route_planning_service.plan_routes(number_couriers, address_distances, delivery_addresses_flattened)
    map = map_creator.create_map(routes, address_coordinates)

    result_for_textbox = format_result_for_textbox_output(routes)

    return result_for_textbox, map


def format_result_for_textbox_output(routes):
    result = ""
    for i, route in enumerate(routes):
        result += f"Courier {i + 1}: {route}\n"
    return result


demo = gr.Interface(
    run_service,
    [
        gr.Number(value=2, label="Number of Couriers"),
        gr.Dataframe(
            label="Delivery Addresses",
            headers=["Address"],
            value=[
                ["Alexanderplatz, Berlin, Germany"],
                ["Brandenburg Gate, Berlin, Germany"],
                ["Fernsehturm Berlin, Germany"],
                ["Potsdamer Platz, Berlin, Germany"],
                ["Reichstag building, Berlin, Germany"],
                ["Berlin Wall Memorial, Germany"],
                ["Checkpoint Charlie, Berlin, Germany"],
                ["Kurfürstendamm, Berlin, Germany"],
                ["Berlin Cathedral, Germany"],
                ["Charlottenburg Palace, Berlin, Germany"]
            ],
            col_count=(1, "fixed"),
            type="array",
        ),
    ],
    [
        gr.Textbox(label="Courier Routes"),
        gr.Plot(label="Courier Routes on Map")
    ],
    examples=[
        [
            2,
            [
                ["Alexanderplatz, Berlin, Germany"],
                ["Brandenburg Gate, Berlin, Germany"],
                ["Fernsehturm Berlin, Germany"],
                ["Potsdamer Platz, Berlin, Germany"],
                ["Reichstag building, Berlin, Germany"],
                ["Berlin Wall Memorial, Germany"],
                ["Checkpoint Charlie, Berlin, Germany"],
                ["Kurfürstendamm, Berlin, Germany"],
                ["Berlin Cathedral, Germany"],
                ["Charlottenburg Palace, Berlin, Germany"]
            ],
        ],
    ],
    title=title,
    description=description,
    allow_flagging="never",
)

demo.launch()
