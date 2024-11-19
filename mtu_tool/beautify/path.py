from typing import List, Optional

from rich.console import Console

from mtu_tool.models.itms import ConnectionItem


def print_path(
    paths: List[List[ConnectionItem]],
    start_name: str,
    min_mtu: Optional[int] = None,
    console: Console = Console(),
) -> None:

    # TODO
    # use console.print(...) to print
    pass


if __name__ == "__main__":
    demo_paths = [
        [
            ConnectionItem(
                local_name="r01",
                local_interface="Ethernet1",
                local_mtu=1500,
                neighbor_name="r02",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r02",
                local_interface="Ethernet4",
                local_mtu=1500,
                neighbor_name="r04",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r04",
                local_interface="Ethernet5",
                local_mtu=1500,
                neighbor_name="r06",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r06",
                local_interface="Ethernet2",
                local_mtu=1480,
                neighbor_name="r08",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r08",
                local_interface="Ethernet4",
                local_mtu=1500,
                neighbor_name="r10",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
        ],
        [
            ConnectionItem(
                local_name="r01",
                local_interface="Ethernet1",
                local_mtu=1500,
                neighbor_name="r02",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r02",
                local_interface="Ethernet4",
                local_mtu=1500,
                neighbor_name="r04",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r04",
                local_interface="Ethernet5",
                local_mtu=1500,
                neighbor_name="r06",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r06",
                local_interface="Ethernet3",
                local_mtu=1500,
                neighbor_name="r09",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r09",
                local_interface="Ethernet4",
                local_mtu=1500,
                neighbor_name="r10",
                neighbor_interface="Ethernet2",
                neighbor_mtu=1500,
            ),
        ],
        [
            ConnectionItem(
                local_name="r01",
                local_interface="Ethernet1",
                local_mtu=1500,
                neighbor_name="r03",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r03",
                local_interface="Ethernet4",
                local_mtu=1500,
                neighbor_name="r05",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1480,
            ),
            ConnectionItem(
                local_name="r05",
                local_interface="Ethernet5",
                local_mtu=1500,
                neighbor_name="r07",
                neighbor_interface="Ethernet1",
                neighbor_mtu=1500,
            ),
            ConnectionItem(
                local_name="r07",
                local_interface="Ethernet3",
                local_mtu=1480,
                neighbor_name="r09",
                neighbor_interface="Ethernet2",
                neighbor_mtu=1480,
            ),
            ConnectionItem(
                local_name="r09",
                local_interface="Ethernet4",
                local_mtu=1500,
                neighbor_name="r10",
                neighbor_interface="Ethernet2",
                neighbor_mtu=1500,
            ),
        ],
    ]
    print_path(demo_paths, "r01", min_mtu=1500)
