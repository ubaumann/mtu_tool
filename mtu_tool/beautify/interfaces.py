from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from mtu_tool.models.itms import InterfaceItem


def _mtu_rich_str(mtu: int, min_mtu: Optional[int] = None) -> str:
    if not min_mtu:
        return str(mtu)
    return str(mtu) if mtu >= min_mtu else f"[red]{mtu}[/red]"


def print_interfaces(
    data: Dict["str", List[InterfaceItem]],
    min_mtu: Optional[int] = None,
    console: Console = Console(),
) -> None:
    for host, interface_list in data.items():
        table = Table(style="cyan", row_styles=["green"], expand=True)
        table.add_column("Interface Name")
        table.add_column("MTU", justify="right")

        for item in interface_list:
            table.add_row(item.name, _mtu_rich_str(mtu=item.mtu, min_mtu=min_mtu))

        title_colour = (
            "red"
            if min_mtu and min([x.mtu for x in interface_list]) < min_mtu
            else "green"
        )
        console.print(
            Panel(table, title=f"[{title_colour}]Device [b]{host}[/b]", style="magenta")
        )


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
