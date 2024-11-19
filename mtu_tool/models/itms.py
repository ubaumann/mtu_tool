from typing import Optional
from dataclasses import dataclass

from rich.columns import Columns
from rich.panel import Panel
from rich.json import JSON


@dataclass
class InterfaceItem:
    name: str
    mtu: int


@dataclass
class ConnectionItem:
    local_interface: str
    local_mtu: int
    neighbor_name: str
    neighbor_interface: str
    local_name: Optional[str] = None
    neighbor_mtu: Optional[int] = None

    def __rich__(self) -> Panel:
        colour = "red" if self.local_mtu != self.neighbor_mtu else "green"
        text = Columns(
            [
                Panel(
                    JSON.from_data(
                        {
                            "name": self.local_name,
                            "interface": self.local_interface,
                            "mtu": self.local_mtu,
                        }
                    ),
                    title=f"[{colour}]{self.local_name}",
                    style=colour,
                ),
                Panel(
                    JSON.from_data(
                        {
                            "name": self.neighbor_name,
                            "interface": self.neighbor_interface,
                            "mtu": self.neighbor_mtu,
                        }
                    ),
                    title=f"[{colour}]{self.neighbor_name}",
                    style=colour,
                ),
            ]
        )
        return Panel(text, title=f"{self.local_name} <> {self.neighbor_name}", width=80)
