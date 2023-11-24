from utils.check import check_file
from PyLTSpice import RawRead, SpiceEditor
from IPython.display import Image, display


def load_asc(asc_file_path, schematic_image_path):
    check_file(asc_file_path)
    netlist = SpiceEditor(asc_file_path)

    display(Image(schematic_image_path))

    return netlist


def load_ltr(raw_file_path):
    check_file(raw_file_path)
    ltr = RawRead(raw_file_path)
    return ltr


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
