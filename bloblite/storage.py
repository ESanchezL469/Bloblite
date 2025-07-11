import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Dict

# 📁 Ruta base del sistema de almacenamiento
BASE_PATH: Path = Path.home() / ".bloblite_storage"

def _ensure_base_path() -> None:
    """Garantiza que el directorio base exista."""
    BASE_PATH.mkdir(parents=True, exist_ok=True)

def create_container(name: str) -> None:
    """
    Crea un nuevo contenedor (carpeta).

    Args:
        name: Nombre del contenedor.

    Raises:
        ValueError: Si el contenedor ya existe.
    """
    _ensure_base_path()
    container_path = BASE_PATH / name
    if container_path.exists():
        raise ValueError(f"Container '{name}' already exists.")
    container_path.mkdir()
    print(f"✅ Container '{name}' created.")

def list_containers() -> List[str]:
    """
    Lista todos los contenedores existentes.

    Returns:
        Lista de nombres de contenedores.
    """
    _ensure_base_path()
    return sorted([
        d.name for d in BASE_PATH.iterdir()
        if d.is_dir()
    ])

def upload_blob(container: str, file_path: str) -> None:
    """
    Sube un archivo al contenedor especificado y guarda su metadata.

    Args:
        container: Nombre del contenedor.
        file_path: Ruta del archivo local a subir.

    Raises:
        FileNotFoundError: Si el contenedor o el archivo no existen.
    """
    _ensure_base_path()
    container_path = BASE_PATH / container
    if not container_path.exists():
        raise FileNotFoundError(f"Container '{container}' does not exist.")

    source = Path(file_path)
    if not source.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    destination = container_path / source.name
    shutil.copy2(source, destination)

    metadata: Dict[str, str | int] = {
        "name": source.name,
        "size": source.stat().st_size,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "content_type": "application/octet-stream"
    }

    metadata_file = container_path / f"{source.stem}.metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"⬆️  Uploaded '{source.name}' to container '{container}'.")

def list_blobs(container: str) -> List[str]:
    """
    Lista todos los blobs dentro de un contenedor.

    Args:
        container: Nombre del contenedor.

    Returns:
        Lista de nombres de blobs (archivos).

    Raises:
        FileNotFoundError: Si el contenedor no existe.
    """
    container_path = BASE_PATH / container
    if not container_path.exists():
        raise FileNotFoundError(f"Container '{container}' does not exist.")

    blobs = sorted([
        f.name for f in container_path.iterdir()
        if f.is_file() and not f.name.endswith(".metadata.json")
    ])
    return blobs

def download_blob(container: str, blob_name: str, destination: str) -> None:
    """
    Descarga un blob a una ruta local.

    Args:
        container: Nombre del contenedor.
        blob_name: Nombre del archivo.
        destination: Ruta local destino.

    Raises:
        FileNotFoundError: Si el blob no existe.
    """
    container_path = BASE_PATH / container
    blob_path = container_path / blob_name
    if not blob_path.exists():
        raise FileNotFoundError(f"Blob '{blob_name}' not found in container '{container}'.")

    shutil.copy2(blob_path, destination)
    print(f"⬇️  Downloaded '{blob_name}' to '{destination}'.")

def get_blob_metadata(container: str, blob_name: str) -> Optional[Dict[str, str | int]]:
    """
    Retorna la metadata asociada a un blob.

    Args:
        container: Nombre del contenedor.
        blob_name: Nombre del archivo.

    Returns:
        Diccionario con metadata o None si no existe.
    """
    container_path = BASE_PATH / container
    metadata_path = container_path / f"{Path(blob_name).stem}.metadata.json"
    if not metadata_path.exists():
        return None

    with open(metadata_path, encoding="utf-8") as f:
        return json.load(f)
