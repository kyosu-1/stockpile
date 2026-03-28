import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "stockpile"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.toml"
DEFAULT_DATA_DIR = Path.home() / ".local" / "share" / "stockpile" / "data"


@dataclass
class ApiKeys:
    jquants: str = ""
    fmp: str = ""
    finnhub: str = ""
    gnews: str = ""
    fred: str = ""


@dataclass
class Config:
    storage_backend: str = "sqlite"
    storage_path: str = str(DEFAULT_DATA_DIR)
    default_market: str = "us"
    default_output_format: str = "table"
    api_keys: ApiKeys = field(default_factory=ApiKeys)


def load_config(config_path: Path | None = None) -> Config:
    path = config_path or DEFAULT_CONFIG_PATH
    if not path.exists():
        return Config()

    with open(path, "rb") as f:
        data = tomllib.load(f)

    config = Config()

    if "storage" in data:
        config.storage_backend = data["storage"].get("backend", config.storage_backend)
        config.storage_path = data["storage"].get("path", config.storage_path)

    if "defaults" in data:
        config.default_market = data["defaults"].get("market", config.default_market)
        config.default_output_format = data["defaults"].get("output_format", config.default_output_format)

    if "api_keys" in data:
        keys = data["api_keys"]
        config.api_keys = ApiKeys(
            jquants=keys.get("jquants", ""),
            fmp=keys.get("fmp", ""),
            finnhub=keys.get("finnhub", ""),
            gnews=keys.get("gnews", ""),
            fred=keys.get("fred", ""),
        )

    return config


def init_config(config_path: Path | None = None) -> Path:
    path = config_path or DEFAULT_CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return path

    template = """\
[storage]
backend = "sqlite"
path = "{data_dir}"

[defaults]
market = "us"
output_format = "table"

[api_keys]
jquants = ""
fmp = ""
finnhub = ""
gnews = ""
fred = ""
""".format(data_dir=DEFAULT_DATA_DIR)

    path.write_text(template)
    return path
