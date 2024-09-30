import gradio as gr

import google_maps_service
import map_creator
import route_planning_service

title = "PlanQK Tutorial - Fleet Route Planning"
description = """
    This demo implements a simple app to plan delivery routes for a given number of couriers in the Berlin district of Pankow. 
    The routes are optimized to minimize the total distance traveled by the couriers while ensuring that each delivery address is visited exactly once.
    You can adjust the number of couriers and the delivery addresses to see how the routes change.
    
    > The route planning service created by the PlanQK tutorial is used in this demo.
    > Follow the tutorial to learn how to implement and create the respective service. 
    > It also shows how you subscribe to the created service and how to use it in this demo.
    
    When you press the submit button, the demo converts the number of couriers and the selected delivery addresses into the respective input required by the service.
    Consult the API documentation of the route planning service to understand the input and output of the service.
    Once the service calculated the routes, the demo displays the routes on a map and lists the routes for each courier in a text box.  
    """


def run_service(number_couriers: int, delivery_addresses: list[str]):
    address_distances, address_coordinates = google_maps_service.get_address_distances_and_coordinates(delivery_addresses)
    routes = route_planning_service.plan_routes(number_couriers, address_distances, delivery_addresses)
    map = map_creator.create_map(routes, address_coordinates)

    result_for_textbox = format_result_for_textbox_output(routes)

    return map, result_for_textbox


def init_empty_map():
    return map_creator.create_map([], {})


def format_result_for_textbox_output(routes):
    result = ""
    for i, route in enumerate(routes):
        result += f"Courier {i + 1}: {route}\n"
    return result


address_choices = [
    "Schliemannstraße 34, 10437 Berlin",
    "Kastanienallee 82, 10435 Berlin",
    "Helmholtzplatz 1, 10437 Berlin",
    "Danziger Straße 136, 10407 Berlin",
    "Kollwitzstraße 1, 10405 Berlin",
    "Schönhauser Allee 6-7, 10119 Berlin",
    "Knaackstraße 97, 10435 Berlin",
    "Sredzkistraße 44, 10435 Berlin",
    "Stargarder Straße 73, 10437 Berlin",
    "Oderberger Straße 56, 10435 Berlin",
    "Kopenhagener Straße 71, 10437 Berlin",
    "Pappelallee 29, 10437 Berlin",
    "Winsstraße 65, 10405 Berlin",
    "Dunckerstraße 14, 10437 Berlin",
    "Senefelderstraße 22, 10437 Berlin",
    "Husemannstraße 32, 10435 Berlin",
    "Belforter Straße 21, 10405 Berlin",
    "Greifenhagener Straße 65, 10437 Berlin",
    "Greifswalder Straße 212, 10405 Berlin",
    "Bornholmer Straße 72, 10439 Berlin"
]

default_selected_addresses = [
    "Schliemannstraße 34, 10437 Berlin",
    "Kastanienallee 82, 10435 Berlin",
    "Helmholtzplatz 1, 10437 Berlin",
    "Danziger Straße 136, 10407 Berlin",
    "Kollwitzstraße 1, 10405 Berlin",
    "Schönhauser Allee 6-7, 10119 Berlin",
    "Knaackstraße 97, 10435 Berlin",
    "Sredzkistraße 44, 10435 Berlin",
]

demo = gr.Interface(
    run_service,
    [
        gr.Number(value=2, label="Number of Couriers"),
        gr.CheckboxGroup(choices=address_choices, value=default_selected_addresses, label="Select Delivery Addresses:"),
    ],
    [
        gr.Plot(label="Courier Routes on Map"),
        gr.Textbox(label="Courier Routes"),
    ],
    title=title,
    description=description,
    allow_flagging="never",
)

demo.launch()
