from typing import Dict, List, Optional, Tuple

from nornir.core import Nornir
from nornir.core.task import AggregatedResult
from nornir_napalm.plugins.tasks import napalm_get

from mtu_tool.exceptions import NoHostFoundException
from mtu_tool.models.itms import InterfaceItem


def interfaces(
    nr: Nornir,
    hostname: Optional[str] = None,
) -> Tuple[Dict["str", List[InterfaceItem]], AggregatedResult]:
    """Collect the mtu for all interfaces"""

    if hostname:
        nr = nr.filter(name=hostname)
        if len(nr.inventory) == 0:
            raise NoHostFoundException(f"Host {hostname} not found in inventory")

    result = nr.run(
        task=napalm_get,
        getters=[
            "get_interfaces",
        ],
    )

    data = {}
    for host, mulit_result in result.items():
        data_interface = []
        interfaces = mulit_result[0].result.get("get_interfaces", {})
        for int_name, int_data in interfaces.items():
            data_interface.append(InterfaceItem(name=int_name, mtu=int_data.get("mtu")))
        data[host] = data_interface

    return data, result


if __name__ == "__main__":
    from nornir_rich.functions import print_result
    from mtu_tool.helpers import init_nornir

    nr = init_nornir()

    data, result = interfaces(nr)
    print_result(result)
    for host, int_data in data.items():
        for d in int_data:
            print(f"{host}: {d.name:<15} {d.mtu}")

    """
    mtu-tool-py3.10ins@ubuntu-L:~/mtu_tool$ python mtu_tool/procedure/interfaces.py
    r01: Ethernet2       1500
    r01: Ethernet1       1500
    r01: Management0     1500
    r01: Loopback0       65535
    r02: Ethernet2       1500
    r02: Ethernet4       1500
    r02: Ethernet1       1500
    r02: Ethernet3       1500
    r02: Ethernet5       1500
    r02: Management0     1500
    r02: Loopback0       65535
    r03: Ethernet2       1500
    r03: Ethernet4       1500
    r03: Ethernet1       1500
    r03: Ethernet3       1500
    r03: Ethernet5       1500
    r03: Management0     1500
    r03: Loopback0       65535
    r04: Ethernet2       1500
    r04: Ethernet4       1500
    r04: Ethernet1       1500
    r04: Ethernet3       1504
    r04: Ethernet5       1500
    r04: Management0     1500
    r04: Loopback0       65535
    r05: Ethernet2       1500
    r05: Ethernet4       1500
    r05: Ethernet1       1500
    r05: Ethernet3       1500
    r05: Ethernet5       1500
    r05: Management0     1500
    r05: Loopback0       65535
    r06: Ethernet2       1500
    r06: Ethernet1       1500
    r06: Ethernet3       1500
    r06: Management0     1500
    r06: Loopback0       65535
    r07: Ethernet2       1480
    r07: Ethernet1       1500
    r07: Ethernet3       1500
    r07: Management0     1500
    r07: Loopback0       65535
    r08: Ethernet2       1500
    r08: Ethernet4       1500
    r08: Ethernet1       1500
    r08: Ethernet3       1500
    r08: Management0     1500
    r08: Loopback0       65535
    r09: Ethernet2       1500
    r09: Ethernet4       1500
    r09: Ethernet1       1500
    r09: Ethernet3       1500
    r09: Management0     1500
    r09: Loopback0       65535
    r10: Ethernet2       1500
    r10: Ethernet1       1500
    r10: Management0     1500
    r10: Loopback0       65535
    """
