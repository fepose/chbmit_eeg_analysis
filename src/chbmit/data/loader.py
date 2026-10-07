import mne


# ============================================================
# CARGAR ARCHIVO EDF
# ============================================================

def cargar_edf(ruta_edf):
    """
    Carga un archivo EDF utilizando MNE.

    Parameters
    ----------
    ruta_edf : str or Path
        Ruta al archivo EDF.

    Returns
    -------
    mne.io.Raw
        Registro EEG cargado.
    """

    print("\nCargando EDF...")
    raw = mne.io.read_raw_edf(ruta_edf, preload=True, verbose=False)
    print("✓ EDF cargado.")

    return raw


# ============================================================
# OBTENER CANALES EEG
# ============================================================

def obtener_canales_eeg(raw):
    """
    Obtiene únicamente los canales de tipo EEG.

    Los canales que no sean EEG, como ECG, quedan excluidos.

    Parameters
    ----------
    raw : mne.io.Raw
        Registro cargado mediante MNE.

    Returns
    -------
    list
        Lista con los nombres de los canales EEG.
    """

    canales_eeg = []
    for canal in raw.ch_names:
        tipo = raw.get_channel_types(picks=[canal])[0]
        if tipo == "eeg":
            canales_eeg.append(canal)

    # Mostrar canales encontrados
    print("\nCanales EEG disponibles:")
    for i, canal in enumerate(canales_eeg, start=1):
        print(f"   {i:02d}. {canal}")

    print(f"\nTotal de canales EEG: {len(canales_eeg)}")

    return canales_eeg


# ============================================================
# OBTENER CANALES NO EEG
# ============================================================

def obtener_canales_no_eeg(raw):
    """
    Obtiene los canales que no son EEG.

    Por ejemplo:
    ECG, EOG, EMG, etc.

    Parameters
    ----------
    raw : mne.io.Raw
        Registro cargado mediante MNE.

    Returns
    -------
    list
        Lista con los canales no EEG.
    """

    canales_no_eeg = []

    for canal in raw.ch_names:
        tipo = raw.get_channel_types(picks=[canal])[0]
        if tipo != "eeg":
            canales_no_eeg.append(canal)

    if canales_no_eeg:
        print("\nCanales no EEG:")
        for i, canal in enumerate(canales_no_eeg, start=1):
            tipo = raw.get_channel_types(picks=[canal])[0]
            print(f"   {i:02d}. {canal} ({tipo})")

    else:
        print("\nNo se encontraron canales no EEG.")

    return canales_no_eeg


# ============================================================
# EXTRAER UN SOLO CANAL
# ============================================================

def extraer_canal(raw, canal):
    """
    Extrae un único canal EEG completo.

    Parameters
    ----------
    raw : mne.io.Raw
        Registro EEG cargado.

    canal : str
        Nombre del canal.

    Returns
    -------
    senal : numpy.ndarray
        Señal del canal.

    tiempos : numpy.ndarray
        Vector temporal en segundos.

    Fs : float
        Frecuencia de muestreo.
    """

    senal, tiempos = raw.get_data(picks=[canal], return_times=True)
    senal = senal[0]
    Fs = raw.info["sfreq"]

    return senal, tiempos, Fs


# ============================================================
# EXTRAER TODOS LOS CANALES EEG
# ============================================================

def extraer_canales(raw, canales):
    """
    Extrae todos los canales EEG seleccionados.

    Parameters
    ----------
    raw : mne.io.Raw
        Registro EEG cargado mediante MNE.

    canales : list
        Lista con los nombres de los canales EEG.

    Returns
    -------
    senales : numpy.ndarray
        Matriz de dimensiones:

        [n_canales, n_muestras]

    tiempos : numpy.ndarray
        Vector temporal en segundos.

    Fs : float
        Frecuencia de muestreo.
    """

    # Extraer canales
    senales, tiempos = raw.get_data(picks=canales, return_times=True)
    Fs = raw.info["sfreq"]

    # Mostrar información
    print("\nExtracción de señales:")
    print(f"Canales : {senales.shape[0]}")
    print(f"Muestras: {senales.shape[1]}")
    print(f"Fs      : {Fs} Hz")

    return senales, tiempos, Fs
