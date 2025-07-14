import builtins
import json
from pathlib import Path
from unittest.mock import mock_open, patch
from bloblite.storage import Storage


def test_storage_permission_error_on_init(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        captured = capsys.readouterr()
        assert "Warning: Cannot create or access storage" in captured.out
        assert storage.base_path is None


def test_create_container_already_exists(capsys, storage):
    storage.create_container("clientes")
    storage.create_container("clientes")
    output = capsys.readouterr().out

    assert "already exists" in output


def test_create_container_without_storage(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        storage.create_container("prueba")
        captured = capsys.readouterr()
        assert "Storage not initialized." in captured.out


def test_create_container_without_permissions(capsys, storage):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage.create_container("fail")
        captured = capsys.readouterr()
        assert "Cannot create container" in captured.out


def test_list_containers_empty(capsys, storage):
    storage.list_containers()
    captured = capsys.readouterr()
    assert "No exists containers" in captured.out


def test_list_containers_without_storage(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        result = storage.list_containers()
        captured = capsys.readouterr()
        assert "Storage not initialized. Cannot list containers." in captured.out
        assert result == []


def test_list_containers_permission_error(tmp_path, capsys):
    storage = Storage(base_path=tmp_path)

    with patch.object(Path, "iterdir", side_effect=PermissionError):
        result = storage.list_containers()
        captured = capsys.readouterr()
        assert "Cannot access containers" in captured.out
        assert result == []


def test_upload_blob_twice_skips_duplicate(tmp_path, storage):
    storage.create_container("clientes")
    archivo = tmp_path / "archivo.csv"
    archivo.write_text("id,nombre\n1,Ana")
    storage.upload_blob("clientes", str(archivo))
    storage.upload_blob("clientes", str(archivo))  # No debe duplicar
    blobs = list((storage.base_path / "clientes").glob("archivo.csv"))
    assert len(blobs) == 1


def test_upload_blob_container_not_found(capsys, tmp_path, storage):
    dummy_file = tmp_path / "archivo.csv"
    dummy_file.write_text("id,nombre\n1,Juan")

    storage.upload_blob(container="clientes", file_path=str(dummy_file))
    output = capsys.readouterr().out
    assert "does not exist" in output


def test_upload_blob_file_not_found(capsys, storage):
    storage.create_container("clientes")

    storage.upload_blob(container="clientes", file_path="no_existe.csv")
    output = capsys.readouterr().out
    assert "not found" in output


def test_upload_blob_already_exists(capsys, tmp_path, storage):
    storage.create_container("clientes")

    # Crear archivo y subirlo una vez
    archivo = tmp_path / "archivo.csv"
    archivo.write_text("data")
    storage.upload_blob(container="clientes", file_path=str(archivo))

    # Segundo intento
    storage.upload_blob(container="clientes", file_path=str(archivo))
    output = capsys.readouterr().out
    assert "already exists" in output


def test_upload_blob_write_metadata_fails(tmp_path, capsys):
    storage = Storage(base_path=tmp_path)
    container = tmp_path / "c1"
    container.mkdir()
    source = tmp_path / "test.txt"
    source.write_text("hello")

    metadata_file = container / "test.metadata.json"
    real_open = builtins.open  # Guardamos referencia al open original

    def selective_open(path, *args, **kwargs):
        if str(path) == str(metadata_file):
            raise PermissionError("Cannot write metadata")
        return real_open(path, *args, **kwargs)

    with patch("builtins.open", side_effect=selective_open):
        storage.upload_blob("c1", str(source))
        captured = capsys.readouterr()

    assert "[alert] Failed to write metadata for 'test.txt'." in captured.out


def test_upload_blob_without_storage(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        storage.upload_blob(container="test", file_path="data.csv")
        captured = capsys.readouterr()
        assert "Storage not initialized. Cannot upload." in captured.out


def test_upload_blob_metadata_write_failure(tmp_path, capsys):
    storage = Storage(base_path=tmp_path)
    container = tmp_path / "mycontainer"
    container.mkdir()

    test_file = tmp_path / "file.txt"
    test_file.write_text("sample")

    metadata_file = container / "file.metadata.json"

    real_open = builtins.open

    def selective_open(path, *args, **kwargs):
        if str(path) == str(metadata_file):
            raise PermissionError("Simulated metadata write failure")
        return real_open(path, *args, **kwargs)

    with patch("builtins.open", side_effect=selective_open):
        storage.upload_blob("mycontainer", str(test_file))
        captured = capsys.readouterr()

    assert "Failed to write metadata for 'file.txt'." in captured.out


def test_list_blobs_empty_container(capsys, storage):
    storage.create_container("clientes")
    storage.list_blobs("clientes")
    captured = capsys.readouterr()
    assert "is empty" in captured.out


def test_list_blobs_container_not_found(capsys, storage):
    blobs = storage.list_blobs(container="inexistente")
    output = capsys.readouterr().out

    assert blobs == []
    assert "does not exist" in output


def test_list_blobs_without_storage(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        result = storage.list_blobs("prueba")
        captured = capsys.readouterr()
        assert "Storage not initialized. Cannot list blobs." in captured.out
        assert result == []


def test_list_blobs_permission_error(tmp_path, capsys):
    storage = Storage(base_path=tmp_path)
    (tmp_path / "c1").mkdir()

    with patch.object(Path, "iterdir", side_effect=PermissionError):
        result = storage.list_blobs("c1")
        captured = capsys.readouterr()
        assert "Cannot access files in container" in captured.out
        assert result == []


def test_download_blob_not_exist(tmp_path, storage):
    storage.create_container("clientes")
    storage.download_blob("clientes", "no_existe.csv", str(tmp_path))
    assert not (tmp_path / "no_existe.csv").exists()


def test_download_blobs_without_storage(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        storage.download_blob("prueba", "data.csv", "ext")
        captured = capsys.readouterr()
        assert "Storage not initialized. Cannot download." in captured.out


def test_download_blob_no_permission(tmp_path, capsys):
    storage = Storage(base_path=tmp_path)
    container = tmp_path / "c1"
    container.mkdir()
    blob = container / "blob.txt"
    blob.write_text("data")

    with patch("shutil.copy2", side_effect=PermissionError):
        storage.download_blob("c1", "blob.txt", str(tmp_path / "dest.txt"))
        captured = capsys.readouterr()
        assert "Cannot write blob" in captured.out


def test_metadata_file_created(tmp_path, storage):
    storage.create_container("clientes")
    archivo = tmp_path / "data.csv"
    archivo.write_text("1,2")
    storage.upload_blob("clientes", str(archivo))
    meta = storage.base_path / "clientes" / "data.metadata.json"
    assert meta.exists()
    contenido = json.loads(meta.read_text())
    assert contenido["name"] == "data.csv"


def test_get_blob_metadata_not_found(storage):
    storage.create_container("clientes")
    result = storage.get_blob_metadata("clientes", "missing.csv")
    assert result is None


def test_get_blob_metadata_without_storage(capsys):
    with patch.object(Path, "mkdir", side_effect=PermissionError):
        storage = Storage()
        result = storage.get_blob_metadata("prueba", "data.csv")
        captured = capsys.readouterr()
        assert "Storage not initialized. Cannot get metadata." in captured.out
        assert None == result


def test_get_blob_metadata_permission_error(tmp_path, capsys):
    storage = Storage(base_path=tmp_path)
    c = tmp_path / "c1"
    c.mkdir()
    (c / "file.metadata.json").write_text('{"a": 1}')

    with patch("builtins.open", side_effect=PermissionError):
        metadata = storage.get_blob_metadata("c1", "file.txt")
        captured = capsys.readouterr()
        assert "Cannot read metadata" in captured.out
        assert metadata is None
