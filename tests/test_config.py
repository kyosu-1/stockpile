from stockpile.config import load_config, init_config


class TestLoadConfig:
    def test_nonexistent_path_returns_defaults(self, tmp_path):
        config = load_config(tmp_path / "nonexistent.toml")
        assert config.storage_backend == "sqlite"
        assert config.default_market == "us"
        assert config.default_output_format == "table"
        assert config.api_keys.fred == ""

    def test_full_config(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text("""\
[storage]
backend = "postgres"
path = "/custom/path"

[defaults]
market = "jp"
output_format = "json"

[api_keys]
fred = "my-fred-key"
fmp = "my-fmp-key"
""")
        config = load_config(config_file)
        assert config.storage_backend == "postgres"
        assert config.storage_path == "/custom/path"
        assert config.default_market == "jp"
        assert config.default_output_format == "json"
        assert config.api_keys.fred == "my-fred-key"
        assert config.api_keys.fmp == "my-fmp-key"

    def test_partial_config(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text("""\
[storage]
backend = "sqlite"
""")
        config = load_config(config_file)
        assert config.storage_backend == "sqlite"
        assert config.default_market == "us"  # default
        assert config.api_keys.fred == ""  # default

    def test_empty_file(self, tmp_path):
        config_file = tmp_path / "config.toml"
        config_file.write_text("")
        config = load_config(config_file)
        assert config.storage_backend == "sqlite"


class TestInitConfig:
    def test_creates_file(self, tmp_path):
        config_path = tmp_path / "sub" / "config.toml"
        result = init_config(config_path)
        assert result == config_path
        assert config_path.exists()
        content = config_path.read_text()
        assert "[storage]" in content
        assert "[api_keys]" in content

    def test_does_not_overwrite_existing(self, tmp_path):
        config_path = tmp_path / "config.toml"
        config_path.write_text("existing content")
        result = init_config(config_path)
        assert result == config_path
        assert config_path.read_text() == "existing content"
