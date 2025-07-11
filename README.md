# 📦 BlobLite - Local Azure Blob Storage Simulator

**BlobLite** is a real, production-grade tool that simulates [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/) using only your local filesystem.  
It’s designed to help developers, students, and data engineers **learn and test Azure Blob workflows** without needing a cloud subscription.

> ⚠️ Currently supports **Linux only** (e.g., Ubuntu, Linux Mint). Compatibility with macOS and Windows will come in future versions.

---

## 🚀 What Does BlobLite Do?

BlobLite allows you to:

- Create containers (like Azure)
- Upload and download blobs (files)
- View metadata for each blob
- List containers and blobs
- Store everything persistently in your filesystem (not in memory)

### 🧱 BlobLite Structure

BlobLite stores everything under:

```
~/.bloblite_storage/
```

Each container is a folder inside that path.

Example:

```
~/.bloblite_storage/demo-container/
├── demo_data.txt
├── demo_data.metadata.json
```

To view it in your file manager:
- Go to your home folder (`/home/youruser/`)
- Press `Ctrl + H` to show hidden folders

---

## ⚙️ Features in Phase 1 (Current Version)

| Feature           | Status    |
|------------------|-----------|
| Create container | ✅ Done   |
| Upload blob      | ✅ Done   |
| Download blob    | ✅ Done   |
| List containers  | ✅ Done   |
| List blobs       | ✅ Done   |
| View metadata    | ✅ Done   |
| CLI interface    | ✅ Done   |
| Python SDK       | 🔜 Next   |
| Docker image     | 🔜 Later  |
| Web API (FastAPI)| 🔜 Later  |

---

## 🖥️ How to Use

### ▶️ Run from CLI

```bash
python bloblite/cli.py create mycontainer
python bloblite/cli.py upload mycontainer ./example.csv
python bloblite/cli.py list mycontainer
python bloblite/cli.py download mycontainer example.csv ./downloads/
python bloblite/cli.py metadata mycontainer example.csv
```

### ▶️ Run from Code

```bash
python main.py
```

This will:
- Create a test container and file
- Upload it
- List contents and metadata
- Download it to a local folder (`./descargas/`)
- Handle errors gracefully

---

## 📂 Where Does It Store Things?

BlobLite stores all your containers and files here:

```
~/.bloblite_storage/
```

This is your **home directory** (the `~` symbol). The folder is hidden.

To check manually:

```bash
ls -la ~/.bloblite_storage
```

---

## 📌 Requirements

- Python 3.8 or higher
- Linux OS (Ubuntu, Mint, Debian, etc.)

No external libraries or cloud account required.

---

## 📅 Roadmap

- [x] Phase 1: Local filesystem core + CLI
- [ ] Phase 2: Python SDK (`from bloblite import BlobClient`)
- [ ] Phase 3: REST API with FastAPI
- [ ] Phase 4: Docker support for isolated usage
- [ ] Phase 5: Cross-platform support (macOS, Windows)

---

## 🤝 Community-Oriented

BlobLite is designed with ❤️ to help make Azure Blob Storage accessible for:

- Students and bootcampers
- Developers with limited internet/cloud access
- Engineers preparing for Azure certification
- Anyone who wants a **real working tool**, not just mock-ups

---

## 📄 License

MIT License — use freely, improve freely, contribute freely.