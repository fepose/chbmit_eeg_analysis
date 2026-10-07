import json
from pathlib import Path


# ============================================================
# GUARDAR METADATA DEL REGISTRO
# ============================================================

def guardar_metadata(resultado, paciente, archivo, carpeta):
    """
    Guarda un resumen del procesamiento de un EDF
    en formato JSON.

    Se genera un archivo independiente para cada EDF.

    Ejemplo:

        chb04_05_metadata.json
        chb04_08_metadata.json
        chb04_28_metadata.json


    Parameters
    ----------
    resultado : dict
        Diccionario generado por procesar_registro().

    paciente : str
        Identificador del paciente.

    archivo : str
        Nombre del archivo EDF.

    carpeta : Path
        Directorio donde se guardará el JSON.

    Returns
    -------
    Path
        Ruta del archivo JSON generado.
    """

    # Preparo el directorio 
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    # obtención del nombre del archivo .edf
    #
    # Ejemplo:
    #
    # chb04_28.edf
    #
    # se convierte en:
    #
    # chb04_28
    nombre_edf = Path(archivo).stem

    # Extracción de información
    raw = resultado["raw"]
    senales = resultado["senales"]
    tiempos = resultado["tiempos"]
    Fs = resultado["Fs"]
    canales = resultado["canales"]
    crisis = resultado["crisis"]
    datos_crisis = resultado["datos_crisis"]

    # Información general del registro
    metadata = {
        "paciente": paciente,
        "archivo_edf": archivo,
        "frecuencia_muestreo_Hz": float(Fs),
        "canales_totales": len(raw.ch_names),
        "canales_EEG": len(canales),
        "canales_EEG_nombres": list(canales),
        "muestras_totales": int(senales.shape[1]),
        "duracion_total_s": float(len(tiempos) / Fs),
        "numero_crisis": len(crisis),
        "crisis": []
    }

    # Información detallada de cada crisis
    for numero_crisis, datos in enumerate(datos_crisis.values(), start=1):

        senal = datos["senal"]

        informacion_crisis = {
            "numero": numero_crisis,
            "inicio_s": float(datos["inicio"]),
            "fin_s": float(datos["fin"]),
            "duracion_s": float(datos["duracion"]),
            "margen_s": float(datos["margen"]),
            "ventana_inicio_s": float(datos["ventana_inicio"]),
            "ventana_fin_s": float(datos["ventana_fin"]),
            "duracion_ventana_s": float(datos["ventana_fin"] - datos["ventana_inicio"]),
            "canales": len(datos["canales"]),
            "muestras": int(senal.shape[1]),
            "forma_matriz": [int(senal.shape[0]), int(senal.shape[1])],
            "canales_nombres": list(datos["canales"])
        }

        metadata["crisis"].append(informacion_crisis)

    # Nombre del archivo JSON de salida
    nombre_archivo = f"{nombre_edf}_metadata.json"
    ruta_metadata = carpeta / nombre_archivo

    # Guardo el archivo JSON
    with open(ruta_metadata, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    # Imprimo por pantalla que se guardo el archivo
    print(f"\n✓ Metadata guardada:")
    print(f"  {ruta_metadata}")

    return ruta_metadata