from pathlib import Path

from click.testing import CliRunner
from google_books import cli


def test_new_shipment(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        twd = Path(td)
        f = twd / "files"
        f.mkdir()
        s = f / "shipments"
        s.mkdir()

        result = runner.invoke(cli, ["new-shipment", "19991231"])
        assert result.exit_code == 0
        output = Path("files/shipments/1999-12-31")
        assert result.output == f"New shipment directory created at {output}\n"
