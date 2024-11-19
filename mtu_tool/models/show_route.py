from typing import Dict, List, Optional
from pydantic import BaseModel


class Via(BaseModel):
    nexthopAddr: Optional[str] = None
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
    routes: Dict[str, Route]


class Model(BaseModel):
    vrfs: Dict[str, Vrf]
