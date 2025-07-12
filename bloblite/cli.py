import argparse
from bloblite import storage


def _setup_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bloblite",
        description="📦 BlobLite - Azure Blob Storage simulator (local)",
    )

    subparsers = parser.add_subparsers(dest="resource", required=True)

    # ░█▀▀░█░█░█▀▄░█▀▀░█▀▀
    # ░█▀▀░░█░░█▀▄░█▀▀░▀▀█
    # ░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀

    container_parser = subparsers.add_parser("container", help="Manage containers")
    container_sub = container_parser.add_subparsers(dest="action", required=True)

    container_create = container_sub.add_parser("create", help="Create a new container")
    container_create.add_argument("name", help="Name of the container to create")

    container_sub.add_parser("list", help="List all containers")

    # ░█▀█░█░█░█▀▀░█▀█
    # ░█▀▀░█░█░█▀▀░█░█
    # ░▀░░░▀▀▀░▀▀▀░▀░▀

    blob_parser = subparsers.add_parser("blob", help="Manage blobs inside containers")
    blob_sub = blob_parser.add_subparsers(dest="action", required=True)

    blob_upload = blob_sub.add_parser("upload", help="Upload a file to a container")
    blob_upload.add_argument("--container", required=True, help="Target container name")
    blob_upload.add_argument("--file", required=True, help="Path to local file")

    blob_download = blob_sub.add_parser("download", help="Download a blob from a container")
    blob_download.add_argument("--container", required=True, help="Container name")
    blob_download.add_argument("--name", required=True, help="Blob name to download")
    blob_download.add_argument("--dest", required=True, help="Destination folder path")

    blob_list = blob_sub.add_parser("list", help="List all blobs in a container")
    blob_list.add_argument("--container", required=True, help="Container name")

    blob_meta = blob_sub.add_parser("show-metadata", help="Show blob metadata")
    blob_meta.add_argument("--container", required=True, help="Container name")
    blob_meta.add_argument("--name", required=True, help="Blob name")

    return parser


def main() -> None:
    parser = _setup_arg_parser()
    args = parser.parse_args()

    if args.resource == "container":
        if args.action == "create":
            storage.create_container(container_name=args.name)
        elif args.action == "list":
            storage.list_containers()

    elif args.resource == "blob":
        if args.action == "upload":
            storage.upload_blob(container_name=args.container, file_path=args.file)
        elif args.action == "download":
            storage.download_blob(
                container_name=args.container,
                blob_name=args.name,
                destination_path=args.dest,
            )
        elif args.action == "list":
            storage.list_blobs(container_name=args.container)
        elif args.action == "show-metadata":
            storage.get_blob_metadata(container_name=args.container, blob_name=args.name)


if __name__ == "__main__":
    main()
