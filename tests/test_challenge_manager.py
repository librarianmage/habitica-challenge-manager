
from click.testing import CliRunner

from challenge_manager.cli import cli


def test_main():
    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.output == '()\n'
    assert result.exit_code == 0
