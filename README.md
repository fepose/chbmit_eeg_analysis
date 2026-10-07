# CHB-MIT EEG Analysis

Pipeline en Python para la descarga, validación y preprocesamiento de registros EEG del dataset [CHB-MIT Scalp EEG Database](https://physionet.org/content/chbmit/1.0.0/).

El proyecto permite trabajar de forma reproducible con registros EEG en formato EDF, conservar los canales disponibles, identificar las crisis epilépticas a partir de los archivos `summary` y mantener la trazabilidad entre paciente, registro, información temporal, crisis y resultados.

## Descripción

`chbmit_eeg_analysis` automatiza el preprocesamiento de registros EEG del dataset CHB-MIT.

El pipeline integra las siguientes etapas:

- descarga de archivos EDF;
- validación de los archivos descargados;
- lectura de los registros mediante MNE;
- conservación de los canales EEG disponibles;
- obtención de la frecuencia de muestreo y duración de cada registro;
- lectura de los archivos `summary`;
- identificación de los intervalos de las crisis;
- asociación entre las crisis y los registros EDF;
- preprocesamiento y almacenamiento estructurado de los resultados.

La configuración, descarga, identificación de crisis y ejecución del pipeline se encuentran organizadas en módulos independientes.

# Objetivos

## Objetivo general

Desarrollar un pipeline reproducible para el preprocesamiento de registros EEG del dataset CHB-MIT, manteniendo la relación entre pacientes, archivos EDF, canales EEG, información temporal y crisis epilépticas.

## Objetivos específicos

- Automatizar la descarga y validación de los registros EDF.
- Procesar únicamente los archivos definidos en la configuración.
- Identificar las crisis a partir de los archivos `summary`.
- Conservar los canales EEG disponibles en cada registro.
- Mantener la información temporal y la frecuencia de muestreo de los registros.
- Relacionar los intervalos de las crisis con los registros EEG correspondientes.
- Organizar los datos y resultados de forma estructurada.
- Mantener la trazabilidad de los datos a lo largo del pipeline.
- Facilitar la reutilización de los registros procesados en análisis posteriores.

# Dataset CHB-MIT

El proyecto utiliza el dataset [CHB-MIT Scalp EEG Database](https://physionet.org/content/chbmit/1.0.0/), disponible a través de PhysioNet.

El dataset contiene registros EEG de pacientes con epilepsia en formato EDF, junto con archivos `summary` que proporcionan información sobre los registros y, cuando corresponde, los intervalos temporales de las crisis.

Cada paciente puede disponer de múltiples registros EDF. La relación entre la información del paciente, los archivos `summary` y los registros EEG puede representarse conceptualmente como:

    Paciente
    ├── summary
    ├── registro EDF
    │   ├── canal EEG 1
    │   ├── canal EEG 2
    │   ├── canal EEG 3
    │   └── ...
    ├── otro registro EDF
    │   └── ...
    └── ...

Los archivos `summary` constituyen la fuente utilizada por el pipeline para identificar las crisis asociadas a cada registro EDF.

# Arquitectura del proyecto

La estructura del proyecto separa la configuración, los scripts de ejecución, el código fuente del pipeline, los datos, los resultados y las pruebas.

    chbmit_eeg_analysis/

    ├── config/
    │   ├── __init__.py
    │   └── config.py
    │
    ├── scripts/
    │   ├── __init__.py
    │   └── run_analysis.py
    │
    ├── data/
    │   ├── csv/
    │   ├── processed/
    │   └── raw/
    │
    ├── results/
    │   ├── figures/
    │   ├── mat/
    │   └── metadata/
    │
    ├── src/
    │   └── chbmit/
    │       ├── data/
    │       │   ├── download.py
    │       │   ├── loader.py
    │       │   └── saver.py
    │       │
    │       ├── export/
    │       │   ├── matlab.py
    │       │   └── metadata.py
    │       │
    │       ├── processing/
    │       │   ├── pipeline.py
    │       │   ├── seizures.py
    │       │   └── validation.py
    │       │
    │       └── visualization/
    │           └── plots.py
    │
    ├── tests/
    │   └── __init__.py
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore

## `config/`

Contiene la configuración central del proyecto.

- `config.py`: define las rutas, la URL del dataset, los archivos a procesar y los parámetros generales.
- `__init__.py`: define el directorio como paquete de Python.

## `scripts/`

Contiene los scripts utilizados para ejecutar el proyecto.

- `run_analysis.py`: punto de entrada principal del pipeline.
- `__init__.py`: define el directorio como paquete de Python.

## `data/`

Contiene los datos utilizados durante las diferentes etapas del preprocesamiento.

- `raw/`: almacena los archivos EDF originales descargados desde el dataset CHB-MIT.
- `processed/`: almacena los datos derivados del preprocesamiento de las señales.
- `csv/`: almacena archivos en formato CSV utilizados o generados durante el preprocesamiento.

## `results/`

Contiene los resultados generados por el pipeline, organizados según el tipo de salida.

- `figures/`: contiene las figuras y visualizaciones generadas a partir de las señales preprocesadas.
- `mat/`: contiene los resultados exportados en formato MATLAB (`.mat`).
- `metadata/`: contiene la información descriptiva y de trazabilidad asociada a los registros procesados.

## `src/chbmit/`

Contiene el código fuente principal del proyecto, organizado por funcionalidad.

### `src/chbmit/data/`

Contiene las funciones relacionadas con la gestión de los datos.

- `download.py`: descarga los archivos EDF y otros archivos necesarios desde el dataset CHB-MIT.
- `loader.py`: carga los archivos y señales necesarios para el preprocesamiento.
- `saver.py`: guarda los datos procesados y las señales generadas por el pipeline.

### `src/chbmit/export/`

Contiene las funciones encargadas de exportar los resultados.

- `matlab.py`: exporta señales y resultados en formato MATLAB (`.mat`).
- `metadata.py`: genera y guarda la información de metadata asociada a cada registro procesado.

### `src/chbmit/processing/`

Contiene la lógica principal de preprocesamiento y validación.

- `pipeline.py`: coordina las diferentes etapas del preprocesamiento de cada registro.
- `seizures.py`: obtiene e interpreta la información de las crisis a partir de los archivos `summary`.
- `validation.py`: realiza controles de consistencia sobre los archivos, señales, canales, frecuencia de muestreo, duración y tiempos de las crisis.

### `src/chbmit/visualization/`

Contiene las funciones relacionadas con la visualización de las señales y resultados.

- `plots.py`: genera gráficos y representaciones visuales de las señales EEG y de los resultados del preprocesamiento.

## `tests/`

Contiene las pruebas utilizadas para verificar el correcto funcionamiento de los diferentes componentes del proyecto.

- `__init__.py`: define el directorio como paquete de Python.

## Archivos principales

- `requirements.txt`: contiene las dependencias necesarias para ejecutar el proyecto.
- `README.md`: documentación general del proyecto, su arquitectura, instalación, configuración y uso.
- `.gitignore`: define los archivos y directorios que no deben incluirse en el control de versiones.

# Flujo del pipeline

El preprocesamiento sigue las siguientes etapas:

    Configuración
         │
         ▼
    Lista de archivos
         │
         ▼
    Descarga del EDF
         │
         ▼
    Validación del archivo
         │
         ▼
    Lectura del EDF con MNE
         │
         ├──────────────► Información del registro
         │                ├── canales
         │                ├── frecuencia de muestreo
         │                └── duración
         │
         ▼
    Lectura del `summary`
         │
         ▼
    Identificación de crisis
         │
         ▼
    Asociación temporal con el EDF
         │
         ▼
    Preprocesamiento de las señales
         │
         ▼
    Resultados y metadata

El pipeline mantiene la relación entre el paciente, el archivo EDF, los canales EEG, la información temporal, las crisis y los resultados generados.

# Requisitos

El proyecto requiere:

- Python 3.9
- NumPy
- Pandas
- SciPy
- MNE
- Matplotlib

Las dependencias se encuentran especificadas en `requirements.txt`.

Para instalarlas:

    pip install -r requirements.txt

# Configuración

La configuración central del proyecto se encuentra en:

`config/config.py`

Este archivo concentra los parámetros necesarios para ejecutar el pipeline, incluyendo las rutas de trabajo, la URL base del dataset y la lista de archivos que serán procesados.

Centralizar estos parámetros permite modificar la configuración sin realizar cambios en los módulos del pipeline.

# Archivos a procesar

Los archivos que serán procesados se especifican explícitamente mediante las variables `PACIENTE` y `ARCHIVOS`, definidas en `config/config.py`.

    PACIENTE = "chb04"

    ARCHIVOS = [
        "chb04_05.edf",
        "chb04_08.edf",
        "chb04_28.edf",
    ]

`PACIENTE` identifica al paciente cuyos registros serán procesados, mientras que `ARCHIVOS` contiene los nombres de los archivos EDF seleccionados manualmente.

El pipeline procesa únicamente los registros incluidos en `ARCHIVOS`. No se descargan ni procesan automáticamente todos los archivos disponibles para el paciente en el dataset.

Para agregar o quitar registros, solamente es necesario modificar la lista `ARCHIVOS` en `config/config.py`.

Esta configuración permite controlar de forma explícita y reproducible qué registros participan en cada ejecución del pipeline.


# Descarga de archivos EDF

La descarga de los registros EDF se implementa en:

`scripts/download.py`

El módulo se encarga de:

1. construir la URL correspondiente al registro;
2. crear el directorio de destino cuando es necesario;
3. descargar el archivo EDF;
4. verificar que el archivo exista;
5. validar que el archivo pueda ser abierto correctamente;
6. obtener información básica del registro;
7. informar los errores detectados durante el proceso.

La existencia de un archivo en disco no implica necesariamente que la descarga sea válida. Por este motivo, el pipeline diferencia entre un archivo descargado y un archivo EDF que puede ser leído y utilizado correctamente.

Los archivos originales se conservan sin modificaciones en `data/raw/`.

# Detección de crisis

La identificación de las crisis se implementa en:

`scripts/seizures.py`

El módulo analiza los archivos `summary` asociados a cada paciente y extrae las crisis correspondientes a cada registro EDF.

Para cada crisis se registra:

- archivo EDF;
- número de crisis;
- tiempo de inicio;
- tiempo de finalización.

Por ejemplo:

    Paciente: chb04
    Archivo: chb04_08.edf
    Crisis: 1
    Inicio: 6446 s
    Fin: 6557 s

Los tiempos obtenidos del `summary` se utilizan posteriormente para determinar si el intervalo de la crisis se encuentra disponible dentro del registro EDF correspondiente.

La información original del `summary` se conserva incluso cuando existe una discrepancia entre el intervalo de la crisis y la duración del EDF.

# Canales EEG

El pipeline conserva los canales EEG disponibles en cada archivo EDF y no elimina canales automáticamente.

Los nombres de los canales se obtienen mediante MNE:

    raw.ch_names

Las señales se obtienen mediante:

    raw.get_data()

Los datos se representan como una matriz con dimensiones:

    n_canales × n_muestras

La cantidad y los nombres de los canales dependen de cada registro EDF.

Por ejemplo, un registro puede incluir canales como:

    FP1-F7
    F7-T7
    T7-P7
    P7-O1
    FP1-F3
    F3-C3
    C3-P3
    P3-O1
    FP2-F4
    F4-C4
    C4-P4
    P4-O2

La selección de canales para análisis posteriores puede realizarse en etapas posteriores del preprocesamiento, sin modificar los datos originales.

# Control de consistencia temporal

El pipeline compara los intervalos de las crisis obtenidos del `summary` con la duración real del archivo EDF.

Por ejemplo:

    Crisis indicada en summary: 6446–6557 s
    Duración del EDF local:     2096 s

En este caso, el intervalo de la crisis no se encuentra disponible dentro del EDF local.

Esto no significa que el paciente no haya presentado una crisis. Significa que el `summary` contiene información sobre una crisis cuyo intervalo no está incluido en el registro EDF disponible localmente.

Las posibles causas incluyen:

- archivo truncado;
- descarga incompleta;
- registro parcial;
- archivo incorrecto;
- discrepancia entre los archivos del dataset.

La información del `summary` se conserva y la inconsistencia se registra para evitar eliminar o interpretar incorrectamente una crisis únicamente porque su intervalo no está presente en el EDF local.

# Resultados

Los resultados generados por el pipeline se organizan según el tipo de salida, manteniendo la trazabilidad con el paciente y el registro EDF procesado.

La estructura de resultados es:

    results/

    ├── figures/
    │   └── ...
    │
    ├── mat/
    │   └── ...
    │
    └── metadata/
        └── ...

Los resultados asociados al preprocesamiento se almacenan en directorios separados según su finalidad.

La carpeta `figures/` contiene las figuras y visualizaciones generadas durante el análisis de las señales EEG.

La carpeta `mat/` contiene las señales y resultados exportados en formato MATLAB (`.mat`), cuando corresponde.

La carpeta `metadata/` contiene la información descriptiva y de trazabilidad asociada a los registros procesados, incluyendo información del paciente, archivo EDF, canales, frecuencia de muestreo, duración y datos relacionados con las crisis.

La organización de los resultados permite mantener una separación clara entre las señales y datos exportados, las visualizaciones y la información de metadata generada durante el preprocesamiento.

# Metadata

Cada registro procesado genera información de metadata que permite conservar el contexto del análisis y mantener la trazabilidad entre el paciente, el archivo EDF, las señales EEG y las crisis identificadas.

La metadata se almacena en formato JSON y contiene información general del registro, características de las señales y, cuando corresponde, información detallada de cada crisis y de la ventana temporal utilizada para su preprocesamiento.

Ejemplo:

    {
        "paciente": "chb04",
        "archivo_edf": "chb04_05.edf",
        "frecuencia_muestreo_Hz": 256.0,
        "canales_totales": 23,
        "canales_EEG": 23,
        "canales_EEG_nombres": [
            "FP1-F7",
            "F7-T7",
            "T7-P7",
            "P7-O1",
            "FP1-F3",
            "F3-C3",
            "C3-P3",
            "P3-O1",
            "FP2-F4",
            "F4-C4",
            "C4-P4",
            "P4-O2",
            "FP2-F8",
            "F8-T8",
            "T8-P8-0",
            "P8-O2",
            "FZ-CZ",
            "CZ-PZ",
            "P7-T7",
            "T7-FT9",
            "FT9-FT10",
            "FT10-T8",
            "T8-P8-1"
        ],
        "muestras_totales": 2441216,
        "duracion_total_s": 9536.0,
        "numero_crisis": 1,
        "crisis": [
            {
                "numero": 1,
                "inicio_s": 7804.0,
                "fin_s": 7853.0,
                "duracion_s": 49.0,
                "margen_s": 60.0,
                "ventana_inicio_s": 7744.0,
                "ventana_fin_s": 7913.0,
                "duracion_ventana_s": 169.0,
                "canales": 23,
                "muestras": 43264,
                "forma_matriz": [
                    23,
                    43264
                ],
                "canales_nombres": [
                    "FP1-F7",
                    "F7-T7",
                    "T7-P7",
                    "P7-O1",
                    "FP1-F3",
                    "F3-C3",
                    "C3-P3",
                    "P3-O1",
                    "FP2-F4",
                    "F4-C4",
                    "C4-P4",
                    "P4-O2",
                    "FP2-F8",
                    "F8-T8",
                    "T8-P8-0",
                    "P8-O2",
                    "FZ-CZ",
                    "CZ-PZ",
                    "P7-T7",
                    "T7-FT9",
                    "FT9-FT10",
                    "FT10-T8",
                    "T8-P8-1"
                ]
            }
        ]
    }

La metadata incluye, entre otros, los siguientes campos:

- `paciente`: identificador del paciente.
- `archivo_edf`: nombre del archivo EDF procesado.
- `frecuencia_muestreo_Hz`: frecuencia de muestreo del registro en Hz.
- `canales_totales`: número total de canales presentes en el registro.
- `canales_EEG`: número de canales utilizados como señales EEG.
- `canales_EEG_nombres`: nombres de los canales EEG disponibles.
- `muestras_totales`: número total de muestras del registro.
- `duracion_total_s`: duración total del registro en segundos.
- `numero_crisis`: número de crisis identificadas para el registro.
- `crisis`: información detallada de las crisis asociadas al registro.

Para cada crisis se almacena:

- `numero`: número identificador de la crisis.
- `inicio_s`: tiempo de inicio de la crisis en segundos.
- `fin_s`: tiempo de finalización de la crisis en segundos.
- `duracion_s`: duración de la crisis en segundos.
- `margen_s`: margen temporal utilizado alrededor de la crisis.
- `ventana_inicio_s`: inicio de la ventana temporal extraída.
- `ventana_fin_s`: final de la ventana temporal extraída.
- `duracion_ventana_s`: duración total de la ventana extraída.
- `canales`: número de canales incluidos en la ventana.
- `muestras`: número de muestras correspondientes a la ventana.
- `forma_matriz`: dimensiones de la matriz de señales, expresadas como número de canales y número de muestras.
- `canales_nombres`: nombres de los canales incluidos en la ventana.

La metadata se almacena en la carpeta correspondiente de resultados:

    results/
    └── metadata/
        └── ...

Esta información permite conservar la trazabilidad entre el paciente, el archivo EDF, las características de la adquisición, las señales EEG, las crisis identificadas y las ventanas utilizadas durante el preprocesamiento.

# Manejo de errores

El pipeline registra los errores e inconsistencias que pueden producirse durante las distintas etapas del preprocesamiento.

Entre los casos contemplados se encuentran:

- archivo EDF inexistente;
- error durante la descarga;
- archivo EDF corrupto o incompleto;
- error de lectura con MNE;
- archivo `summary` inexistente o no interpretable;
- crisis fuera de la duración del EDF;
- canal no disponible;
- error durante el preprocesamiento de una señal.

Los errores se registran sin ocultar el problema ni considerar el registro como procesado correctamente cuando una etapa crítica falla.

Las inconsistencias entre el `summary` y el EDF se conservan como información de control de calidad y no se interpretan automáticamente como ausencia de crisis.

# Problemas frecuentes

## `ModuleNotFoundError: No module named 'config'`

Este error puede producirse cuando `run_analysis.py` se ejecuta desde un directorio distinto de la raíz del proyecto o cuando la estructura de directorios no coincide con la arquitectura esperada.

La estructura debe contener:

    chbmit_eeg_analysis/

    ├── config/
    │   ├── __init__.py
    │   └── config.py
    │
    ├── scripts/
    │   ├── __init__.py
    │   └── run_analysis.py
    │
    └── src/
        └── chbmit/
            └── ...

Ejecutar el pipeline desde la raíz del proyecto:

    cd /ruta/al/proyecto/chbmit_eeg_analysis

    python scripts/run_analysis.py

Si el error persiste, verificar que `config/` se encuentre en la raíz del proyecto.

## `Archivo EDF no encontrado`

Si el pipeline no encuentra un archivo EDF, verificar:

- que el paciente esté correctamente definido en `PACIENTE`;
- que el nombre del archivo EDF esté correctamente definido en `ARCHIVOS`;
- que el archivo se encuentre en la ubicación esperada;
- que la descarga se haya completado correctamente.

## `Crisis fuera del rango temporal del EDF`

Si un archivo `summary` contiene una crisis cuyo intervalo se encuentra fuera de la duración real del archivo EDF, la información del `summary` no debe interpretarse automáticamente como inexistente.

El pipeline debe conservar la información original de la crisis y registrar la inconsistencia para su posterior revisión.

Este caso puede deberse a diferencias entre los registros disponibles, archivos incompletos, registros truncados o inconsistencias entre la información del `summary` y el EDF local.

## `Error durante la lectura o preprocesamiento del EDF`

Si MNE no puede leer el archivo EDF o se produce un error durante el preprocesamiento, verificar:

- que el archivo no esté incompleto o corrupto;
- que la descarga haya finalizado correctamente;
- que el archivo corresponda al paciente y registro indicados;
- que las dependencias del entorno estén instaladas correctamente.

Los errores de lectura o preprocesamiento deben registrarse y no ocultarse, para mantener la trazabilidad y facilitar la revisión de los resultados.

## `ModuleNotFoundError: No module named 'mne'`

Este error indica que MNE-Python no está disponible en el entorno virtual utilizado para ejecutar el proyecto.

Verificar que el entorno virtual esté activo y que las dependencias estén instaladas:

    pip install -r requirements.txt

También se puede comprobar la instalación mediante:

    python -c "import mne; print(mne.__version__)"

# Ejecución

Desde la raíz del proyecto:

    cd /ruta/al/proyecto/chbmit_eeg_analysis

Ejecutar el pipeline:

    python scripts/run_analysis.py

# Estado del proyecto

El proyecto cuenta con una primera versión funcional del pipeline para la descarga, validación y preprocesamiento de registros EEG del dataset CHB-MIT.

La versión actual permite:

- seleccionar explícitamente los registros a procesar;
- descargar y validar archivos EDF;
- conservar los canales EEG disponibles;
- obtener información temporal de los registros;
- identificar las crisis a partir de los archivos `summary`;
- detectar inconsistencias entre los intervalos de las crisis y la duración de los EDF;
- organizar los resultados por paciente y registro;
- conservar metadata asociada al preprocesamiento.

El proyecto continúa en evolución para incorporar mejoras y nuevos análisis sobre los registros EEG preprocesados.
