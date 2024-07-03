import os
import typing
from planqk.service.client import PlanqkServiceClient

consumer_key = os.getenv("CONSUMER_KEY", None)
consumer_secret = os.getenv("CONSUMER_SECRET", None)
service_endpoint = os.getenv(
    "SERVICE_ENDPOINT",
    "https://gateway.platform.planqk.de/anaqor/fleet-route-planning/1.0.0",
)

def plan_routes(
        number_couriers: int, address_distances: dict, addresses: list
):
    client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

    ## assign each address a number idenfier starting from 0
    address_id = {}
    for i, address in enumerate(addresses):
        address_id[address] = i

    ## in address weights array, replace the address with the corresponding number identifier
    weight_dict = {}
    for address_pair, weight in address_distances.items():
        address1 = address_pair[0]
        address2 = address_pair[1]
        key_as_str = f"({address_id[address1]}, {address_id[address2]})"
        weight_dict[key_as_str] = weight

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

    job = client.start_execution(data=data, params=params)
    job_result = client.get_result(job.id)

    return job_result["result"]["routes_list"]



