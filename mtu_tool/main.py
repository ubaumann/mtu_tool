import typer
from rich.console import Console
from nornir_rich.functions import print_result

from mtu_tool.helpers import init_nornir
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
    
    # TODO

) -> None:
    """Show MTU values for all interfaces."""
    nr = ctx.obj

    # TODO


@app.command()
def neighbors(
    ctx: typer.Context,
    
    # TODO

) -> None:
    """Display the MTU values for all interfaces along with their corresponding neighbors."""
    nr = ctx.obj

    # TODO


@app.command()
def path(
    ctx: typer.Context,
    
    # TODO

) -> None:
    """Recursively print the MTU of all interfaces for all paths from the specified device to the specified destination."""
    nr = ctx.obj

    # TODO


if __name__ == "__main__":
    app()
