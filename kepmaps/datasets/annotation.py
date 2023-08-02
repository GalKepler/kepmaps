from pathlib import Path
from typing import Union
from osfclient.models import File
from bids.layout.layout import parse_file_entities
from kepmaps.datasets.dataset import Dataset


# Annotation class inherits from Dataset class
class Annotation(Dataset):

    SUBFOLDER_NAME = "annotations"

    def __init__(self, project: str = None) -> None:
        super().__init__(project)

    def _get_available_annotations(self) -> list:
        """
        Return a list of available annotations.

        Returns
        -------
        list
            List of available annotations.
        """
        return list(self.tree.get(self.SUBFOLDER_NAME).keys())

    def query_available_spaces(self, annotation: str) -> list:
        """
        Return a list of available spaces for a given annotation.

        Parameters
        ----------
        annotation : str
            Annotation to query.

        Returns
        -------
        list
            List of available spaces for a given annotation.
        """
        destination = self.tree.get(self.SUBFOLDER_NAME).get(annotation)
        return [
            key
            for key in destination.keys()
            if not isinstance(destination.get(key), File)
        ]

    def fetch(
        self,
        annotation: str,
        entities: dict = None,
        destination: Union[str, Path] = None,
    ) -> dict:
        """
        Fetch annotation from OSF project.

        Parameters
        ----------
        annotation : str
            Annotation to fetch.
        entities : dict, optional
            Entities to fetch, by default None
        destination : Union[str,Path], optional
            Destination folder, by default None

        Returns
        -------
        dict
            Dictionary of the fetched annotation.
        """
        spaces = entities.get("space")
        if spaces is None:
            spaces = self.query_available_spaces(annotation)
        else:
            if not isinstance(spaces, list):
                spaces = [spaces]

        annotation_data = self.tree.get(self.SUBFOLDER_NAME).get(annotation)
        result = {}
        for space in spaces:
            space_result = annotation_data.get(space)
            if "den" in entities:
                space_result = space_result.get(entities.get("den"))
            for key, file in space_result.items():
                file_entities = parse_file_entities(key)
                # check if entities match, if not, don't add to result
                for entity, entity_value in entities.items():
                    if entity in file_entities:
                        if entity_value != file_entities.get(entity):
                            space_result.pop(key)
                            break
                
            result[space] = space_result
            
        return result

    @property
    def available_annotations(self) -> list:
        """
        Return a list of available annotations.

        Returns
        -------
        list
            List of available annotations.
        """
        return self._get_available_annotations()
