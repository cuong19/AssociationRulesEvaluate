from src.common.path import Path
from src.common.yaml import Yaml


def get_config(path, filename):
    """
    Get the config file
    :param path: usually Path(__file__) to get the path of the current app
    :param filename: name of the config file
    :return: The config variable if succeeded
    """
    try:
        return Yaml(path.get_absolute_path(filename)).content
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    # Parse the config file
    conf = get_config(Path(__file__), "config.yml")