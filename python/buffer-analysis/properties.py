from utils.paths import rit_models_for_ltspice_file_path

# pmos-minimum_inverter_sizing_analysis
w_min_pmos_start = '0.12u'
w_min_pmos_stop = '0.36u'
w_min_pmos_step = '0.01u'
w_min_pmos_step_param = f'.step param w_min_pmos_analysis {w_min_pmos_start} {w_min_pmos_stop} {w_min_pmos_step}'

# save-w_min_pmos_analysis
save_w_min_pmos_analysis = ".meas w_min_pmos_analysis_values param w_min_pmos_analysis"

# number-of-simulations
nr_runs = 100

# pmos
l_min_pmos = '0.1u'

# nmos
l_min_nmos = '0.1u'
w_min_nmos = '0.12u'

# sizing-factor
S1 = 'mc(4,0.75)'
S2 = 'mc(16,0.75)'
S_LOAD = '50'

# time-run
tran = ".tran 0 65n 0 10p"

# rit-models
rit_models = f".inc {rit_models_for_ltspice_file_path}"

# save-s1-s2
save_s1 = ".meas S1_values param S1"
save_s2 = ".meas S2_values param S2"
