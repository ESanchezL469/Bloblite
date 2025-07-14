from pathlib import Path
from typing import List, Optional
from bloblite.storage import Storage
from bloblite.sdk.container_client import ContainerClient


class BlobServiceClient:
    """
    Simulates Azure BlobServiceClient for local use.
    """

    def __init__(self, storage_root: Optional[Path] = None) -> None:
        self.storage = Storage(storage_root)
        self.storage_root = storage_root

    def list_containers(self) -> List[str]:
        """
        List all available containers (folders).
        """
        return [item.name for item in self.storage_root.iterdir() if item.is_dir()]

    def get_container_client(self, name: str) -> ContainerClient:
        """
        Returns a ContainerClient for the given container name.
        """
        return ContainerClient(name=name, storage=self.storage)
