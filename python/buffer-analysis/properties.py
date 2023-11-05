from utils.paths import rit_models_for_ltspice_file_path

# number-of-simulations
nr_runs = 100

# pmos
l_min_pmos = '0.1u'
w_min_pmos = '0.2u'

# nmos
l_min_nmos = '0.1u'
w_min_nmos = '0.12u'

# sizing-factor
S1 = 'mc(4,0.75)'
S2 = 'mc(16,0.75)'
S_LOAD = '50'

# time-run
tran = ".tran 0 50n 0"

# rit-models
rit_models = f".inc {rit_models_for_ltspice_file_path}"

# save-s1-s2
save_s1 = ".meas S1_values param S1"
save_s2 = ".meas S2_values param S2"

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
