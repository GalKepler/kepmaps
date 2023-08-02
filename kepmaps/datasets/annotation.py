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
        return list(self.tree.get(self.SUBFOLDER_NAME).get(annotation).keys())

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
