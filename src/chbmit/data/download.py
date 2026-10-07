from pathlib import Path
import urllib.request


# ============================================================
# DESCARGAR UN EDF
# ============================================================

def descargar_edf(paciente, archivo, carpeta, base_url):
    """
    Descarga un archivo EDF desde PhysioNet.

    Parameters
    ----------
    paciente : str
        Identificador del paciente.
        Ejemplo: "chb04"

    archivo : str
        Nombre del archivo EDF.
        Ejemplo: "chb04_28.edf"

    carpeta : Path
        Directorio donde se guardará el EDF.

    base_url : str
        URL base de PhysioNet.

    Returns
    -------
    Path or None
        Ruta local del archivo descargado.
    """

    # Crear directorio si no existe
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    # Construir URL
    url = (f"{base_url}/{paciente}/{archivo}")

    # Construir ruta local
    ruta_local = carpeta / archivo

    # Verificar si ya existe. Si el archivo ya fue descargado anteriormente, no lo volvemos a descargar.
    if ruta_local.exists():
        print(f"✓ Archivo ya disponible: {ruta_local}")
        return ruta_local

    # Descargar archivo
    print(f"\nDescargando: {archivo}")
    print(f"URL: {url}")

    try:

        with urllib.request.urlopen(url, timeout=30) as respuesta:

            # Obtener tamaño del archivo
            total = respuesta.headers.get("Content-Length")
            if total is not None:
                total = int(total)
                print(f"Tamaño: {total / (1024 * 1024):.2f} MB")

            # Descargar por bloques
            descargado = 0
            bloque = 8192

            with open(ruta_local, "wb") as archivo_local:
                
                while True:
                    datos = respuesta.read(bloque)
                    if not datos:
                        break

                    archivo_local.write(datos)
                    descargado += len(datos)
                    # Mostrar progreso
                    if total:
                        porcentaje = (descargado * 100 / total)
                        print(f"\rProgreso: {porcentaje:6.2f}%", end="", flush=True)

        print("\n✓ Descarga completada.")

        return ruta_local

    except Exception as e:

        # Si la descarga falló, eliminar archivo incompleto.
        if ruta_local.exists():
            ruta_local.unlink()
        print(f"\n✗ Error al descargar {archivo}: {e}")

        return None


# ============================================================
# DESCARGAR VARIOS EDF
# ============================================================

def descargar_archivos(paciente, archivos, carpeta, base_url):
    """
    Descarga una lista de archivos EDF.

    Los archivos que ya existen localmente
    no se vuelven a descargar.

    Parameters
    ----------
    paciente : str
        Identificador del paciente.

    archivos : list
        Lista de nombres EDF.

    carpeta : Path
        Directorio donde guardar los archivos.

    base_url : str
        URL base de PhysioNet.

    Returns
    -------
    list
        Lista de rutas de archivos descargados
        o ya disponibles.
    """

    archivos_descargados = []

    # Recorrer la lista de archivos
    for archivo in archivos:

        print("\n")
        print("=" * 60)
        print(f"ARCHIVO: {archivo}")
        print("=" * 60)

        ruta = descargar_edf(paciente=paciente, archivo=archivo, carpeta=carpeta, base_url=base_url)
        # Guardar solamente los archivos que se obtuvieron correctamente.
        if ruta is not None:
            archivos_descargados.append(ruta)

    # Resumen
    print("\n")
    print("=" * 60)
    print("RESUMEN DE DESCARGAS")
    print("=" * 60)
    print(f"Archivos solicitados : {len(archivos)}")
    print(f"Archivos disponibles : {len(archivos_descargados)}")
    for ruta in archivos_descargados:
        print(f"   ✓ {ruta.name}")

    return archivos_descargados


# ============================================================
# DESCARGAR SUMMARY
# ============================================================

def descargar_summary(paciente, carpeta, base_url):
    """
    Descarga el archivo summary del paciente.

    Ejemplo:

    chb04-summary.txt
    """

    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    nombre_summary = f"{paciente}-summary.txt"
    ruta_summary = carpeta / nombre_summary
    url = f"{base_url}/{paciente}/{nombre_summary}"

    # Verificar si ya existe
    if ruta_summary.exists():
        print(f"✓ Summary ya disponible: {ruta_summary}")
        return ruta_summary

    # Descargar summary
    print(f"Descargando {nombre_summary}...")

    try:

        urllib.request.urlretrieve(url, ruta_summary)
        print("✓ Summary descargado.")
        return ruta_summary

    except Exception as e:

        if ruta_summary.exists():
            ruta_summary.unlink()
        print(f"✗ Error al descargar {nombre_summary}: {e}")

        return None