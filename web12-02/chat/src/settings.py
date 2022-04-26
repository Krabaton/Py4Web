import pathlib
import yaml
from os import environ

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config" / 'config.yaml'


def get_config(path):
    with open(path) as f:
        parsed_config = yaml.safe_load(f)
        print(environ.get("DATABASE_URL", None))
        print(environ.get("PORT", None))
        if environ.get("APPID", None):
            parsed_config["common"].update({"appid": environ["APPID"]})
        if environ.get("PORT", None):
            parsed_config["common"].update({"port": environ["PORT"]})
        if environ.get("DATABASE_URL", None):
            parsed_config["postgres"].update({"database_url": environ["DATABASE_URL"]})
    return parsed_config


config = get_config(config_path)