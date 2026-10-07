from pathlib import Path
import matplotlib.pyplot as plt
from config.config import FIGURES_PATIENT_DIR


# ============================================================
# GRAFICAR UNA SEÑAL
# ============================================================

def graficar_senal(senal, tiempos, canal, paciente, archivo):
    """
    Grafica una señal EEG individual.

    Parameters
    ----------
    senal : array
        Señal EEG.

    tiempos : array
        Vector temporal.

    canal : str
        Nombre del canal EEG.

    paciente : str
        Identificador del paciente.

    archivo : str
        Nombre del EDF de origen.
    """

    # Directorio
    FIGURES_PATIENT_DIR.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo EDF
    nombre_edf = Path(archivo).stem

    # Creo la figura
    fig, ax = plt.subplots(figsize=(16, 5))

    ax.plot(tiempos, senal, linewidth=0.5)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud (µV)")
    ax.set_title(f"{paciente} - {nombre_edf} - {canal}")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Nombre y ruta de la figura
    nombre_figura = f"{nombre_edf}_{canal}_senal.png"
    ruta_figura = FIGURES_PATIENT_DIR / nombre_figura

    # Guardo la figura
    plt.savefig(ruta_figura, dpi=300, bbox_inches="tight")
    print(f"✓ Figura guardada: {ruta_figura}")

    plt.show()
    plt.close()


# ============================================================
# GRAFICAR UNA CRISIS
# ============================================================

def graficar_crisis(datos_crisis, numero_crisis, paciente, archivo):
    """
    Grafica una crisis utilizando el primer canal EEG.

    Parameters
    ----------
    datos_crisis : dict
        Diccionario con las crisis extraídas.

    numero_crisis : int
        Número de crisis a graficar.

    paciente : str
        Identificador del paciente.

    archivo : str
        Nombre del EDF de origen.
    """

    # Directorio
    FIGURES_PATIENT_DIR.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo EDF
    nombre_edf = Path(archivo).stem

    # Obtención de los datos
    crisis = datos_crisis[f"crisis_{numero_crisis}"]
    senales = crisis["senal"]
    tiempos = crisis["tiempos"]
    canales = crisis["canales"]

    # Utilizo el primer canal EEG solamente para esta figura individual.
    canal = canales[0]
    senal = senales[0]

    # Figura
    fig, ax = plt.subplots(figsize=(16, 5))

    ax.plot(tiempos, senal, linewidth=0.5)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel(f"Amplitud (µV) - {canal}")
    ax.set_title(f"{paciente} - {nombre_edf} - Crisis {numero_crisis}")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Nombre y ruta de la figura
    nombre_figura = f"{nombre_edf}_C{numero_crisis}_crisis.png"
    ruta_figura = FIGURES_PATIENT_DIR / nombre_figura

    # Guardo la figura
    plt.savefig(ruta_figura, dpi=300, bbox_inches="tight")
    print(f"✓ Figura guardada: {ruta_figura}")

    plt.show()
    plt.close()


# ============================================================
# GRAFICAR TODOS LOS CANALES DE UNA CRISIS
# ============================================================

def graficar_crisis_canales(datos_crisis, numero_crisis, paciente, archivo):
    """
    Grafica todos los canales EEG correspondientes
    a una crisis.

    Se crea un subplot independiente para cada canal.

    Parameters
    ----------
    datos_crisis : dict
        Diccionario con las crisis extraídas.

    numero_crisis : int
        Número de crisis.

    paciente : str
        Identificador del paciente.

    archivo : str
        Nombre del EDF de origen.
    """

    # Directorio
    FIGURES_PATIENT_DIR.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo EDF
    nombre_edf = Path(archivo).stem

    # Obtención de la crisis
    crisis = datos_crisis[f"crisis_{numero_crisis}"]
    senales = crisis["senal"]
    tiempos = crisis["tiempos"]
    canales = crisis["canales"]

    # Número de canales
    n_canales = len(canales)

    # Creo la figura
    fig, axes = plt.subplots(n_canales, 1, figsize=(16,max(2 * n_canales, 8)), sharex=True)

    # --------------------------------------------------------
    # Caso especial:
    #
    # Si solamente existe un canal, matplotlib no devuelve una lista de axes sino un único objeto.
    #
    # Lo convertimos en una lista para poder usar siempre el mismo código.
    # 
    # --------------------------------------------------------

    if n_canales == 1:
        axes = [axes]

    # Gráfico individual de cada canal
    for i, canal in enumerate(canales):
        axes[i].plot(tiempos, senales[i], linewidth=0.5)
        axes[i].set_ylabel(canal)
        axes[i].grid(True, alpha=0.3)

    axes[-1].set_xlabel("Tiempo (s)")
    fig.suptitle(f"{paciente} - {nombre_edf} - Crisis {numero_crisis} - Todos los canales EEG")

    plt.tight_layout()

    # Nombre y ruta del archivo
    nombre_figura = (f"{nombre_edf}_C{numero_crisis}_todos_los_canales.png")
    ruta_figura = FIGURES_PATIENT_DIR / nombre_figura

    # Guardo la figura
    plt.savefig(ruta_figura, dpi=300, bbox_inches="tight")
    print(f"✓ Figura guardada: {ruta_figura}")

    plt.show()
    plt.close()


# ============================================================
# REGISTRO COMPLETO + CRISIS
# ============================================================

def graficar_registro_crisis(raw, canales, crisis, paciente, archivo):
    """
    Grafica el registro EEG completo utilizando el primer
    canal EEG y marca los intervalos de todas las crisis.

    Parameters
    ----------
    raw : mne.io.Raw
        Registro EEG completo.

    canales : list
        Lista de canales EEG.

    crisis : list
        Lista de tuplas:
            [(inicio_1, fin_1),
             (inicio_2, fin_2), ...]

    paciente : str
        Identificador del paciente.

    archivo : str
        Nombre del EDF de origen.
    """

    # Directorio
    FIGURES_PATIENT_DIR.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo EDF
    nombre_edf = Path(archivo).stem

    # Selecciono el primer canal y obtengo la señal
    canal = canales[0]
    senal, tiempos = raw.get_data(picks=[canal], return_times=True)

    # MNE devuelve:
    #
    # [1, n_muestras]
    #
    # Por eso tomamos el primer elemento.
    senal = senal[0]

    # Figura
    fig, ax = plt.subplots(figsize=(16, 5))

    ax.plot(tiempos, senal, linewidth=0.5)

    for i, (inicio, fin) in enumerate(crisis, start=1):
        ax.axvspan(inicio, fin, alpha=0.25, label=f"Crisis {i}")

    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel(f"Amplitud (µV) - {canal}")
    ax.set_title(f"{paciente} - {nombre_edf} - Registro completo")
    ax.grid( True, alpha=0.3)
    if len(crisis) > 0:
        ax.legend()

    plt.tight_layout()

    # Nombre y ruta del archivo de salida
    nombre_figura = f"{nombre_edf}_registro_completo_crisis.png"
    ruta_figura = FIGURES_PATIENT_DIR / nombre_figura
    
    # Guardo la figura
    plt.savefig(ruta_figura, dpi=300, bbox_inches="tight")
    print(f"✓ Figura guardada: {ruta_figura}")

    plt.show()
    plt.close()