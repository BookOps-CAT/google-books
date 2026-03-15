from pathlib import Path

from click.testing import CliRunner
import pytest

from google_books import cli


@pytest.mark.parametrize(
    "arg,expectation", [("onsite", "1999-12-31_onsite"), ("recap", "1999-12-31_recap")]
)
def test_new_shipment(tmp_path, arg, expectation):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        twd = Path(td)
        f = twd / "files"
        f.mkdir()
        s = f / "shipments"
        s.mkdir()

        result = runner.invoke(cli, ["new-shipment", "19991231", arg])
        assert result.exit_code == 0
        output = Path(f"files/shipments/{expectation}")
        assert result.output == f"New shipment directory created at {output}\n"


def test_new_shipment_invalid_mat_source(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        twd = Path(td)
        f = twd / "files"
        f.mkdir()
        s = f / "shipments"
        s.mkdir()

        result = runner.invoke(cli, ["new-shipment", "19991231", "foobar"])
        assert result.exit_code == 0
        assert (
            result.output
            == "Invalid material source argument. Please use 'onsite' or 'recap'.\n"
        )

        # verify that no new directory was created
        assert not (s / "1999-12-31_foobar").exists()
