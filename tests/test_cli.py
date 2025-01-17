from click.testing import CliRunner
from google_books import cli


def test_new_shipment(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(cli, ["new-shipment", "19991231", td])
        assert result.exit_code == 0
        assert result.output == f"New shipment directory created at {td}\\1999-12-31\n"
