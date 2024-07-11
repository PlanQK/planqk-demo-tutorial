import plotly.express as px
import pandas as pd

def create_map(routes, address_coordinates):

    data = {
        "courier": [],
        "address_name": [],
        "lat": [],
        "lng": [],
    }
    for i, route in enumerate(routes):
        for address in route:
            lat, lng = address_coordinates[address]["lat"], address_coordinates[address]["lng"]
            data["lat"].append(lat)
            data["lng"].append(lng)
            data["courier"].append(f"Courier {i+1}")
            data["address_name"].append(address)

    data_frame = pd.DataFrame(data)

    fig = px.line_mapbox(data_frame, lat="lat", lon="lng", color="courier", hover_name="address_name", zoom=3, height=300)

    ## center of prenzlauer berg
    prenzlauer_berg_lat = 52.5487
    prenzlauer_berg_lng = 13.4319
    fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=10, mapbox_center_lat = prenzlauer_berg_lat, mapbox_center_lon = prenzlauer_berg_lng)

    return fig