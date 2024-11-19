import pytest
from pathlib import Path

from mtu_tool.models.show_route import Model


@pytest.mark.parametrize(
    "json_file", Path("tests/example_data/show_ip_route/").glob("*.json")
)
def test_show_route_model(json_file):
    with json_file.open() as fp:
        data = fp.read()
    m = Model.model_validate_json(data)
    assert len(m.vrfs["default"].routes)
