"""
main.py

Demostración segura del uso de BlobLite desde código Python.
Compatible con múltiples ejecuciones sin errores fatales.
"""

from pathlib import Path
from bloblite.storage import (
    create_container,
    list_containers,
    upload_blob,
    list_blobs,
    download_blob,
    get_blob_metadata,
)


def demo() -> None:
    """Demostración completa de funcionalidades básicas."""
    container = "demo-container"
    test_file = "demo_data.txt"
    download_dir = Path("descargas")
    download_dir.mkdir(exist_ok=True)

    # Crear archivo de prueba
    if not Path(test_file).exists():
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hola desde BlobLite!\n")

    # Crear contenedor si no existe
    print(f"\n➡️  Verificando existencia del contenedor '{container}'...")
    try:
        create_container(container)
    except ValueError:
        print(f"ℹ️  El contenedor '{container}' ya existe. Continuando.")

    # Subir archivo
    print(f"\n⬆️  Subiendo '{test_file}' a '{container}'...")
    try:
        upload_blob(container, test_file)
    except Exception as e:
        print(f"⚠️  No se pudo subir el archivo: {e}")

    # Listar blobs
    print(f"\n📄 Blobs en '{container}':")
    try:
        for blob in list_blobs(container):
            print(f" - {blob}")
    except Exception as e:
        print(f"⚠️  Error al listar blobs: {e}")

    # Ver metadata
    print(f"\nℹ️  Metadata de '{test_file}':")
    meta = get_blob_metadata(container, test_file)
    if meta:
        for k, v in meta.items():
            print(f"   {k}: {v}")
    else:
        print("⚠️  No se encontró metadata.")

    # Descargar blob
    download_path = download_dir / test_file
    print(f"\n⬇️  Descargando '{test_file}' a '{download_path}'...")
    try:
        download_blob(container, test_file, str(download_path))
    except Exception as e:
        print(f"⚠️  Error al descargar archivo: {e}")

    # Listar contenedores
    print("\n📦 Contenedores existentes:")
    for name in list_containers():
        print(f" - {name}")

    print("\n✅ Demo completada sin errores fatales.")


if __name__ == "__main__":
    demo()
