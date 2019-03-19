"""Tests the non-interactive functions of the CLI tool using click's runner"""

from ddl.cli import main, init_component

from ddl.asset import ComponentAsset
from click.testing import CliRunner
from test_asset_exploration import get_test_assetpack


def test_validate_assetpack():
    """Tests that an assetpack validates correctly"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert result.output == """Pack validated
Images validated
Components validated
Validation passed. assetpacks/example_isometric is a good assetpack.
"""


def test_invalidate_assetpack():
    """Tests that an assetpack fails to validate correctly"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_json_fail"])
    assert result.exit_code == 1
    assert result.output != """Pack validated
Images validated
Components validated
Validation passed. assetpacks/example_isometric is a good assetpack.
"""


def test_init_component():
    """Tests that blank components are initialised properly based on user input"""
    assetpack = get_test_assetpack()
    info = {"component_name": "test",
            "component_id": "test_id",
            "component_tags": "a,b"}

    component = init_component(assetpack, info)
    assert isinstance(component, ComponentAsset)
    assert component.name == "test"
    assert component.asset_id == "test_id"
    assert component.tags == ["a", "b"]
    assert component.parts == []
