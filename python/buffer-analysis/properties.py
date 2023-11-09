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
