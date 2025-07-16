# ☁️ BlobLite

**BlobLite** is a local, lightweight simulation of Azure Blob Storage — ideal for developers, data engineers, and learners who want to experiment or prototype **without an Azure subscription**.

---

![Tests](https://github.com/ESanchezL469/bloblite/actions/workflows/test.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

## 🚀 Features

- Create and manage containers locally (mimicking Azure Blob Storage)
- Upload, list, download blobs with realistic metadata handling
- Azure-like CLI for seamless learning and migration
- Clean code, full test coverage, no dependencies
- Built to last — simple, modular, and transparent

---


## ⚙️ Requirements

- Python 3.10+
- Linux (initial support) — *Windows and macOS support coming soon*

---


## 🛠️ Installation (for development)

```bash
git clone https://github.com/ESanchezL469/bloblite.git
cd bloblite
make setup
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate  # Windows (PowerShell)
```

---


## 🧪 CLI Usage

```bash
# Create a container
python -m bloblite.cli container create clientes

# List containers
python -m bloblite.cli container list

# Upload a file to a container
python -m bloblite.cli blob upload --container clientes --file ./data.csv

# List blobs inside a container
python -m bloblite.cli blob list --container clientes

# Download a blob to a specific location
python -m bloblite.cli blob download --container clientes --name data.csv --dest ./downloads/

# Show blob metadata
python -m bloblite.cli blob show-metadata --container clientes --name data.csv
```

---


## 🧩 Python SDK Usage

```python
from bloblite.sdk.blob_service_client import BlobServiceClient

client = BlobServiceClient()
container = client.get_container_client("clientes")
container.create_container()
container.upload_blob("archivo.csv")
blobs = container.list_blobs()
container.download_blob("archivo.csv", "downloads/")
```

---


## 📁 Local File Storage Path

BlobLite stores all blobs and containers under:

```
~/.bloblite_storage/<container>/<blob>
```

> This path is automatically created in the user's home directory.  
> You can override it using the `BLOBLITE_ROOT` environment variable.

---


## 📂 Project Structure

```
bloblite/
├── src/bloblite/          ← Core library (SDK, CLI, storage)
│   ├── cli.py             ← CLI entry point
│   ├── sdk/               ← Azure-like Python SDK
│   │   ├── blob_service_client.py
│   │   └── container_client.py
│   ├── storage.py         ← Local storage engine
│   └── __init__.py
├── examples/              ← Usage examples
│   └── main.py
├── tests/                 ← Full test suite (90%+ coverage)
├── .github/               ← GitHub Actions CI config
│   └── workflows/
│       └── test.yml
├── requirements-dev.txt   ← Dev dependencies only
├── pyproject.toml         ← Project configuration (PEP 621)
├── Makefile               ← Developer helper commands
└── README.md              ← This file
```

---


## ✅ Test Coverage

- 90%+ test coverage via `pytest` + `coverage`
- CLI, SDK and storage logic fully tested in isolation and integration


---


## 🔭 Roadmap

- [x] Azure-style CLI interface
- [x] Python SDK (BlobServiceClient, ContainerClient)
- [x] Linux compatibility and CI
- [x] Full unit + integration test coverage
- [ ] Windows/macOS support
- [ ] Integration with Azure CLI (`az`)
- [ ] Minimal Web UI for interaction

---


## 🪪 License

**MIT** — free to use, share and modify.

Crafted with ❤️ by Santiago Sánchez — [@ESanchezL469](https://github.com/ESanchezL469)