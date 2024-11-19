from typing import List, Optional

from rich.console import Console

from mtu_tool.models.itms import ConnectionItem


def print_neighbors(
    connections: List[ConnectionItem],
    min_mtu: Optional[int] = None,
    console: Console = Console(),
) -> None:
    
    # TODO
    # use console.print(...) to print
    pass


if __name__ == "__main__":
    demo_data = [
        ConnectionItem(
            local_interface="Ethernet1",
            local_mtu=1500,
            neighbor_name="r02",
            neighbor_interface="Ethernet2",
            neighbor_mtu=1500,
        ),
        ConnectionItem(
            local_interface="Ethernet2",
            local_mtu=1500,
            neighbor_name="r03",
            neighbor_interface="Ethernet1",
            neighbor_mtu=1500,
        ),
        ConnectionItem(
            local_interface="Ethernet3",
            local_mtu=1504,
            neighbor_name="r05",
            neighbor_interface="Ethernet4",
            neighbor_mtu=1500,
        ),
        ConnectionItem(
            local_interface="Ethernet4",
            local_mtu=1500,
            neighbor_name="r07",
            neighbor_interface="Ethernet3",
            neighbor_mtu=1480,
        ),
    ]
    print_neighbors(demo_data, min_mtu=1500)
