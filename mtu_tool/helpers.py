from typing import Optional

from nornir import InitNornir
from nornir.core import Nornir


def init_nornir(configuration_file: str = "config.yaml", password: Optional[str] = None) -> Nornir:
    """
    Helper function to init the nornir object.
    We could do stuff like setting the default password here
    """
    nr = InitNornir(config_file=configuration_file)
    if password:
        nr.inventory.defaults.password = password
    return nr
