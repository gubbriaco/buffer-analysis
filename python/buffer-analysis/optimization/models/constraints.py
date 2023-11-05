def delay_constraint(s, delay, tau_nom, gamma_d, s_load):
    c_eq = tau_nom * ( (1 + (s[0]/gamma_d)) + (1 + (s[1]/(gamma_d*s[0]))) + (1 + (s_load/(gamma_d*s[1]))) ) - delay
    c_ieq = 1 - s[0]
    return c_eq, c_ieq
