from pathlib import Path

# ============================================================
# DIRECTORIO RAÍZ DEL PROYECTO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# CONFIGURACIÓN DEL ANÁLISIS
# ============================================================

# IMPORTANTE:
#
# Los archivos se indican MANUALMENTE.
#
# No se va a descargar automáticamente todos los EDF disponibles para el paciente.
# 
# Para agregar o quitar archivos solamente hay que modificar la lista ARCHIVOS.
# 
# Ejemplo:
#
# ARCHIVOS = [
#     "chb04_05.edf",
#     "chb04_08.edf",
#     "chb04_28.edf",
# ]

PACIENTE = "chb04"
ARCHIVOS = ["chb04_05.edf",  "chb04_08.edf", "chb04_28.edf"]

# Margen temporal que se agregará antes y después de cada crisis [s].
# 
# Por ejemplo:
#
# Crisis: 1000 - 1100 s
# Margen: 60 s
#
# Ventana extraída:
#
# 940 - 1160 s

MARGEN = 60

# Base de datos CHB-MIT en PhysioNet
BASE_URL = "https://physionet.org/files/chbmit/1.0.0"

# ============================================================
# DIRECTORIOS DE DATOS
# ============================================================

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CSV_DIR = DATA_DIR / "csv"

# ============================================================
# DIRECTORIOS DE RESULTADOS
# ============================================================

RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
MAT_DIR = RESULTS_DIR / "mat"
METADATA_DIR = RESULTS_DIR / "metadata"

# ============================================================
# DIRECTORIOS ESPECÍFICOS DEL PACIENTE
# ============================================================

# Cada paciente tendrá sus propios directorios. 
# Esto permite trabajar posteriormente con:
#
# chb01
# chb02
# chb03
# chb04
# ...
#
# sin mezclar los archivos.

RAW_PATIENT_DIR = RAW_DIR / PACIENTE
CSV_PATIENT_DIR = CSV_DIR / PACIENTE
MAT_PATIENT_DIR = MAT_DIR / PACIENTE
FIGURES_PATIENT_DIR = FIGURES_DIR / PACIENTE
METADATA_PATIENT_DIR = METADATA_DIR / PACIENTE

# ============================================================
# CREAR DIRECTORIOS SI NO EXISTEN
# ============================================================

RAW_PATIENT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATIENT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_PATIENT_DIR.mkdir(parents=True, exist_ok=True)
MAT_PATIENT_DIR.mkdir(parents=True, exist_ok=True)
METADATA_PATIENT_DIR.mkdir(parents=True, exist_ok=True)