import os
import subprocess
from pathlib import Path


def run_cli(args: list[str], env: dict[str, str], cwd: Path) -> subprocess.CompletedProcess:
    """
    Ejecuta el CLI con argumentos y entorno personalizados.
    """
    cli_path = cwd / "bloblite" / "cli.py"
    return subprocess.run(
        ["python", str(cli_path)] + args,
        env=env,
        cwd=cwd,
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
    assert "created" in result.stdout.lower(), result.stdout + result.stderr

    # 2. Crear archivo de prueba
    test_file = tmp_path / "archivo.csv"
    test_file.write_text("id,nombre\n1,Ana\n2,Luis\n")

    # 3. Subir archivo
    result = run_cli(["blob", "upload", "--container", "clientes", "--file", str(test_file)], env, project_root)
    assert "uploaded" in result.stdout.lower(), result.stdout + result.stderr

    # 4. Listar blobs
    result = run_cli(["blob", "list", "--container", "clientes"], env, project_root)
    assert "archivo.csv" in result.stdout, result.stdout + result.stderr

    # 5. Mostrar metadata
    result = run_cli(["blob", "show-metadata", "--container", "clientes", "--name", "archivo.csv"], env, project_root)
    assert "archivo.csv" in result.stdout, result.stdout + result.stderr

    # 6. Descargar archivo
    out_dir = tmp_path / "descargas"
    out_dir.mkdir()
    result = run_cli(
        ["blob", "download", "--container", "clientes", "--name", "archivo.csv", "--dest", str(out_dir)],
        env,
        project_root,
    )
    assert (out_dir / "archivo.csv").exists(), "Archivo no descargado correctamente"
    assert "downloaded" in result.stdout.lower()
