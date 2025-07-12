# ☁️ BlobLite

**BlobLite** is a local, lightweight simulation of Azure Blob Storage — ideal for developers and data engineers who want to experiment, learn or prototype **without needing an Azure subscription**.

---

## 🚀 Features

- Create and manage containers locally
- Upload, list, download blobs with realistic metadata
- Azure-like CLI for seamless migration and learning
- No dependencies, no external services
- Built to last, with clean architecture and good practices

---

## ⚙️ Requirements

- Python 3.8+
- Linux (initial support; Windows/Mac coming soon)

---

## 🛠 Installation (local development)

```bash
git clone https://github.com/youruser/bloblite.git
cd bloblite
make setup
```

---

## 🧪 CLI Usage

```bash
# Create a container
python bloblite/cli.py container create clientes

# List containers
python bloblite/cli.py container list

# Upload a file to a container
python bloblite/cli.py blob upload --container clientes --file ./data.csv

# List blobs inside a container
python bloblite/cli.py blob list --container clientes

# Download a blob to a specific location
python bloblite/cli.py blob download --container clientes --name data.csv --dest ./downloads/

# Show blob metadata
python bloblite/cli.py blob show-metadata --container clientes --name data.csv
```

---

## 📁 File Storage

All containers and blobs are stored under:

```
~/.bloblite_storage/<container>/<blob>
```

> The base path is automatically created per user in their home directory.

---

## 📂 Project Structure

```
bloblite/
├── bloblite/              ← Core library (container/blob logic)
│   ├── cli.py             ← Azure-style CLI
│   ├── storage.py         ← Storage logic
│   └── __init__.py
├── examples/
│   └── main.py            ← Programmatic example usage
├── tests/                 ← (Coming soon)
├── requirements-dev.txt
├── pyproject.toml
├── Makefile
└── README.md
```

---

## 🔜 Roadmap

- [x] CLI with Azure-style subcommands
- [ ] Python SDK (BlobServiceClient, ContainerClient)
- [ ] Windows/Mac support
- [ ] GitHub Actions tests
- [ ] Integration with Azure CLI (`az`)

---


![Tests](https://github.com/ESanchezL469/bloblite/actions/workflows/test.yml/badge.svg)


## 🪪 License

MIT — feel free to fork, extend, or contribute.

Made with ❤️ by Santiago Sánchez.