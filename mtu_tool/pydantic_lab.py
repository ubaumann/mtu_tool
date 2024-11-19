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
    pass
    main_model_schema = Model.model_json_schema()
    console.print_json(data=main_model_schema)


def task3() -> None:
    # Create a Data Structure from the Objects and Print the JSON
    pass
    vias = [Via(interface=f"Eth{x}", nexthopAddr=f"10.0.0.{x}") for x in range(4)]
    route = Route(
        hardwareProgrammed=True,
        routeType="Fake",
        routeLeaked=False,
        kernelProgrammed=True,
        preference=250,
        metric=666,
        routeAction="forward",
        vias=vias,
        directlyConnected=True,
    )
    vrf = Vrf(
        routingDisabled=False,
        allRoutesProgrammedHardware=True,
        allRoutesProgrammedKernel=True,
        defaultRouteState="notSet",
        routes={"10.10.10.0/24": route},
    )
    model = Model(vrfs={"default": vrf})

    console.print_json(model.model_dump_json())


if __name__ == "__main__":
    console.rule("Task 1")
    task1()
    console.rule("Task 2")
    task2()
    console.rule("Task 3")
    task3()
