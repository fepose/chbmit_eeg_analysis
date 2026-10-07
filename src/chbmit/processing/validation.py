# ============================================================
# VALIDAR REGISTRO
# ============================================================

def validar_registro(raw, canales, crisis):
    """
    Valida que el registro EEG tenga información consistente.

    Se verifica:

    - Frecuencia de muestreo.
    - Cantidad total de canales.
    - Existencia de canales EEG.
    - Cantidad de muestras.
    - Duración del registro.
    - Intervalos temporales de las crisis.

    Parameters
    ----------
    raw : mne.io.Raw
        Registro EEG cargado con MNE.

    canales : list
        Lista de canales EEG seleccionados.

    crisis : list
        Lista de tuplas (inicio, fin), en segundos.

    Returns
    -------
    bool
        True si el registro es válido.
        False si se encuentra algún problema.
    """

    valido = True

    # Información general
    Fs = raw.info["sfreq"]
    n_canales = len(raw.ch_names)
    n_muestras = raw.n_times
    duracion = n_muestras / Fs if Fs > 0 else 0

    print("\n")
    print("=" * 60)
    print("VALIDACIÓN DEL REGISTRO")
    print("=" * 60)

    # Frecuencia de muestreo
    if Fs > 0:
        print(f"✓ Frecuencia de muestreo: {Fs} Hz")
    else:
        print("✗ Frecuencia de muestreo inválida")
        valido = False

    # Canales totales
    if n_canales > 0:
        print(f"✓ Número total de canales: {n_canales}")
    else:
        print("✗ No se encontraron canales")
        valido = False

    # Canales EEG
    if len(canales) > 0:
        print(f"✓ Canales EEG disponibles: {len(canales)}")
        for canal in canales:
            print(f"   ✓ {canal}")
    else:
        print("✗ No se encontraron canales EEG")
        valido = False

    # Muestras
    if n_muestras > 0:
        print(f"✓ Número de muestras: {n_muestras}")
    else:
        print("✗ No hay muestras")
        valido = False

    # Duración
    if duracion > 0:
        print(f"✓ Duración: {duracion:.2f} s")
    else:
        print("✗ Duración inválida")
        valido = False

    # Crisis
    if len(crisis) == 0:
        print("✓ No hay crisis en este archivo.")
    else:
        print(f"✓ Crisis encontradas: {len(crisis)}")
        for i, (inicio, fin) in enumerate(crisis,start=1):
            # Validar intervalo
            if (inicio >= 0 and fin <= duracion and inicio < fin):
                print(f"   ✓ Crisis {i}: {inicio}–{fin} s")
            else:
                print(f"   ✗ Crisis {i} fuera del registro: {inicio}–{fin} s")
                valido = False

    # Resultado final
    print("=" * 60)
    if valido:
        print("✓ REGISTRO VÁLIDO")
    else:
        print("✗ REGISTRO NO VÁLIDO")
    print("=" * 60)

    return valido