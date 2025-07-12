import os
import json
import time
import shutil
import unittest
from pathlib import Path
from datetime import datetime
from bloblite.storage import (
    BASE_PATH,
    create_container,
    list_containers,
    upload_blob,
    list_blobs,
    download_blob,
    get_blob_metadata
)

class TestBlobLiteStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial nuclear para todas las pruebas"""
        cls._nuclear_cleanup()
        cls.test_files_dir = Path(os.getcwd()) / "test_temp_files"
        cls.test_files_dir.mkdir(exist_ok=True)
        
        # Crear archivos de prueba reutilizables
        cls.sample_files = {
            "text": cls.test_files_dir / "sample.txt",
            "json": cls.test_files_dir / "data.json",
            "binary": cls.test_files_dir / "binary.bin"
        }
        
        cls.sample_files["text"].write_text("Contenido de texto de prueba")
        cls.sample_files["json"].write_text(json.dumps({"key": "value"}))
        cls.sample_files["binary"].write_bytes(b'\x00\x01\x02\x03')

    @classmethod
    def tearDownClass(cls):
        """Limpieza final de todo"""
        cls._nuclear_cleanup()
        shutil.rmtree(cls.test_files_dir, ignore_errors=True)

    @classmethod
    def _nuclear_cleanup(cls):
        """Eliminación recursiva con múltiples fallbacks"""
        if not BASE_PATH.exists():
            return

        for attempt in range(3):
            try:
                for item in BASE_PATH.iterdir():
                    try:
                        shutil.rmtree(item) if item.is_dir() else item.unlink()
                    except:
                        pass
                if not list(BASE_PATH.iterdir()):
                    break
                time.sleep(0.1)
            except:
                pass

    def setUp(self):
        """Preparación indestructible para cada test"""
        self._nuclear_cleanup()
        BASE_PATH.mkdir(parents=True, exist_ok=True)
        self.current_container = f"container_{os.getpid()}_{time.time_ns()}"
        create_container(self.current_container)

    # --------------------------
    # Pruebas para contenedores
    # --------------------------
    def test_container_operations(self):
        containers_before = list_containers()
        self.assertIn(self.current_container, containers_before)
        
        with self.assertRaises(ValueError):
            create_container(self.current_container)

    def test_list_containers(self):
        new_container = f"extra_container_{time.time_ns()}"
        create_container(new_container)
        
        containers = list_containers()
        self.assertGreaterEqual(len(containers), 2)
        self.assertIn(self.current_container, containers)
        self.assertIn(new_container, containers)

    # --------------------------
    # Pruebas para blobs
    # --------------------------
    def test_upload_and_list_blobs(self):
        # Subir archivo de texto
        upload_blob(self.current_container, str(self.sample_files["text"]))
        
        blobs = list_blobs(self.current_container)
        self.assertEqual(blobs, [self.sample_files["text"].name])
        
        # Subir archivo JSON
        upload_blob(self.current_container, str(self.sample_files["json"]))
        blobs = list_blobs(self.current_container)
        self.assertEqual(len(blobs), 2)
        self.assertIn(self.sample_files["json"].name, blobs)

    def test_blob_metadata(self):
        upload_blob(self.current_container, str(self.sample_files["json"]))
        
        metadata = get_blob_metadata(self.current_container, self.sample_files["json"].name)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["name"], self.sample_files["json"].name)
        self.assertEqual(metadata["content_type"], "application/octet-stream")
        self.assertIn("uploaded_at", metadata)
        
        # Verificar metadata para archivo binario
        upload_blob(self.current_container, str(self.sample_files["binary"]))
        binary_metadata = get_blob_metadata(self.current_container, self.sample_files["binary"].name)
        self.assertEqual(binary_metadata["size"], 4)

    def test_download_blob(self):
        upload_blob(self.current_container, str(self.sample_files["text"]))
        
        download_path = self.test_files_dir / "downloaded.txt"
        download_blob(self.current_container, self.sample_files["text"].name, str(download_path))
        
        self.assertTrue(download_path.exists())
        self.assertEqual(
            download_path.read_text(),
            self.sample_files["text"].read_text()
        )
        download_path.unlink()

    # --------------------------
    # Pruebas de errores
    # --------------------------
    def test_upload_to_nonexistent_container(self):
        with self.assertRaises(FileNotFoundError):
            upload_blob("container_inexistente", str(self.sample_files["text"]))

    def test_download_nonexistent_blob(self):
        with self.assertRaises(FileNotFoundError):
            download_blob(
                self.current_container,
                "archivo_que_no_existe.txt",
                str(self.test_files_dir / "no_importa.txt")
            )

    def test_metadata_for_nonexistent_blob(self):
        metadata = get_blob_metadata(
            self.current_container,
            "archivo_que_no_existe.txt"
        )
        self.assertIsNone(metadata)

    # --------------------------
    # Prueba de estrés
    # --------------------------
    def test_repeated_operations(self):
        """Prueba de ejecución múltiple consecutiva"""
        for i in range(5):
            container_name = f"stress_test_{i}"
            create_container(container_name)
            
            # Subir todos los tipos de archivo
            for file_type, file_path in self.sample_files.items():
                upload_blob(container_name, str(file_path))
                
                # Verificar metadata
                metadata = get_blob_metadata(container_name, file_path.name)
                self.assertEqual(metadata["size"], os.path.getsize(file_path))
                
                # Descargar y verificar
                download_path = self.test_files_dir / f"temp_{file_type}_{i}"
                download_blob(container_name, file_path.name, str(download_path))
                self.assertEqual(
                    download_path.read_bytes() if file_type == "binary" else download_path.read_text(),
                    file_path.read_bytes() if file_type == "binary" else file_path.read_text()
                )
                download_path.unlink()

if __name__ == "__main__":
    unittest.main(failfast=True, verbosity=2)