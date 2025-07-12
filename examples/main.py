import os
from bloblite import storage


def main() -> None:
    container = "clientes"
    file_path = "data.csv"
    dest_path = "./descargas/"
    blob_name = os.path.basename(file_path)

    # Crear contenedor (idempotente)
    try:
        storage.create_container(name=container)
    except Exception as e:
        print(f"[⚠️] Error creating container: {e}")

    # Validar que el archivo exista antes de subirlo
    if not os.path.isfile(file_path):
        print(f"[❌] File not found: {file_path}")
        return

    # Subir archivo como blob
    try:
        storage.upload_blob(container=container, file_path=file_path)
    except FileExistsError:
        print(f"[ℹ️] Blob '{blob_name}' already exists in container '{container}'. Skipping upload.")
    except Exception as e:
        print(f"[⚠️] Error uploading blob: {e}")

    # Listar blobs
    try:
        storage.list_blobs(container=container)
    except Exception as e:
        print(f"[⚠️] Error listing blobs: {e}")

    # Asegurar que la carpeta de destino exista
    os.makedirs(dest_path, exist_ok=True)

    # Descargar el blob
    try:
        storage.download_blob(container=container, blob_name=blob_name, destination=dest_path)
    except Exception as e:
        print(f"[⚠️] Error downloading blob: {e}")

    # Mostrar metadata
    try:
        storage.get_blob_metadata(container=container, blob_name=blob_name)
    except Exception as e:
        print(f"[⚠️] Error retrieving metadata: {e}")


if __name__ == "__main__":
    main()
