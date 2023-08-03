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

    def _get_spaces(self, annotation: str, entities: dict = None) -> list:
        """
        Return a list of spaces for a given annotation.

        Parameters
        ----------
        annotation : str
            Annotation to query.
        entities : dict, optional
            Entities to query, by default None

        Returns
        -------
        list
            List of spaces for a given annotation.
        """
        spaces = entities.get("space") if entities is not None else None
        if spaces is None:
            spaces = self.query_available_spaces(annotation)
        else:
            if not isinstance(spaces, list):
                spaces = [spaces]
        return spaces

    def _get_space_data(
        self, annotation_data: dict, space: str, entities: dict = None
    ) -> dict:
        """
        Return a dictionary of the space data.

        Parameters
        ----------
        annotation_data : dict
            Dictionary of the annotation data.
        space : str
            Space to query.
        entities : dict, optional
            Entities to query, by default None

        Returns
        -------
        dict
            Dictionary of the space data.
        """
        result = annotation_data.get(space)
        if "den" in entities:
            result = result.get(entities.get("den"))
        for key in result:
            file_entities = parse_file_entities(key)
            # check if entities match, if not, don't add to result
            for entity, entity_value in entities.items():
                if entity in file_entities:
                    if entity_value != file_entities.get(entity):
                        result.pop(key)
                        break
        return result

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
        spaces = self._get_spaces(annotation, entities)
        annotation_data = self.tree.get(self.SUBFOLDER_NAME).get(annotation)
        result = {}
        for space in spaces:
            result[space] = self._get_space_data(
                annotation_data, space, entities
            )
        result["supp"] = {
            key: annotation_data.get(key)
            for key in [f"atlas-{annotation}_dseg.tsv", "references.bib"]
        }

        for main_key, sub_results in result.items():
            for key, file in sub_results.items():
                file_destination = Path(destination) / file.path.replace(
                    self.SUBFOLDER_NAME, ""
                ).replace("//", "")
                print(file_destination)
                file_destination.parent.mkdir(parents=True, exist_ok=True)
                with open(str(file_destination), "wb") as f:
                    file.write_to(f)
                # result[main_key][key].update(file_destination)

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
