import json
from pathlib import Path
from typing import Union

# set up path to "data/kepmaps.json"
KEPMAPS_CONFIG = Path(__file__).parents[2] / "data"


def _get_project(
    project: str = None, config_file: Path = KEPMAPS_CONFIG / "kepmaps.json"
):
    """
    Return the OSF project ID. By default, it returns KepMap's.

    Parameters
    ----------
    project : str, optional
        OSF project ID, by default None
    """
    if project is None:
        with open(config_file, "r", encoding="utf-8") as f:
            project = json.load(f)
            project = project.get("osf").get("project")
    return project


def _get_path_patterns(
    bids_config: Union[str, Path] = KEPMAPS_CONFIG / "bids.json"
) -> list:
    """
    Get path patterns from a json file of BIDS configurations.

    Parameters
    ----------
    bids_config : Union[str,Path]
        Path to json file of BIDS configurations.

    Returns
    -------
    list
        List of path patterns.
    """
    with open(bids_config, "r", encoding="utf-8") as f:
        bids_config = json.load(f)
        path_patterns = bids_config.get("path_patterns")
    return path_patterns
