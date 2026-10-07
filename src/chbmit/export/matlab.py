from pathlib import Path
import numpy as np
from scipy.io import savemat


# ============================================================
# GUARDAR CRISIS EN FORMATO MATLAB
# ============================================================

def guardar_crisis_mat(datos_crisis, paciente, archivo, carpeta):
    """
    Guarda cada crisis en un archivo MAT independiente.

    Cada archivo MAT corresponde a una crisis de un EDF específico.
    
    Ejemplo:

        chb04_05_C1.mat
        chb04_05_C2.mat

        chb04_28_C1.mat
        chb04_28_C2.mat


    Parameters
    ----------
    datos_crisis : dict
        Diccionario generado por guardar_crisis().

    paciente : str
        Identificador del paciente.
        Ejemplo: "chb04"

    archivo : str
        Nombre del archivo EDF.
        Ejemplo: "chb04_28.edf"

    carpeta : Path
        Directorio donde se guardarán los archivos MAT.

    Returns
    -------
    list
        Lista con las rutas de los archivos MAT generados.
    """

    # Preparo el directorio para guardar los datos
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    # Se obtiene el nombre del archivo .edf
    # Path(archivo).stem elimina la extensión ".edf".
    #
    # Ejemplo:
    #
    # chb04_28.edf
    #
    # se convierte en:
    #
    # chb04_28
    nombre_edf = Path(archivo).stem

    # Lista de archivos generados
    archivos_generados = []

    # Recorro las crisis
    for numero_crisis, crisis in enumerate(datos_crisis.values(), start=1):

        # Obtener información de la crisis
        senales = crisis["senal"]
        tiempos = crisis["tiempos"]
        inicio = crisis["inicio"]
        fin = crisis["fin"]
        duracion = crisis["duracion"]
        margen = crisis["margen"]
        ventana_inicio = crisis["ventana_inicio"]
        ventana_fin = crisis["ventana_fin"]
        Fs = crisis["Fs"]
        canales = crisis["canales"]

        # Validaciones

        # La primera dimensión de senales corresponde al número de canales.
        if senales.shape[0] != len(canales):
            raise ValueError("La cantidad de canales no coincide con la primera dimensión de 'senales'.")

        # La segunda dimensión de senales corresponde al número de muestras.
        if senales.shape[1] != len(tiempos):
            raise ValueError("La cantidad de muestras no coincide con la longitud de 'tiempos'.")

        # Nombre del nuevo archivo .mat

        # El nombre contiene:
        #
        # EDF + número de crisis
        #
        # Ejemplo:
        #
        # chb04_28_C1.mat
        nombre_archivo = f"{nombre_edf}_C{numero_crisis}.mat"
        ruta_archivo = carpeta / nombre_archivo

        # Preparación de los datos para el guardado

        # Señales EEG. Forma: [n_canales x n_muestras]
        datos_mat = {
            "senal": senales,
            "tiempos": tiempos,
            "inicio": inicio,
            "fin": fin,
            "duracion": duracion,
            "margen": margen,
            "ventana_inicio": (ventana_inicio),
            "ventana_fin": (ventana_fin),
            "Fs": Fs,
            "canales": np.array(canales, dtype=object),
            "paciente": paciente,
            "archivo_edf": archivo,
        }

        # Guardo el archivo con los datos
        savemat(ruta_archivo, datos_mat)

        # Guardo la ruta generada
        archivos_generados.append(ruta_archivo)

        # Muestro la información por pantalla
        print(f"\n✓ Crisis {numero_crisis} guardada en MATLAB:")
        print(f"  Archivo : {ruta_archivo}")
        print(f"  Canales : {len(canales)}")
        print(f"  Muestras: {senales.shape[1]}")

    # Resumen
    print("\n")
    print("-" * 60)
    print(f"MAT generados para {archivo}: {len(archivos_generados)}")
    print("-" * 60)

    return archivos_generados