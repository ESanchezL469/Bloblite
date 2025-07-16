from pathlib import Path

from bloblite.storage import Storage


class ContainerClient:
    """
    Simulates Azure's Container Client for a single container.
    """

    def __init__(self, name: str, storage: Storage) -> None:
        self.name = name
        self.storage = storage

    def create_container(self) -> None:
        """
        Create this container if it doesn't exist.
        """
        self.storage.create_container(self.name)

    def list_blobs(self) -> None:
        """
        List blobs inside this container.
        """
        self.storage.list_blobs(self.name)

    def upload_blob(self, file_path: str | Path) -> None:
        """
        Upload a blob to the container.
        """
        self.storage.upload_blob(self.name, str(file_path))

    def download_blob(self, blob_name: str, dest_path: str | Path) -> None:
        """
        Download a blob to a given destination.
        """
        self.storage.download_blob(self.name, blob_name, str(dest_path))

    def get_blob_metadata(self, blob_name: str) -> dict:
        """
        Return metadata for a blob.
        """
        return self.storage.get_blob_metadata(self.name, blob_name)
