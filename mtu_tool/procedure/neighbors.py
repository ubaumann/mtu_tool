from typing import List, Tuple

from nornir.core import Nornir
from nornir.core.task import AggregatedResult
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get

from mtu_tool.models.itms import ConnectionItem


def neighbors(
    nr: Nornir,
    hostname: str,
) -> Tuple[List[ConnectionItem], AggregatedResult]:
    """Collect the mtu for all local and neighbor interfaces"""

    # TODO

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
