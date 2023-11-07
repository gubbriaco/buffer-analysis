function [energy] = energy_model(s, vdd, c_min, s_load, gamma_e)
    energy = c_min * vdd * vdd * ( gamma_e + ((1 + gamma_e) * s(1)) + ((1 + gamma_e) * s(2)) + s_load );
end