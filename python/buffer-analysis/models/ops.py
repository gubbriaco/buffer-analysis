from PyLTSpice import RawRead, SpiceEditor
from utils.paths import data, images
from utils.check import check_file, check_image
from matplotlib import pyplot
import pandas as pd
from pandas.plotting import table
from matplotlib import pyplot as plt
import os


def load_asc(asc_file_path, schematic_image_path):
    check_file(asc_file_path)
    netlist = SpiceEditor(asc_file_path)
    return netlist


def load_ltr(raw_file_path):
    check_file(raw_file_path)
    ltr = RawRead(raw_file_path)
    return ltr


def save_image(image_path: str, plt: pyplot) -> None:
    """
    Salva un'immagine utilizzando il percorso specificato e un oggetto pyplot di matplotlib.

    :param image_path: Percorso in cui salvare l'immagine.
    :param plt: Oggetto pyplot di matplotlib contenente l'immagine da salvare.
    :return: None
    """

    # Verifica che il percorso e l'immagine siano validi
    check_image(image_path)

    # Salva l'immagine utilizzando l'oggetto pyplot
    plt.savefig(image_path, format='png')


def table_creation(
        data_table,
        title_plot,
        title_image_saving,
        figsize
):
    df = pd.DataFrame(data_table)
    blankIndex = [''] * len(df)
    df.index = blankIndex

    fig_table, ax_table = plt.subplots(figsize=(figsize[0], figsize[1]))
    ax_table.set_frame_on(False)
    ax_table.set_title(title_plot, fontsize=16, color='blue')
    tab = table(
        ax_table,
        df,
        loc='center',
        colWidths=[0.14] * len(df.columns),
        cellLoc='center'
    )
    tab.auto_set_font_size(False)
    tab.set_fontsize(11)

    for i, key in enumerate(df.keys()):
        cell = tab[0, i]
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold', color='black')
        cell.set_facecolor('lightblue')

    tab.scale(1.2, 1.2)
    ax_table.axis('off')

    fig_table.tight_layout()
    save_image(image_path=os.path.join(images, title_image_saving), plt=plt)
    plt.show()


# energy-connected
def energy_connected(from_ns, to_ns):
    return f".measure tran energy_connected INTEG (v(supply)*i(Vsupply)) from={from_ns}n to={to_ns}n"


# energy-disconnected
def energy_disconnected(from_ns, to_ns):
    return f".measure tran energy_disconnected INTEG (v(supply)*i(Vsupply)) from={from_ns}n to={to_ns}n"


# rise-delay-connected
def rise_delay_connected():
    return ".measure tran rise_delay_connected trig v(IN) val=0.5 fall=1 targ v(OUT) val=0.5 rise=1"


# rise-delay-disconnected
def rise_delay_disconnected():
    return ".measure tran rise_delay_disconnected trig v(IN) val=0.5 fall=1 targ v(OUT) val=0.5 rise=1"


# fall-delay-connected
def fall_delay_connected():
    return ".measure tran fall_delay_connected trig v(IN) val=0.5 rise=1 targ v(OUT) val=0.5 fall=1"


# fall-delay-disconnected
def fall_delay_disconnected():
    return ".measure tran fall_delay_disconnected trig v(IN) val=0.5 rise=1 targ v(OUT) val=0.5 fall=1"
