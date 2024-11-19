from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from mtu_tool.models.itms import ConnectionItem


def print_neighbors(
    connections: List[ConnectionItem],
    min_mtu: Optional[int] = None,
    console: Console = Console(),
) -> None:
    site_table = Table(show_lines=True)
    site_table.add_column("local", vertical="bottom")
    site_table.add_column("remote")
    site_table.add_column("status", vertical="middle")

    for item in connections:
        local_table = Table(show_header=False)
        local_table.add_column("Interface", min_width=25)
        local_table.add_column("MTU")
        if min_mtu and item.local_mtu < min_mtu:
            local_table.style = "red"

        remote_table = Table(show_header=False, title=item.neighbor_name)
        remote_table.add_column("Interface", min_width=25)
        remote_table.add_column("MTU")
        if min_mtu and item.neighbor_mtu < min_mtu:  # type: ignore
            remote_table.style = "red"

        local_table.add_row(item.local_interface, str(item.local_mtu))
        remote_table.add_row(item.neighbor_interface, str(item.neighbor_mtu))

        status_str = (
            ":white_heavy_check_mark:"
            if item.local_mtu == item.neighbor_mtu
            else ":cross_mark:"
        )
        site_table.add_row(local_table, remote_table, status_str)

    console.print(site_table)


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
