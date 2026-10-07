from chbmit.data.download import descargar_edf
from chbmit.data.loader import cargar_edf, extraer_canales, obtener_canales_eeg
from chbmit.processing.seizures import obtener_crisis, guardar_crisis
from chbmit.processing.validation import validar_registro


# ============================================================
# PROCESAR UN ÚNICO REGISTRO EDF
# ============================================================

def procesar_registro(paciente, archivo, margen, carpeta, base_url):
    """
    Procesa un único archivo EDF.

    Esta función trabaja con UN archivo por vez.

    El recorrido general será:

        1. Descargar / verificar EDF
        2. Obtener información de las crisis
        3. Cargar EDF
        4. Identificar canales EEG
        5. Validar registro
        6. Extraer todos los canales EEG
        7. Extraer las ventanas de las crisis

    Parameters
    ----------
    paciente : str
        Identificador del paciente.
        Ejemplo: "chb04"

    archivo : str
        Nombre del EDF.
        Ejemplo: "chb04_28.edf"

    margen : int or float
        Tiempo en segundos que se agrega antes
        y después de cada crisis.

    carpeta : Path
        Directorio donde están los EDF.

    base_url : str
        URL base de PhysioNet.

    Returns
    -------
    dict or None
        Diccionario con todos los datos procesados.
    """

    # Información del registro
    print("\n")
    print("=" * 70)
    print("PROCESAMIENTO DEL REGISTRO")
    print("=" * 70)
    print(f"Paciente : {paciente}")
    print(f"Archivo  : {archivo}")

    # 1. Descargar / verficar EDF
    print("\n")
    print("=" * 70)
    print("1. DESCARGANDO / VERIFICANDO EDF")
    print("=" * 70)

    ruta_edf = descargar_edf(paciente=paciente, archivo=archivo, carpeta=carpeta, base_url=base_url)
    
    # Verificar que el archivo esté disponible
    if ruta_edf is None:
        print("\n✗ No se pudo obtener el archivo {archivo}.")
        return None

    print(f"\n✓ EDF disponible:")
    print(f"  {ruta_edf}")

    # 2. Obtención de la información de las crisis
    print("\n")
    print("=" * 70)
    print("2. OBTENIENDO INFORMACIÓN DE LAS CRISIS")
    print("=" * 70)

    crisis = obtener_crisis(paciente=paciente, archivo=archivo, carpeta=carpeta, base_url=base_url)
    
    # Verificar que se pudo obtener la información
    if crisis is None:
        print("\n✗ No se pudo obtener la información de las crisis.")
        return None

    # Mostrar resultado
    if len(crisis) == 0:
        print("\n✓ El archivo no contiene crisis.")
    else:
        print(f"\n✓ Crisis encontradas: {len(crisis)}")

    # 3. Carga del EDF
    print("\n")
    print("=" * 70)
    print("3. CARGANDO EDF")
    print("=" * 70)

    raw = cargar_edf(ruta_edf)
    if raw is None:
        print("\n✗ No se pudo cargar {archivo}.")
        return None

    # 4. Identificación de canales del EEG
    print("\n")
    print("=" * 70)
    print("4. IDENTIFICANDO CANALES EEG")
    print("=" * 70)

    canales = obtener_canales_eeg(raw)
    if len(canales) == 0:
        print("\n✗ No se encontraron canales EEG.")
        return None

    # 5. Validación del registro
    print("\n")
    print("=" * 70)
    print("5. VALIDANDO REGISTRO")
    print("=" * 70)

    valido = validar_registro(raw, canales, crisis)
    if not valido:
        print("\n✗ El procesamiento fue detenido porque el registro no es válido.")
        return None

    print("\n✓ Registro válido.")

    # 6. Extracción de los canales del EEG
    print("\n")
    print("=" * 70)
    print("6. EXTRAYENDO TODOS LOS CANALES EEG")
    print("=" * 70)

    senales, tiempos, Fs = extraer_canales(raw, canales)

    # 7. Extracción de las crisis
    print("\n")
    print("=" * 70)
    print("7. EXTRAYENDO CRISIS")
    print("=" * 70)

    # --------------------------------------------------------
    # Si no hay crisis, no intentamos extraer ventanas.
    #
    # Esto es importante porque se puede procesar una
    # lista arbitraria de EDF y algunos pueden no tener crisis.
    # --------------------------------------------------------

    if len(crisis) > 0:
        datos_crisis = guardar_crisis(raw, canales, crisis, margen)

    else:
        datos_crisis = {}
        print("\n✓ No hay crisis para extraer.")

    # Resumen del registro
    print("\n")
    print("=" * 70)
    print("RESUMEN DEL REGISTRO")
    print("=" * 70)
    print(f"Paciente       : {paciente}")
    print(f"Archivo        : {archivo}")
    print(f"Canales EEG    : {len(canales)}")
    print(f"Frecuencia     : {Fs} Hz")
    print(f"Muestras       : {senales.shape[1]}")
    print(f"Duración       : {senales.shape[1] / Fs:.2f} s")
    print(f"Crisis         : {len(crisis)}")

    # Lista de canales del EEG
    print("\nCanales EEG utilizados:")
    for i, canal in enumerate(canales, start=1):
        print(f"   {i:02d}. {canal}")

    # Información de cada crisis
    if len(datos_crisis) > 0:
        print("\n")
        print("=" * 70)
        print("CRISIS EXTRAÍDAS")
        print("=" * 70)

        for numero_crisis, datos in enumerate(datos_crisis.values(), start=1):
            print(f"\nCrisis {numero_crisis}:")
            print(f"   Inicio      : {datos['inicio']} s")
            print(f"   Fin         : {datos['fin']} s")
            print(f"   Duración    : {datos['duracion']} s")
            print(f"   Ventana     : {datos['ventana_inicio']} - {datos['ventana_fin']} s")
            print(f"   Canales     : {len(datos['canales'])}")
            print(f"   Muestras    : {datos['senal'].shape[1]}")

    # Retorno los resultados obtenidos
    return {
        "raw": raw,
        "senales": senales,
        "tiempos": tiempos,
        "Fs": Fs,
        "canales": canales,
        "crisis": crisis,
        "datos_crisis": datos_crisis,
        "ruta_edf": ruta_edf,
    }