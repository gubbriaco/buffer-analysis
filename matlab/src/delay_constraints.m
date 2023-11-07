function [c_eq, c_ieq] = delay_constraints(s, d, tau_nom, s_load, gamma_d)
    c_eq = tau_nom * ( (1 + (s(1)/gamma_d)) + (1 + (s(2)/(gamma_d*s(1)))) + (1 + (s_load/(gamma_d*s(2)))) ) - d;
    c_ieq = 1 - s(1);
end