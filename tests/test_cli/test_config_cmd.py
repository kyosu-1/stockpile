from unittest.mock import patch

from stockpile.cli.app import app


class TestConfigInit:
    @patch("stockpile.cli.config_cmd.init_config")
    def test_init_command(self, mock_init, cli_runner, tmp_path):
        mock_init.return_value = tmp_path / "config.toml"
        result = cli_runner.invoke(app, ["config", "init"])
        assert result.exit_code == 0
        assert "Config file created" in result.output


class TestConfigShow:
    @patch("stockpile.cli.config_cmd.load_config")
    def test_show_command(self, mock_load, cli_runner, mock_config):
        mock_load.return_value = mock_config
        result = cli_runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "sqlite" in result.output
        assert "us" in result.output
