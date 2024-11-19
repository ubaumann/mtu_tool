from typing import Dict, List, Optional

from rich.console import Console

from mtu_tool.models.itms import InterfaceItem


def print_interfaces(
    data: Dict["str", List[InterfaceItem]],
    min_mtu: Optional[int] = None,
    console: Console = Console(),
) -> None:
    
    # TODO
    # use console.print(...) to print
    pass


if __name__ == "__main__":
    demo_data = {
        "r01": [
            InterfaceItem("Ethernet1", 1500),
            InterfaceItem("Ethernet2", 1500),
            InterfaceItem("Ethernet3", 1480),
            InterfaceItem("Ethernet4", 1500),
        ],
        "r02": [
            InterfaceItem("Ethernet1", 1500),
            InterfaceItem("Ethernet2", 1500),
            InterfaceItem("Ethernet3", 1504),
            InterfaceItem("Ethernet4", 1500),
        ],
    }
    print_interfaces(demo_data, min_mtu=1500)
