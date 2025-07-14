import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Dict


class Storage:

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / ".bloblite_storage"
        self.base_path.mkdir(parents=True, exist_ok=True)

    def create_container(self, name: str) -> None:
        """
        Crea un nuevo contenedor (carpeta).

        Args:
            name: Nombre del contenedor.

        Raises:
            ValueError: Si el contenedor ya existe.
        """
        container_path = self.base_path / name
        if container_path.exists():
            print(f"ℹ️ Container '{name}' already exists.")
            return

        container_path.mkdir()
        print(f"✅ Container '{name}' created.")

    def list_containers(self) -> List[str]:
        """
        Lista todos los contenedores existentes.

        Returns:
            Lista de nombres de contenedores.
        """
        containers = sorted([d.name for d in self.base_path.iterdir() if d.is_dir()])

        if not containers:
            print("⚠️ No exists containers")
        else:
            print("📦 Available containers:")
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
        container_path = self.base_path / container
        if not container_path.exists():
            print(f"Container '{container}' does not exist.")
            return

        source = Path(file_path)
        if not source.exists():
            print(f"❌ Source file '{file_path}' not found.")
            return

        dst = container_path / source.name

        if dst.exists():
            print(
                f"ℹ️ Blob '{source.name}' already exists in container '{container}'. Skipping upload."
            )
            return

        shutil.copy2(source, dst)

        metadata: Dict[str, str | int] = {
            "name": source.name,
            "size": source.stat().st_size,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "content_type": "application/octet-stream",
        }

        metadata_file = container_path / f"{source.stem}.metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        print(f"⬆️  Uploaded '{source.name}' to container '{container}'.")

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
        container_path = self.base_path / container
        if not container_path.exists():
            if verbose:
                print(f"❌ Error: Container '{container}' does not exist.")
            return []

        blobs = sorted(
            [
                f.name
                for f in container_path.iterdir()
                if f.is_file() and not f.name.endswith(".metadata.json")
            ]
        )

        if verbose:
            if not blobs:
                print(f"ℹ️  Container '{container}' is empty.")
            else:
                print(f"📄 Blobs in container '{container}':")
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
        container_path = self.base_path / container
        blob_path = container_path / blob_name
        if not blob_path.exists():
            print(f"Blob '{blob_name}' not found in container '{container}'.")
            return

        shutil.copy2(blob_path, destination)
        print(f"⬇️  Downloaded '{blob_name}' to '{destination}'.")

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
        container_path = self.base_path / container
        metadata_path = container_path / f"{Path(blob_name).stem}.metadata.json"
        if not metadata_path.exists():
            return None

        with open(metadata_path, encoding="utf-8") as f:
            return json.load(f)
