import os
import subprocess
import sys
from pathlib import Path


def run_cli(
    args: list[str], env: dict[str, str], cwd: Path
) -> subprocess.CompletedProcess:
    """
    Ejecuta el CLI con argumentos y entorno personalizados.
    """
    env = {
        **env,
        "PYTHONPATH": str(cwd / "src"),  # ✅ esta línea es CRUCIAL
    }

    return subprocess.run(
        [sys.executable, "-m", "bloblite.cli"] + args,
        env=env,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_full_workflow(tmp_path: Path):
    env = {
        **os.environ,
        "BLOBLITE_ROOT": str(tmp_path),
    }

    project_root = Path(__file__).resolve().parent.parent

    # 1. Crear contenedor
    result = run_cli(["container", "create", "clientes"], env, project_root)
    print(result)
    assert "created" in result.stdout.lower(), result.stdout + result.stderr

    # 2. Crear archivo de prueba
    test_file = tmp_path / "archivo.csv"
    test_file.write_text("id,nombre\n1,Ana\n2,Luis\n")

    # 3. Subir archivo
    result = run_cli(
        ["blob", "upload", "--container", "clientes", "--file", str(test_file)],
        env,
        project_root,
    )
    assert "uploaded" in result.stdout.lower(), result.stdout + result.stderr

    # 4. Listar blobs
    result = run_cli(["blob", "list", "--container", "clientes"], env, project_root)
    assert "archivo.csv" in result.stdout, result.stdout + result.stderr

    # 5. Mostrar metadata
    result = run_cli(
        ["blob", "show-metadata", "--container", "clientes", "--name", "archivo.csv"],
        env,
        project_root,
    )
    assert "archivo.csv" in result.stdout, result.stdout + result.stderr

    # 6. Descargar archivo
    out_dir = tmp_path / "descargas"
    out_dir.mkdir()
    result = run_cli(
        [
            "blob",
            "download",
            "--container",
            "clientes",
            "--name",
            "archivo.csv",
            "--dest",
            str(out_dir),
        ],
        env,
        project_root,
    )
    assert (out_dir / "archivo.csv").exists(), "Archivo no descargado correctamente"
    assert "downloaded" in result.stdout.lower()


# def test_cli_blob_show_metadata_missing(monkeypatch, tmp_path):
#     monkeypatch.setenv("BLOBLITE_ROOT", str(tmp_path))
#     subprocess.run(
#         [sys.executable, "src/bloblite/cli.py", "container", "create", "clientes"],
#         check=True,
#     )
#     result = subprocess.run(
#         [
#             sys.executable,
#             "src/bloblite/cli.py",
#             "blob",
#             "show-metadata",
#             "--container",
#             "clientes",
#             "--name",
#             "missing.csv",
#         ],
#         capture_output=True,
#         text=True,
#     )
#     assert "not found" in result.stdout or result.returncode == 0


# def test_cli_container_list(monkeypatch, tmp_path):
#     monkeypatch.setenv("BLOBLITE_ROOT", str(tmp_path))

#     # Primero crea un contenedor para que "list" tenga salida
#     subprocess.run(
#         [sys.executable, "src/bloblite/cli.py", "container", "create", "clientes"],
#         check=True,
#     )

#     # Luego lista los contenedores
#     result = subprocess.run(
#         [sys.executable, "src/bloblite/cli.py", "container", "list"],
#         capture_output=True,
#         text=True,
#     )

#     assert "clientes" in result.stdout
#     assert "container(s)" in result.stdout
