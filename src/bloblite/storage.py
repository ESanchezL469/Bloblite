import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Dict


class Storage:

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / ".bloblite_storage"
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(
                f"[alert] Warning: Cannot create or access storage at {self.base_path}. Check your permissions."
            )
            self.base_path = None

    def create_container(self, name: str) -> None:
        """
        Crea un nuevo contenedor (carpeta).

        Args:
            name: Nombre del contenedor.

        Raises:
            ValueError: Si el contenedor ya existe.
        """
        if not self.base_path:
            print("[alert] Storage not initialized. Cannot create container.")
            return
        container_path = self.base_path / name
        if container_path.exists():
            print(f"[info] Container '{name}' already exists.")
            return

        try:
            container_path.mkdir()
            print(f"[ok] Container '{name}' created.")
        except PermissionError:
            print(f"[alert] Cannot create container '{name}'. Check your permissions.")

    def list_containers(self) -> List[str]:
        """
        Lista todos los contenedores existentes.

        Returns:
            Lista de nombres de contenedores.
        """
        if not self.base_path:
            print("[alert] Storage not initialized. Cannot list containers.")
            return []
        try:
            containers = sorted(
                [d.name for d in self.base_path.iterdir() if d.is_dir()]
            )
        except (PermissionError, OSError):
            print("[alert] Cannot access containers. Permission denied.")
            return []

        if not containers:
            print("[alert] No exists containers")
        else:
            print("[ok] Available containers:")
            for i, container in enumerate(containers, 1):
                print(f" {i}. {container}")
            print(f"\nTotal: {len(containers)} container(s)")
        return containers

    def upload_blob(self, container: str, file_path: str) -> None:
        """
        Sube un archivo al contenedor especificado y guarda su metadata.

        Args:
            container: Nombre del contenedor.
            file_path: Ruta del archivo local a subir.

        Raises:
            FileNotFoundError: Si el contenedor o el archivo no existen.
        """
        if not self.base_path:
            print("[alert] Storage not initialized. Cannot upload.")
            return
        container_path = self.base_path / container
        if not container_path.exists():
            print(f"Container '{container}' does not exist.")
            return

        source = Path(file_path)
        if not source.exists():
            print(f"[error] Source file '{file_path}' not found.")
            return

        dst = container_path / source.name

        if dst.exists():
            print(
                f"[info] Blob '{source.name}' already exists in container '{container}'. Skipping upload."
            )
            return

        try:
            shutil.copy2(source, dst)
        except (PermissionError, IOError):
            print(f"[alert] Cannot copy file to '{dst}'. Check permissions.")
            return

        metadata: Dict[str, str | int] = {
            "name": source.name,
            "size": source.stat().st_size,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "content_type": "application/octet-stream",
        }

        metadata_file = container_path / f"{source.stem}.metadata.json"
        try:
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
        except (PermissionError, IOError):
            print(f"[alert] Failed to write metadata for '{source.name}'.")

        print(f"[ok]  Uploaded '{source.name}' to container '{container}'.")

    def list_blobs(self, container: str, verbose: bool = True) -> List[str]:
        """
        Lista todos los blobs dentro de un contenedor.

        Args:
            container: Nombre del contenedor.
            verbose: Si True, imprime los resultados (modo CLI). Si False, solo retorna la lista.
        Returns:
            Lista de nombres de blobs (archivos).

        Raises:
            FileNotFoundError: Si el contenedor no existe.
        """
        if not self.base_path:
            if verbose:
                print("[alert] Storage not initialized. Cannot list blobs.")
            return []
        container_path = self.base_path / container
        if not container_path.exists():
            if verbose:
                print(f"[error] Error: Container '{container}' does not exist.")
            return []

        try:
            blobs = sorted(
                [
                    f.name
                    for f in container_path.iterdir()
                    if f.is_file() and not f.name.endswith(".metadata.json")
                ]
            )
        except (PermissionError, OSError):
            if verbose:
                print(f"[alert] Cannot access files in container '{container}'.")
            return []

        if verbose:
            if not blobs:
                print(f"[info]  Container '{container}' is empty.")
            else:
                print(f"Blobs in container '{container}':")
                for i, blob in enumerate(blobs, 1):
                    print(f"  {i}. {blob}")
                print(f"\nTotal: {len(blobs)} blob(s)")
        return blobs

    def download_blob(self, container: str, blob_name: str, destination: str) -> None:
        """
        Descarga un blob a una ruta local.

        Args:
            container: Nombre del contenedor.
            blob_name: Nombre del archivo.
            destination: Ruta local destino.

        Raises:
            FileNotFoundError: Si el blob no existe.
        """
        if not self.base_path:
            print("[alert] Storage not initialized. Cannot download.")
            return
        container_path = self.base_path / container
        blob_path = container_path / blob_name
        if not blob_path.exists():
            print(f"Blob '{blob_name}' not found in container '{container}'.")
            return

        try:
            shutil.copy2(blob_path, destination)
            print(f"[ok]  Downloaded '{blob_name}' to '{destination}'.")
        except (PermissionError, IOError):
            print(f"[alert] Cannot write blob to '{destination}'. Check permissions.")

    def get_blob_metadata(
        self, container: str, blob_name: str
    ) -> Optional[Dict[str, str | int]]:
        """
        Retorna la metadata asociada a un blob.

        Args:
            container: Nombre del contenedor.
            blob_name: Nombre del archivo.

        Returns:
            Diccionario con metadata o None si no existe.
        """
        if not self.base_path:
            print("[alert] Storage not initialized. Cannot get metadata.")
            return None
        container_path = self.base_path / container
        metadata_path = container_path / f"{Path(blob_name).stem}.metadata.json"
        if not metadata_path.exists():
            return None

        try:
            with open(metadata_path, encoding="utf-8") as f:
                return json.load(f)
        except (PermissionError, IOError):
            print(f"[alert] Cannot read metadata for blob '{blob_name}'.")
            return None
