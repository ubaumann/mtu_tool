from typing import Optional
from dataclasses import dataclass


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
