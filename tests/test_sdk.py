from pathlib import Path

from bloblite.sdk.blob_service_client import BlobServiceClient


def test_sdk_blob_workflow(tmp_path: Path) -> None:

    # Inicializa SDK con almacenamiento temporal
    client = BlobServiceClient(storage_root=tmp_path)
    container = client.get_container_client("clientes")

    # Crea contenedor
    container.create_container()
    assert "clientes" in client.list_containers()

    # Crea archivo temporal
    file = tmp_path / "archivo.csv"
    file.write_text("id,name\n1,Santiago")

    # Sube archivo
    container.upload_blob(file)
    blob_path = tmp_path / "clientes" / "archivo.csv"
    assert blob_path.exists()

    # Metadata
    metadata = container.get_blob_metadata("archivo.csv")
    print(metadata)
    assert metadata["name"] == "archivo.csv"
    assert metadata["size"] > 0

    # Descarga
    out_dir = tmp_path / "descargas"
    out_dir.mkdir(parents=True, exist_ok=True)
    container.download_blob("archivo.csv", out_dir)
    assert (out_dir / "archivo.csv").exists()


def test_container_client_list_blobs(capsys, tmp_path):
    client = BlobServiceClient(storage_root=tmp_path)
    container = client.get_container_client("clientes")
    container.create_container()

    # Upload un archivo para que la lista no esté vacía
    dummy_file = tmp_path / "archivo.csv"
    dummy_file.write_text("id,nombre\n1,Juan")

    container.upload_blob(str(dummy_file))

    container.list_blobs()
    output = capsys.readouterr().out
    assert "archivo.csv" in output
    assert "blob(s)" in output
