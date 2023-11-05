def energy_function(s, gamma_e, vdd, c_min, s_load):
    energy_model = c_min * vdd * vdd * (gamma_e + ((1 + gamma_e) * s[0]) + ((1 + gamma_e) * s[1]) + s_load)
    return energy_model
