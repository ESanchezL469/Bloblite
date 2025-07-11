import argparse
import sys
from typing import Optional
from pathlib import Path

from bloblite.storage import (create_container,list_containers, upload_blob, 
                              list_blobs, download_blob, get_blob_metadata)


def handle_create(container: str) -> None:
    """
    Maneja la creación de un contenedor.

    Args:
        container: Nombre del contenedor a crear.
    """
    create_container(container)


def handle_list(container: Optional[str]) -> None:
    """
    Lista contenedores o blobs dentro de un contenedor.

    Args:
        container: Nombre del contenedor o None para listar todos.
    """
    if container:
        blobs = list_blobs(container)
        print(f"📄 Blobs en '{container}':")
        for blob in blobs:
            print(f"  - {blob}")
    else:
        containers = list_containers()
        print("📦 Contenedores:")
        for name in containers:
            print(f"  - {name}")


def handle_upload(container: str, file_path: str) -> None:
    """
    Sube un archivo a un contenedor.

    Args:
        container: Nombre del contenedor.
        file_path: Ruta del archivo a subir.
    """
    upload_blob(container, file_path)


def handle_download(container: str, blob: str, destination: str) -> None:
    """
    Descarga un blob desde un contenedor.

    Args:
        container: Nombre del contenedor.
        blob: Nombre del archivo.
        destination: Ruta de destino local.
    """
    download_blob(container, blob, destination)


def handle_metadata(container: str, blob: str) -> None:
    """
    Muestra la metadata de un blob.

    Args:
        container: Nombre del contenedor.
        blob: Nombre del archivo.
    """
    metadata = get_blob_metadata(container, blob)
    if metadata:
        print(f"ℹ️  Metadata de '{blob}':")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
    else:
        print("⚠️  No se encontró metadata para ese blob.")


def build_parser() -> argparse.ArgumentParser:
    """
    Construye y devuelve el parser de argumentos.

    Returns:
        Objeto ArgumentParser configurado.
    """
    parser = argparse.ArgumentParser(
        description="BlobLite: Simulador local de Azure Blob Storage."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create
    create_parser = subparsers.add_parser("create", help="Crear un contenedor.")
    create_parser.add_argument("container", type=str)

    # list
    list_parser = subparsers.add_parser("list", help="Listar contenedores o blobs.")
    list_parser.add_argument("container", type=str, nargs="?", default=None)

    # upload
    upload_parser = subparsers.add_parser("upload", help="Subir un archivo.")
    upload_parser.add_argument("container", type=str)
    upload_parser.add_argument("file", type=str)

    # download
    download_parser = subparsers.add_parser("download", help="Descargar un archivo.")
    download_parser.add_argument("container", type=str)
    download_parser.add_argument("blob", type=str)
    download_parser.add_argument("destination", type=str)

    # metadata
    meta_parser = subparsers.add_parser("metadata", help="Ver metadata de un archivo.")
    meta_parser.add_argument("container", type=str)
    meta_parser.add_argument("blob", type=str)

    return parser


def main() -> None:
    """
    Punto de entrada del CLI.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        match args.command:
            case "create":
                handle_create(args.container)
            case "list":
                handle_list(args.container)
            case "upload":
                handle_upload(args.container, args.file)
            case "download":
                handle_download(args.container, args.blob, args.destination)
            case "metadata":
                handle_metadata(args.container, args.blob)
            case _:
                parser.print_help()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
