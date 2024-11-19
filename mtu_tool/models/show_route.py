from typing import Dict, List, Optional
from ipaddress import IPv4Address, IPv4Network
from pydantic import BaseModel


class Via(BaseModel):
    nexthopAddr: Optional[IPv4Address] = None
    interface: str


class Route(BaseModel):
    hardwareProgrammed: bool
    routeType: str
    routeLeaked: bool
    kernelProgrammed: bool
    preference: Optional[int] = None
    metric: Optional[int] = None
    routeAction: str
    vias: List[Via]
    directlyConnected: bool


class Vrf(BaseModel):
    routingDisabled: bool
    allRoutesProgrammedHardware: bool
    allRoutesProgrammedKernel: bool
    defaultRouteState: str
    routes: Dict[IPv4Network, Route]


class Model(BaseModel):
    vrfs: Dict[str, Vrf]
