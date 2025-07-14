import argparse
import os
from pathlib import Path

from bloblite.storage import Storage


def _setup_arg_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser for BlobLite CLI."""
    parser = argparse.ArgumentParser(
        prog="bloblite",
        description="[ok] BlobLite - Azure Blob Storage simulator (local)",
        epilog="Example: 'bloblite container create my-container'",
    )

    # Container subcommands
    subp = parser.add_subparsers(dest="resource", required=True)

    cont_parser = subp.add_parser("container", help="Manage containers")
    cont_sub = cont_parser.add_subparsers(dest="action", required=True)

    # Container actions
    cont_create = cont_sub.add_parser("create", help="Create a new container")
    cont_create.add_argument("name", help="Name of the container to create")

    cont_sub.add_parser("list", help="List all containers")

    # Blob subcommands
    blob_parser = subp.add_parser("blob", help="Manage blobs inside containers")
    blob_sub = blob_parser.add_subparsers(dest="action", required=True)

    # Blob actions
    blob_upload = blob_sub.add_parser("upload", help="Upload a file to a container")
    blob_upload.add_argument("--container", required=True, help="Target container name")
    blob_upload.add_argument("--file", required=True, help="Path to local file")

    blob_download = blob_sub.add_parser(
        "download", help="Download a blob from a container"
    )
    blob_download.add_argument("--container", required=True, help="Container name")
    blob_download.add_argument("--name", required=True, help="Blob name to download")
    blob_download.add_argument("--dest", required=True, help="Destination folder path")

    blob_list = blob_sub.add_parser("list", help="List all blobs in a container")
    blob_list.add_argument("--container", required=True, help="Container name")

    blob_meta = blob_sub.add_parser("show-metadata", help="Show blob metadata")
    blob_meta.add_argument("--container", required=True, help="Container name")
    blob_meta.add_argument("--name", required=True, help="Blob name")

    return parser


def _get_storage() -> Storage:
    """Crea una instancia de Storage configurable vía BLOBLITE_ROOT."""
    custom_root = os.environ.get("BLOBLITE_ROOT")
    root_path = Path(custom_root) if custom_root else None
    return Storage(base_path=root_path)


def _handle_container_actions(args, storage: Storage) -> None:
    """Execute container-related actions based on parsed arguments."""
    if args.action == "create":
        storage.create_container(name=args.name)
    elif args.action == "list":
        storage.list_containers()


def _handle_blob_actions(args, storage: Storage) -> None:
    """Execute blob-related actions based on parsed arguments."""
    if args.action == "upload":
        storage.upload_blob(container=args.container, file_path=args.file)
    elif args.action == "download":
        storage.download_blob(
            container=args.container,
            blob_name=args.name,
            destination=args.dest,
        )
    elif args.action == "list":
        storage.list_blobs(container=args.container)
    elif args.action == "show-metadata":
        metadata = storage.get_blob_metadata(
            container=args.container, blob_name=args.name
        )
        if metadata:
            print(metadata)
        else:
            print("[info] Metadata not found.")


def main() -> None:
    """Entry point for the BlobLite CLI application."""
    parser = _setup_arg_parser()
    args = parser.parse_args()

    storage = _get_storage()

    if args.resource == "container":
        _handle_container_actions(args, storage)
    elif args.resource == "blob":
        _handle_blob_actions(args, storage)


if __name__ == "__main__":
    main()
