from pydantic import ValidationError
from rich.console import Console
from mtu_tool.models.show_route import Model, Vrf, Route, Via

console = Console()


def task1() -> None:
    # Update the Model to only accapt IPv4 addresses as a `nextHopAddr`
    try:
        Via(interface="Eth1", nexthopAddr="not_an_ip")
    except ValidationError:
        console.print_exception(show_locals=True)
        console.print("this is expected to happen!!!")
    v = Via(interface="Eth1", nexthopAddr="10.0.0.0")
    console.print(f"This time it worked well: {v}")
    console.print(f"nexthoAddr type is {type(v.nexthopAddr)}")


def task2() -> None:
    # Print out the JSON Schema
    # TODO
    pass


def task3() -> None:
    # Create a Data Structure from the Objects and Print the JSON
    # TODO
    pass


if __name__ == "__main__":
    console.rule("Task 1")
    task1()
    console.rule("Task 2")
    task2()
    console.rule("Task 3")
    task3()
