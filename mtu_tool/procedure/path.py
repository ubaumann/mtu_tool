import logging
from typing import Dict, Tuple, List
from ipaddress import IPv4Interface

from nornir.core import Nornir
from nornir.core.task import Task, Result, AggregatedResult
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli

from mtu_tool.models.itms import ConnectionItem


def path(
    nr: Nornir,
    hostname: str,
    destination: IPv4Interface,
) -> Tuple[List[List[ConnectionItem]], AggregatedResult]:

    # TODO

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
