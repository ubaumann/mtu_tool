import sys
from ipaddress import IPv4Interface, NetmaskValueError

import typer
from rich.console import Console
from nornir_rich.functions import print_result

from mtu_tool.helpers import init_nornir
from mtu_tool.exceptions import NoHostFoundException, PathProcedureError
from mtu_tool.procedure.interfaces import interfaces as interfaces_procedure
from mtu_tool.procedure.neighbors import neighbors as neighbors_procedure
from mtu_tool.procedure.path import path as path_procedure
from mtu_tool.beautify.interfaces import print_interfaces
from mtu_tool.beautify.neighbors import print_neighbors
from mtu_tool.beautify.path import print_path


# https://ascii.today/ to create ASCII art
HELP_TEXT = """
Simple [bright_green]MTU[/] CLI tool  :hammer:

[bright_cyan]
 _   .-')     .-') _               
( '.( OO )_  (  OO) )              
 ,--.   ,--.)/     '._ ,--. ,--.   
 |   `.'   | |'--...__)|  | |  |   
 |         | '--.  .--'|  | | .-') 
 |  |'.'|  |    |  |   |  |_|( OO )
 |  |   |  |    |  |   |  | | `-' /
 |  |   |  |    |  |  ('  '-'(_.-' 
 `--'   `--'    `--'    `-----'
"""

app = typer.Typer(help=HELP_TEXT, rich_markup_mode="rich")
console = Console()
console_error = Console(stderr=True, style="red")


@app.callback()
def setup_nornir(
    ctx: typer.Context,
    configuration_file: typer.FileText = typer.Option(
        "config.yaml",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        metavar="NORNIR_SETTINGS",
        help="Path to the nornir configuration file.",
        envvar="NORNIR_SETTINGS",
    ),
) -> None:
    """
    Get nornir object from configuration file
    """
    ctx.obj = init_nornir(str(configuration_file))


@app.command()
def interfaces(
    ctx: typer.Context,
    hostname: str = typer.Option(None, help="Choose a device by its hostname."),
    min_mtu: int = typer.Option(
        None,
        help="Highlight in [red]red[/] all MTU values smaller than the specified minimum.",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Display detailed output showing Nornir results."
    ),
) -> None:
    """Show MTU values for all interfaces."""
    nr = ctx.obj

    try:
        data, result = interfaces_procedure(nr, hostname)
    except NoHostFoundException as exc:
        console_error.print(exc)
        raise sys.exit(1)

    if verbose:
        print_result(result)

    print_interfaces(data, min_mtu, console=console)


@app.command()
def neighbors(
    ctx: typer.Context,
    hostname: str,
    min_mtu: int = typer.Option(
        None,
        help="Highlight in [red]red[/] all MTU values smaller than the specified minimum.",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Display detailed output showing Nornir results."
    ),
) -> None:
    """Display the MTU values for all interfaces along with their corresponding neighbors."""
    nr = ctx.obj

    try:
        connections, result = neighbors_procedure(nr, hostname)
    except NoHostFoundException as exc:
        console_error.print(exc)
        raise sys.exit(1)

    if verbose:
        print_result(result)

    print_neighbors(connections, min_mtu, console=console)


@app.command()
def path(
    ctx: typer.Context,
    hostname: str = typer.Argument(
        ...,
        help="Please provide the hostname of the starting device from which you would like to retrieve the MTU path.",
    ),
    destination: str = typer.Argument(
        ..., help="Provide the destination IPv4 Address. E.g.: 10.0.0.10/32"
    ),
    min_mtu: int = typer.Option(
        None,
        help="Highlight in [red]red[/] all MTU values smaller than the specified minimum.",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Multiple verbose levels can be enabled to increase the verbosity of the output when running Nornir by utilizing the corresponding option.",
        show_default=False,
    ),
) -> None:
    """Recursively print the MTU of all interfaces for all paths from the specified device to the specified destination."""
    nr = ctx.obj

    try:
        paths, result = path_procedure(nr, hostname, IPv4Interface(destination))
    except PathProcedureError as exc:
        print_result(exc.aggregated_result)
        raise sys.exit(1) from exc
    except NetmaskValueError as exc:
        console_error.print(
            f"Provided destination {destination} is not a valid IPv4Interface. Error message: {exc}"
        )
        raise sys.exit(1)
    if verbose:
        level = 10 * (4 - max(0, min(verbose + 1, 4)))
        print_result(result, severity_level=level)

    print_path(paths, hostname, min_mtu, console=console)


if __name__ == "__main__":
    app()
