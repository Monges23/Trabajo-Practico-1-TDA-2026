# TP1 - TDA - Echevarria: Instrucciones de Ejecución

Guía para configurar el entorno virtual, instalar las dependencias con el solver CBC y ejecutar los programas.

---

## 1. Requisitos Previos

* **Python:** `>= 3.10`
* **Instalador de paquetes:** `pip` o `uv`

---

## 2. Gestión de Dependencias y Entorno Virtual

Elegí una de las dos opciones para preparar el entorno:

### Opción A: Usando `uv` (Recomendado)

#### Linux / macOS:
```bash
# 1. Instalar uv (si no está instalado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Crear y activar el entorno virtual
uv venv
source .venv/bin/activate

# 3. Instalar PuLP con soporte para CBC
uv pip install "pulp==2.9.0"
```

#### Windows:
```powershell
# 1. Instalar uv (si no está instalado)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Crear y activar el entorno virtual
uv venv
.venv\Scripts\activate

# 3. Instalar PuLP con soporte para CBC
uv pip install "pulp==2.9.0"
```

---

### Opción B: Usando `pip` estándar

#### Linux / macOS:
```bash
# 1. Asegurar pip actualizado
python3 -m ensurepip --upgrade

# 2. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar PuLP con soporte para CBC
pip install "pulp==2.9.0"
```

#### Windows:
```powershell
# 1. Asegurar pip actualizado
py -m ensurepip --upgrade

# 2. Crear y activar el entorno virtual
py -m venv .venv
.venv\Scripts\activate

# 3. Instalar PuLP con soporte para CBC
pip install "pulp==2.9.0"
```

---

## 3. Ejecución del Código

Asegurate de tener el entorno virtual activo antes de ejecutar los comandos:
```bash
source .venv/bin/activate
```

### Paso 1: Generar una instancia de prueba

Crea un archivo con una instancia aleatoria del problema de tamaño $n$ (por ejemplo, $n = 20$):

```bash
python crear_mochila.py 20
```

---

### Paso 2: Resolver el problema

Ejecutar el script principal sobre la instancia generada:

```bash
python mochila.py
```
