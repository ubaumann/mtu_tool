from typing import List, Tuple

from nornir.core import Nornir
from nornir.core.task import AggregatedResult
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get

from mtu_tool.exceptions import NoHostFoundException
from mtu_tool.models.itms import ConnectionItem


def neighbors(
    nr: Nornir,
    hostname: str,
) -> Tuple[List[ConnectionItem], AggregatedResult]:
    """Collect the mtu for all local and neighbor interfaces"""

    nr_host = nr.filter(name=hostname)
    if len(nr_host.inventory) == 0:
        raise NoHostFoundException(f"Host {hostname} not found in inventory")

    result_lldp = nr_host.run(
        task=napalm_get,
        getters=[
            "get_lldp_neighbors",
        ],
    )
    hosts = [hostname]
    get_lldp_neighbors = result_lldp[hostname][0].result.get("get_lldp_neighbors", {})
    for lldp_data in get_lldp_neighbors.values():
        for lldp_neighbor in lldp_data:
            n = lldp_neighbor["hostname"]
            if n not in hosts:
                hosts.append(n)

    result_interfaces = nr.filter(F(name__any=hosts)).run(
        task=napalm_get,
        getters=[
            "get_interfaces",
        ],
    )

    get_interfaces_local = result_interfaces[hostname][0].result.get(
        "get_interfaces", {}
    )

    connections = []
    for local_interface, lldp_data in get_lldp_neighbors.items():
        local_mtu = get_interfaces_local[local_interface]["mtu"]
        for lldp_neighbor in lldp_data:
            neighbor_name = lldp_neighbor["hostname"]
            neighbor_interface = lldp_neighbor["port"]
            neighbor_mtu = result_interfaces[neighbor_name][0].result.get(
                "get_interfaces", {}
            )[neighbor_interface]["mtu"]

            connections.append(
                ConnectionItem(
                    local_name=hostname,
                    local_interface=local_interface,
                    local_mtu=local_mtu,
                    neighbor_name=neighbor_name,
                    neighbor_interface=neighbor_interface,
                    neighbor_mtu=neighbor_mtu,
                )
            )

    return connections, result_interfaces


if __name__ == "__main__":
    from nornir_rich.functions import print_result
    from mtu_tool.helpers import init_nornir

    nr = init_nornir()

    connections, result = neighbors(nr, hostname="r06")
    print_result(result)
    for c in connections:
        print(
            f"{c.local_interface} {c.local_mtu} - {c.neighbor_name} {c.neighbor_interface} {c.neighbor_mtu}"
        )

    """
    mtu-tool-py3.10ins@ubuntu-L:~/mtu_tool$ python mtu_tool/procedure/neighbors.py
    Ethernet1 1500 - r04 Ethernet5 1500
    Ethernet2 1500 - r08 Ethernet1 1500
    Ethernet3 1500 - r09 Ethernet1 1500
    """
