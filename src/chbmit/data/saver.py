from pathlib import Path
import pandas as pd


# ============================================================
# GUARDAR CRISIS EN CSV
# ============================================================

def guardar_crisis_csv(datos_crisis, paciente, archivo, carpeta):
    """
    Guarda cada crisis en un archivo CSV.

    Cada archivo EDF procesado tendrá sus propios archivos CSV.

    Ejemplo:

        chb04_05_C1.csv
        chb04_05_C2.csv

        chb04_28_C1.csv
        chb04_28_C2.csv


    Parameters
    ----------
    datos_crisis : dict
        Diccionario generado por guardar_crisis().

    paciente : str
        Identificador del paciente.
        Ejemplo: "chb04"

    archivo : str
        Nombre del EDF.
        Ejemplo: "chb04_28.edf"

    carpeta : Path
        Directorio donde se guardarán los CSV.

    Returns
    -------
    list
        Lista con las rutas de los archivos CSV generados.
    """

    # Se prepara el directorio
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    # Obtención del nombre del .edf
    # Path(archivo).stem elimina la extensión ".edf".
    #
    # Por ejemplo:
    #
    # "chb04_28.edf"
    #
    # se convierte en:
    #
    # "chb04_28"
    nombre_edf = Path(archivo).stem

    # Lista de archivos generados
    archivos_generados = []

    # Se recorren las crisis
    for numero_crisis, crisis in enumerate(datos_crisis.values(), start=1):

        # Obtener información de la crisis
        senales = crisis["senal"]
        tiempos = crisis["tiempos"]
        canales = crisis["canales"]

        # Validaciones:
        
        # Verificar que el número de canales coincida con la primera dimensión de la matriz EEG.
        if senales.shape[0] != len(canales):
            raise ValueError("La cantidad de canales no coincide con la primera dimensión de 'senales'.")

        # Verificar que el número de muestras coincida con la cantidad de tiempos.
        if senales.shape[1] != len(tiempos):
            raise ValueError("La cantidad de muestras no coincide con la longitud de 'tiempos'.")

        # Creación del dataframe

        # senales tiene forma:
        #
        # [n_canales, n_muestras]
        #
        # Para construir el DataFrame necesitamos:
        #
        # [n_muestras, n_canales]
        #
        # Por eso utilizamos .T.
        df = pd.DataFrame(senales.T, columns=canales)

        # Se agrega la columna tiempo al dataframe
        # La primera columna será el tiempo relativo al inicio de la ventana de crisis.
        df.insert(0, "time", tiempos)

        # NOMBRE DEL ARCHIVO

        # El nombre incluye:
        #
        # paciente
        # EDF
        # número de crisis
        #
        # Ejemplo:
        #
        # chb04_28_C1.csv
        nombre_archivo = (f"{paciente}_{nombre_edf}_C{numero_crisis}.csv")
        ruta_archivo = carpeta / nombre_archivo

        # Guardar en formato csv
        df.to_csv(ruta_archivo, index=False)

        # Guardar ruta
        archivos_generados.append(ruta_archivo)

        # Mostrar la información por pantalla
        print(f"\n✓ Crisis {numero_crisis} guardada en CSV:")
        print(f"  Archivo : {ruta_archivo}")
        print(f"  Canales : {len(canales)}")
        print(f"  Muestras: {len(df)}")

    # Resumen
    print("\n")
    print("-" * 60)
    print(f"CSV generados para {archivo}: {len(archivos_generados)}")
    print("-" * 60)

    return archivos_generados
