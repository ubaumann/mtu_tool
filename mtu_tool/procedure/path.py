import logging
from typing import Dict, Tuple, List
from ipaddress import IPv4Interface
from copy import copy

from nornir.core import Nornir
from nornir.core.task import Task, Result, AggregatedResult
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli

from mtu_tool.models.itms import ConnectionItem
from mtu_tool.models.show_route import Model as RouteModel

from mtu_tool.exceptions import PathProcedureError


# Use a cash to interact only once with a device/mock
CACHE: Dict[str, Result] = {}


def get_next_hop(task: Task, destination: IPv4Interface) -> Result:
    if cached := CACHE.get(task.host.name):
        return cached

    show_cmd = f"show ip route {destination} | json"
    result_cli = task.run(
        task=napalm_cli,
        commands=[show_cmd],
        severity_level=logging.DEBUG,
    )
    result_getters = task.run(
        task=napalm_get,
        getters=[
            "get_lldp_neighbors",
            "get_interfaces",
        ],
        severity_level=logging.DEBUG,
    )

    # The CLI command returns a JSON string, use Pydantic Model
    show_routes = RouteModel.model_validate_json(result_cli[0].result[show_cmd])

    # default VRF hardcoded for now
    routes = show_routes.vrfs["default"].routes
    if len(routes) == 0:
        raise Exception("No route found")

    # Collect "interface: mtu" mapping
    interface_mtus = {
        name: data["mtu"]
        for name, data in result_getters[0].result["get_interfaces"].items()
    }

    next_hopes = []
    if not routes[str(destination)].directlyConnected:
        for via in routes[str(destination)].vias:
            interface_data = result_getters[0].result["get_interfaces"][via.interface]
            lldp_data = result_getters[0].result["get_lldp_neighbors"][via.interface]
            # For now we just take the first lldp neighbor. Feel free to improve
            # If DNS PTR works for all p2p links, we could use it to get the next hop host
            next_hopes.append(
                ConnectionItem(
                    local_name=task.host.name,
                    local_interface=via.interface,
                    local_mtu=interface_data["mtu"],
                    neighbor_name=lldp_data[0]["hostname"],
                    neighbor_interface=lldp_data[0]["port"],
                    # The remote MTU needs to be updated in the recursion
                )
            )
    result_data = {
        "next_hops": next_hopes,
        "interface_mtus": interface_mtus,
    }
    result = Result(host=task.host, result=result_data)
    CACHE[task.host.name] = result
    return result


def path(
    nr: Nornir,
    hostname: str,
    destination: IPv4Interface,
) -> Tuple[List[List[ConnectionItem]], AggregatedResult]:

    nr_host = nr.filter(name=hostname)
    if len(nr_host.inventory) == 0:
        raise Exception("Host not found in inventory")  # ToDo

    path_result = AggregatedResult("path")

    path: List[ConnectionItem] = []  # first path list
    paths = [path]  # list of all existing paths

    def split_path(path):
        """
        Generator that first yields the original list and then yields copies of the list passed as an argument. Each copy is added to the 'paths' collection.

        Parameters:
        path (list): The original list to be yielded and copied.

        Yields:
        list: The original list.

        Yields:
        list: Copies of the original list.
        """
        path_copy = copy(path)
        yield path
        while True:
            new_path = copy(path_copy)
            paths.append(new_path)
            yield new_path

    def walk_path(
        hostname: str, interface: str, path, aggregated_result: AggregatedResult
    ) -> int:

        nr_host = nr.filter(name=hostname)

        result = nr_host.run(
            task=get_next_hop,
            destination=destination,
        )
        if hostname not in aggregated_result:
            # If hostname is already in aggregated_result we are working with a cashed result
            aggregated_result.update(result)

        next_hops: List[ConnectionItem] = result[hostname][0].result["next_hops"]
        interface_mtus = result[hostname][0].result["interface_mtus"]

        # generator copies the path and adds it to the paths list if multiple paths exist
        split_path_generator = split_path(path)
        for nh in next_hops:
            passed_path = next(split_path_generator)
            # Add next hop information to the list to have the right order and beeing able to copy the path
            passed_path.append(nh)
            remote_mtu = walk_path(
                nh.neighbor_name,
                nh.neighbor_interface,
                passed_path,
                aggregated_result,
            )
            # walk_path returns the MTU uf the remote and the next hop information added to the list can be updated now
            nh.neighbor_mtu = remote_mtu

        return int(interface_mtus[interface])

    # Start recursion
    try:
        walk_path(
            hostname=hostname,
            interface="Loopback0",
            path=path,
            aggregated_result=path_result,
        )
    except TypeError as exc:
        raise PathProcedureError(
            "Most likely a job failed and did return an exception and not a dict",
            path_result,
        ) from exc
    return paths, path_result


if __name__ == "__main__":
    from nornir_rich.functions import print_result
    from mtu_tool.helpers import init_nornir

    nr = init_nornir()

    paths, result = path(nr, "r01", "10.0.0.10/32")
    print_result(
        result,
        # severity_level=logging.DEBUG,
    )

    for i, p in enumerate(paths):
        print(f"{'=' * 16} Path {i} {'=' * 16}")
        for step in p:
            print(
                f"{step.local_name} {step.local_interface} {step.local_mtu} -> {step.neighbor_mtu} {step.neighbor_interface} {step.neighbor_name}"
            )

    """
    mtu-tool-py3.10ins@ubuntu-L:~/mtu_tool$ python mtu_tool/procedure/path.py
    ================ Path 0 ================
    r01 Ethernet1 1500 -> 1500 Ethernet1 r02
    r02 Ethernet4 1500 -> 1500 Ethernet1 r04
    r04 Ethernet5 1500 -> 1500 Ethernet1 r06
    r06 Ethernet2 1500 -> 1500 Ethernet1 r08
    r08 Ethernet4 1500 -> 1500 Ethernet1 r10
    ================ Path 1 ================
    r01 Ethernet1 1500 -> 1500 Ethernet1 r02
    r02 Ethernet4 1500 -> 1500 Ethernet1 r04
    r04 Ethernet5 1500 -> 1500 Ethernet1 r06
    r06 Ethernet3 1500 -> 1500 Ethernet1 r09
    r09 Ethernet4 1500 -> 1500 Ethernet2 r10
    ================ Path 2 ================
    r01 Ethernet1 1500 -> 1500 Ethernet1 r02
    r02 Ethernet5 1500 -> 1500 Ethernet2 r04
    r04 Ethernet5 1500 -> 1500 Ethernet1 r06
    r06 Ethernet2 1500 -> 1500 Ethernet1 r08
    r08 Ethernet4 1500 -> 1500 Ethernet1 r10
    ================ Path 3 ================
    r01 Ethernet1 1500 -> 1500 Ethernet1 r02
    r02 Ethernet5 1500 -> 1500 Ethernet2 r04
    r04 Ethernet5 1500 -> 1500 Ethernet1 r06
    r06 Ethernet3 1500 -> 1500 Ethernet1 r09
    r09 Ethernet4 1500 -> 1500 Ethernet2 r10
    ================ Path 4 ================
    r01 Ethernet2 1500 -> 1500 Ethernet1 r03
    r03 Ethernet4 1500 -> 1500 Ethernet1 r05
    r05 Ethernet5 1500 -> 1500 Ethernet1 r07
    r07 Ethernet3 1500 -> 1500 Ethernet2 r09
    r09 Ethernet4 1500 -> 1500 Ethernet2 r10
    ================ Path 5 ================
    r01 Ethernet2 1500 -> 1500 Ethernet1 r03
    r03 Ethernet5 1500 -> 1500 Ethernet2 r05
    r05 Ethernet5 1500 -> 1500 Ethernet1 r07
    r07 Ethernet3 1500 -> 1500 Ethernet2 r09
    r09 Ethernet4 1500 -> 1500 Ethernet2 r10
    """
