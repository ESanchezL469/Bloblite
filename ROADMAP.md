# 🚀 BlobLite Roadmap (v1.1+)

**Objetivo:** Hacer que desarrolladores, estudiantes y usuarios no técnicos puedan aprender Azure Blob Storage _sin necesidad de cuenta, tarjeta ni internet_, usando solo su máquina local.

---

## ✅ Versión 1.0 (Liberada)
- [x] Crear contenedores locales
- [x] Subir y descargar blobs
- [x] Listar contenedores y blobs
- [x] Guardar metadata local (JSON)
- [x] CLI funcional con argparse
- [x] CI multiplataforma (Ubuntu, macOS, Windows)
- [x] Compatibilidad con Python 3.10 – 3.12

---

## 🛠️ Prioridad Alta (v1.1)
- [ ] `blob delete`: borrar blobs individuales
- [ ] `container delete`: eliminar contenedores vacíos
- [ ] `blob info`: mostrar metadata en CLI
- [ ] Validación de nombres: sin espacios, longitud máx
- [ ] `--content-type` automático con `mimetypes`
- [ ] Versionado básico: `filename__v1.txt`, `__v2`, etc.

---

## 🧪 Prioridad Media (v1.2)
- [ ] Renombrado de blobs
- [ ] Copia de blobs entre contenedores
- [ ] TTL (expiración) de blobs en metadata
- [ ] Registro de logs simples (`.bloblite.log`)
- [ ] Protección simple de concurrencia (`filelock`)

---

## 🔭 Opcionales / Simulados (v1.3+)
- [ ] Simular carpetas virtuales (`folder1/blob.txt`)
- [ ] Tiers de almacenamiento en metadata (`hot`, `cool`)
- [ ] CLI más amigable con colores (`rich`)

---

## 🚫 No incluir (por ahora)
- Autenticación real / roles
- SAS tokens o URLs públicas
- ACLs avanzadas
- REST API o servidor HTTP
- Integraciones externas (EventGrid, Azure Monitor)

---

## 🎯 Visión del proyecto
**BlobLite** busca acercar Azure a la comunidad técnica y no técnica de forma gratuita, local y offline. Es una herramienta educativa, didáctica y funcional para prototipado, cursos, notebooks y pruebas.

---

Contribuciones, issues y forks son bienvenidos. 💙