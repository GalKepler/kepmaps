import json
from pathlib import Path

# set up path to "data/kepmaps.json"
KEPMAPS_CONFIG = Path(__file__).parents[2] / "data" / "kepmaps.json"


def _get_project(project: str = None):
    """
    Returns the OSF project ID. By default, it returns KepMap's.

    Parameters
    ----------
    project : str, optional
        OSF project ID, by default None
    """
    if project is None:
        with open(KEPMAPS_CONFIG, "r") as f:
            project = json.load(f)
            project = project.get("osf").get("project")
    return project
