import sys
from pathlib import Path


# ============================================================
# CONFIGURACIÓN DE RUTAS DEL PROYECTO
# ============================================================

# ROOT_DIR corresponde a:
#
# chbmit_eeg_analysis_V2/
#
# Esto permite ejecutar este script directamente desde
# cualquier ubicación.

ROOT_DIR = Path(__file__).resolve().parent.parent

# Agregar el directorio principal al PATH de Python
sys.path.insert(0, str(ROOT_DIR))

# Agregar src al PATH de Python
sys.path.insert(0, str(ROOT_DIR / "src"))

# ============================================================
# IMPORTAR CONFIGURACIÓN
# ============================================================

from config.config import PACIENTE, ARCHIVOS, MARGEN, BASE_URL
from config.config import RAW_PATIENT_DIR, CSV_PATIENT_DIR, MAT_PATIENT_DIR, FIGURES_PATIENT_DIR, METADATA_PATIENT_DIR

# ============================================================
# IMPORTAR PIPELINE
# ============================================================

from chbmit.processing.pipeline import procesar_registro

# ============================================================
# IMPORTAR VISUALIZACIONES
# ============================================================

from chbmit.visualization.plots import graficar_crisis, graficar_crisis_canales, graficar_registro_crisis

# ============================================================
# IMPORTAR GUARDADO CSV
# ============================================================

from chbmit.data.saver import guardar_crisis_csv

# ============================================================
# IMPORTAR EXPORTACIÓN MATLAB
# ============================================================

from chbmit.export.matlab import guardar_crisis_mat

# ============================================================
# IMPORTAR METADATA
# ============================================================

from chbmit.export.metadata import guardar_metadata

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """
    Ejecuta el procesamiento de todos los EDF definidos
    manualmente en ARCHIVOS.

    Cada EDF se procesa de manera independiente.

    Si un archivo falla, se informa el error y el programa
    continúa con el siguiente archivo.
    """

    # Encabezado general
    print("\n")
    print("=" * 70)
    print("ANÁLISIS CHB-MIT EEG")
    print("=" * 70)
    print(f"Paciente: {PACIENTE}")
    print(f"Archivos seleccionados: {len(ARCHIVOS)}")

    # Mostrar los arhciov seleccionados
    print("\nArchivos a procesar:")
    for i, archivo in enumerate(ARCHIVOS,start=1):
        print(f"   {i:02d}. {archivo}")

    # Contadores generales
    archivos_exitosos = []
    archivos_fallidos = []

    # Procesamiento de cada archivo .edf
    for numero_archivo, archivo in enumerate(ARCHIVOS, start=1):

        # Encabezado del archivo
        print("\n\n")
        print("=" * 70)
        print(f"ARCHIVO {numero_archivo}/{len(ARCHIVOS)}")
        print("=" * 70)
        print(f"Paciente : {PACIENTE}")
        print(f"EDF      : {archivo}")
        print("=" * 70)

        # Procesamiento del registro
        try:
            resultado = procesar_registro(paciente=PACIENTE, archivo=archivo, margen=MARGEN, carpeta=RAW_PATIENT_DIR, base_url=BASE_URL)

        except Exception as e:

            # Si ocurre un error, no detenemos todo el procesamiento.
            print("\n")
            print("!" * 70)
            print(f"✗ ERROR PROCESANDO: {archivo}")
            print(f"Error: {e}")
            print("!" * 70)
            archivos_fallidos.append(archivo)
            continue

        # Verificación del resultado
        if resultado is None:
            print("\n")
            print(f"✗ No se pudo procesar {archivo}.")
            archivos_fallidos.append(archivo)
            continue

        # Extracción de la información
        senales = resultado["senales"]
        tiempos = resultado["tiempos"]
        Fs = resultado["Fs"]
        canales = resultado["canales"]
        crisis = resultado["crisis"]
        datos_crisis = resultado["datos_crisis"]

        # Resumen del archivo
        print("\n")
        print("=" * 70)
        print("DATOS DISPONIBLES")
        print("=" * 70)
        print(f"Paciente    : {PACIENTE}")
        print(f"Archivo     : {archivo}")
        print(f"Canales EEG : {len(canales)}")
        print(f"Muestras    : {senales.shape[1]}")
        print(f"Fs          : {Fs} Hz")
        print(f"Crisis      : {len(crisis)}")

        # Lista de canales
        print("\n")
        print("=" * 70)
        print("CANALES EEG UTILIZADOS")
        print("=" * 70)
        print(f"\nTotal de canales EEG: {len(canales)}")

        for i, canal in enumerate(canales, start=1):
            print(f"   {i:02d}. {canal}")

        # Gráfico del registro completo
        print("\n")
        print("=" * 70)
        print("GENERANDO FIGURA DEL REGISTRO COMPLETO")
        print("=" * 70)

        try:
            graficar_registro_crisis(raw=resultado["raw"], canales=canales, crisis=crisis, paciente=PACIENTE, archivo=archivo)
        except Exception as e:
            print("\n✗ Error generando figura del registro completo:")
            print(f"  {e}")

        # Gráfico de las crisis
        if len(datos_crisis) > 0:

            print("\n")
            print("=" * 70)
            print("GENERANDO GRÁFICOS DE LAS CRISIS")
            print("=" * 70)

            for numero_crisis in range(1, len(datos_crisis) + 1):

                # Gráfico del primer canal
                try:
                    graficar_crisis(datos_crisis=datos_crisis, numero_crisis=numero_crisis, paciente=PACIENTE, archivo=archivo)
                except Exception as e:
                    print(f"\n✗ Error generando gráfico de crisis {numero_crisis}:")
                    print(f"  {e}")

                # Gráfico de todos los canales
                try:
                    graficar_crisis_canales(datos_crisis=datos_crisis, numero_crisis=numero_crisis, paciente=PACIENTE, archivo=archivo)
                except Exception as e:
                    print(f"\n✗ Error generando gráfico de todos los canales para crisis {numero_crisis}:")
                    print(f"  {e}")

        else:
            print("\n")
            print("✓ No hay crisis. No se generan gráficos individuales de crisis.")

        # GUARDAR CRISIS EN CSV
        archivos_csv = []

        if len(datos_crisis) > 0:

            print("\n")
            print("=" * 70)
            print("GUARDANDO CRISIS EN CSV")
            print("=" * 70)

            try:
                archivos_csv = (guardar_crisis_csv(datos_crisis=datos_crisis, paciente=PACIENTE, archivo=archivo, carpeta=CSV_PATIENT_DIR))
                print("\nArchivos CSV generados:")
                for archivo_csv in archivos_csv:
                    print(f"   ✓ {archivo_csv}")

            except Exception as e:
                print("\n✗ Error guardando archivos CSV:")
                print(f"  {e}")

        else:
            print("\n")
            print("✓ No hay crisis. No se generan CSV.")

        # Guardo las crsis en archivos .mat
        archivos_mat = []

        if len(datos_crisis) > 0:

            print("\n")
            print("=" * 70)
            print("GUARDANDO CRISIS EN MATLAB (.MAT)")
            print("=" * 70)

            try:
                archivos_mat = (guardar_crisis_mat(datos_crisis=datos_crisis, paciente=PACIENTE, archivo=archivo, carpeta=MAT_PATIENT_DIR))
                print("\nArchivos MAT generados:")
                for archivo_mat in archivos_mat:
                    print(f"   ✓ {archivo_mat}")

            except Exception as e:
                print("\n✗ Error guardando archivos MAT:")
                print(f"  {e}")

        else:

            print("\n")
            print("✓ No hay crisis. No se generan MAT.")

        # Guardo metadata
        print("\n")
        print("=" * 70)
        print("GUARDANDO METADATA")
        print("=" * 70)

        ruta_metadata = None

        try:
            ruta_metadata = (guardar_metadata(resultado=resultado, paciente=PACIENTE, archivo=archivo, carpeta=METADATA_PATIENT_DIR))

        except Exception as e:
            print("\n✗ Error guardando metadata:")
            print(f"  {e}")

        # Agrego el archivo a la lista de archivos procesados correctamente
        archivos_exitosos.append(archivo)

        # Resumen del archivo
        print("\n")
        print("=" * 70)
        print(f"✓ FINALIZADO: {archivo}")
        print("=" * 70)
        print(f"Canales EEG : {len(canales)}")
        print(f"Fs          : {Fs} Hz")
        print(f"Muestras    : {senales.shape[1]}")
        print(f"Crisis      : {len(crisis)}")
        print(f"CSV         : {len(archivos_csv)}")
        print(f"MAT         : {len(archivos_mat)}")
        print(f"Metadata    : {'Sí' if ruta_metadata else 'No'}")

    # Resumen final de todos los archivos
    print("\n\n")
    print("=" * 70)
    print("RESUMEN FINAL DEL PROCESAMIENTO")
    print("=" * 70)

    # Archivos exitosos
    print("\n")
    print(f"✓ Archivos procesados correctamente: {len(archivos_exitosos)}")
    for archivo in archivos_exitosos:
        print(f"   ✓ {archivo}")

    # Archivos fallidos
    print("\n")
    print(f"✗ Archivos con problemas: {len(archivos_fallidos)}")
    for archivo in archivos_fallidos:
        print(f"   ✗ {archivo}")

    # Directorios de resultados
    print("\n")
    print("=" * 70)
    print("DIRECTORIOS DE RESULTADOS")
    print("=" * 70)
    print(f"\nEDF:")
    print(f"   {RAW_PATIENT_DIR}")
    print(f"\nCSV:")
    print(f"   {CSV_PATIENT_DIR}")
    print(f"\nMAT:")
    print(f"   {MAT_PATIENT_DIR}")
    print(f"\nFiguras:")
    print(f"   {FIGURES_PATIENT_DIR}")
    print(f"\nMetadata:")
    print(f"   {METADATA_PATIENT_DIR}")

    # Termino el programa
    print("\n")
    print("=" * 70)

    if len(archivos_fallidos) == 0:
        print("✓ TODOS LOS ARCHIVOS FUERON PROCESADOS CORRECTAMENTE")
    else:
        print("⚠ EL PROCESAMIENTO TERMINÓ CON ALGUNOS ARCHIVOS CON PROBLEMAS")

    print("=" * 70)
    print()


# ============================================================
# EJECUTAR MAIN
# ============================================================

if __name__ == "__main__":
    main()