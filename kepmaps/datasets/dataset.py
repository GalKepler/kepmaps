from typing import Union
from osfclient.api import OSF
from osfclient.models import Folder, Project, Storage
from kepmaps.datasets.utils import _get_project


class Dataset:
    def __init__(self, project_id: str = None) -> None:
        """
        Dataset class.

        Parameters
        ----------
        project_id : str, optional
            OSF project ID, by default None
        """
        self.project_id = _get_project(project_id)

    def _get_osf_project(self) -> Project:
        """
        Return the OSF project.

        Returns
        -------
        Project
            OSF project.
        """
        osf = OSF()
        project = osf.project(self.project_id)
        return project

    def _map_folder(self, folder: Union[None, Folder, Storage]) -> dict:
        """
        Map a single folder.

        Parameters
        ----------
        folder : Union[None,Folder]
            Folder to map.

        Returns
        -------
        dict
            Dictionary of the folder.
        """
        folder_dict = {}
        for file in folder.files:
            folder_dict[file.name] = file
        for folder in folder.folders:
            folder_dict[folder.name] = self._map_folder(folder)
        return folder_dict

    def _map_project_tree(self, folder: Union[None, Folder]) -> dict:
        """
        Return a dictionary of the folders tree.

        Returns
        -------
        dict
            Dictionary of the folders tree.
        """
        folder_dict = {}
        if hasattr(folder, "files") and not isinstance(folder, Storage):
            for file in folder.files:
                folder_dict[file.name] = file
        for folder in folder.folders:
            folder_dict[folder.name] = self._map_folder(folder)
        return folder_dict

    @property
    def project(self) -> Project:
        """
        Returns the OSF project.

        Returns
        -------
        Project
            OSF project.
        """
        return self._get_osf_project()

    @property
    def tree(self) -> dict:
        """
        Recursively map the project tree.

        Returns
        -------
        dict
            Dictionary of the project tree.
        """
        return self._map_project_tree(self.project.storage())
