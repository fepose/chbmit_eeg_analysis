import re
from pathlib import Path
import urllib.request


# ============================================================
# OBTENER CRISIS
# ============================================================

def obtener_crisis(paciente, archivo, carpeta, base_url):
    """
    Obtiene los intervalos temporales de las crisis asociadas
    a un archivo EDF utilizando el archivo summary de CHB-MIT.

    Parameters
    ----------
    paciente : str
        Identificador del paciente.

    archivo : str
        Nombre del archivo EDF.

    carpeta : str or Path
        Directorio donde se guardará el summary.

    base_url : str
        URL base de PhysioNet.

    Returns
    -------
    list
        Lista de tuplas:

        [(inicio_1, fin_1),
         (inicio_2, fin_2),
         ...]

        Los tiempos están expresados en segundos.
    """

    # Preparar directorio
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    # Nombre y ruta del summary
    nombre_summary = f"{paciente}-summary.txt"
    ruta_summary = carpeta / nombre_summary
    url_summary = f"{base_url}/{paciente}/{nombre_summary}"

    # Descargar summary si no existe
    if not ruta_summary.exists():
        print(f"Descargando {nombre_summary}...")

        try:
            urllib.request.urlretrieve(url_summary, ruta_summary)
            print("✓ Summary descargado.")

        except Exception as e:
            print(f"✗ Error al descargar {nombre_summary}: {e}")
            return None
        
    else:
        print(f"✓ Summary ya disponible: {ruta_summary}")

    # Leer summary
    with open(ruta_summary, "r", encoding="utf-8") as f:
        texto = f.read()

    # Localizar el bloque del archivo EDF
    patron = (rf"File Name:\s*{re.escape(archivo)}(.*?)(?=\nFile Name:|\Z)")
    coincidencia = re.search(patron, texto, re.DOTALL)
    if coincidencia is None:
        raise ValueError(f"No se encontró {archivo} en {nombre_summary}")

    bloque = coincidencia.group(1)

    # Número de crisis
    match_num = re.search(r"Number of Seizures in File:\s*(\d+)", bloque)
    if match_num is None:
        raise ValueError(f"No se encontró información de crisis para {archivo}")

    numero_crisis = int(match_num.group(1))

    # Si no hay crisis
    if numero_crisis == 0:
        print(f"\nNo hay crisis en {archivo}.")
        return []

    # Obtención de los tiempos de las crisis
    inicios = []
    finales = []

    # Caso de una sola crisis
    if numero_crisis == 1:
        match_inicio = re.search(r"Seizure Start Time:\s*(\d+)\s*seconds", bloque)
        if match_inicio is not None:
            inicios.append(int(match_inicio.group(1)))

        match_final = re.search(r"Seizure End Time:\s*(\d+)\s*seconds", bloque)
        if match_final is not None:
            finales.append(int(match_final.group(1)))

    # Caso de múltiples crisis
    else:

        for numero in range(1, numero_crisis + 1):
            match_inicio = re.search(rf"Seizure {numero} Start Time:\s*(\d+)\s*seconds", bloque)
            if match_inicio is not None:
                inicios.append(int(match_inicio.group(1)))

            match_final = re.search(rf"Seizure {numero} End Time:\s*(\d+)\s*seconds", bloque)
            if match_final is not None:
                finales.append(int(match_final.group(1)))

    # Validación de la información
    if (len(inicios) != numero_crisis or len(finales) != numero_crisis):
        raise ValueError(f"Información inconsistente de crisis en {archivo}. Esperadas: {numero_crisis}, inicios encontrados: {len(inicios)}, finales encontrados: {len(finales)}")

    # Creación de lista de crisis
    crisis = [(inicio, fin) for inicio, fin in zip(inicios,finales)]

    # Mostrar crisis encontradas
    print(f"\nCrisis encontradas en {archivo}:")

    for i, (inicio, fin) in enumerate(crisis, start=1):
        print(f"   Crisis {i}: {inicio} - {fin} s ({fin - inicio} s)")

    return crisis


# ============================================================
# EXTRAER CRISIS
# ============================================================

def guardar_crisis(raw, canales, crisis, margen=60):
    """
    Extrae cada crisis junto con todos los canales EEG
    disponibles.

    Cada crisis contiene una matriz:

        [n_canales, n_muestras]

    Parameters
    ----------
    raw : mne.io.Raw
        Registro EEG cargado.

    canales : list
        Lista de canales EEG.

    crisis : list
        Lista de tuplas (inicio, fin), en segundos.

    margen : float
        Margen temporal antes y después de cada crisis,
        expresado en segundos.

    Returns
    -------
    dict
        Diccionario con los datos de cada crisis.
    """

    # Frecuencia de muestreo
    Fs = raw.info["sfreq"]

    # Diccionario de resultados
    datos_crisis = {}

    # Procesamiento de cada crisis
    for i, (inicio, fin) in enumerate(crisis, start=1):

        # Ventana temporal
        t_inicio = max(0, inicio - margen)
        t_fin = min(raw.times[-1], fin + margen)

        # Convertir segundos a muestras
        muestra_inicio = int(round(t_inicio * Fs))
        muestra_fin = int(round(t_fin * Fs))

        # Extraer TODOS los canales EEG
        senales, tiempos = raw.get_data(picks=canales, start=muestra_inicio, stop=muestra_fin, return_times=True)

        # Guardar información de la crisis
        datos_crisis[f"crisis_{i}"] = {
            "numero": i,
            "inicio": inicio,
            "fin": fin,
            "duracion": fin - inicio,
            "margen": margen,
            "ventana_inicio": t_inicio,
            "ventana_fin": t_fin,
            "senal": senales,
            "tiempos": tiempos,
            "Fs": Fs,
            "canales": canales.copy(),
        }

        # Mostrar información
        print(f"✓ Crisis {i}: {len(canales)} canales | {senales.shape[1]} muestras")


    return datos_crisis