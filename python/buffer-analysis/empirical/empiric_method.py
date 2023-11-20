import numpy as np


def empiric_curve(delay_connected_buffer, energy_connected_buffer, offset_empirical, length):
    delay_tmp = []
    energy_tmp = []
    delay_min = min(delay_connected_buffer)
    energy_min = min(energy_connected_buffer)
    for delay, energy in zip(delay_connected_buffer, energy_connected_buffer):
        delay_cons = delay <= delay_min + (offset_empirical * 1e-10)
        energy_cons = energy <= energy_min + (offset_empirical * 1e-13)
        if delay_cons or energy_cons:
            delay_tmp.append(delay)
            energy_tmp.append(energy)
    final_length = length - len(delay_tmp)

    points = list(zip(energy_tmp, delay_tmp))
    points = sorted(points, key=lambda x: x[1])

    delay_emp = []
    energy_emp = []
    for e, d in points:
        delay_emp.append(d)
        energy_emp.append(e)

    grade = 2
    coeff = np.polyfit(delay_emp, energy_emp, grade)
    pol = np.poly1d(coeff)
    delay_fit = np.linspace(min(delay_emp), max(delay_emp), 100)
    energy_fit = pol(delay_fit)
    delay_fit_tmp = list(delay_fit)
    energy_fit_tmp = list(energy_fit)
    for i in range(0, final_length):
        delay_fit_tmp.append(delay_fit_tmp[-1] + 0.01* 1e-10)
        energy_fit_tmp.append(energy_fit_tmp[-1])
    delay_fit = delay_fit_tmp
    energy_fit = energy_fit_tmp

    return delay_fit, energy_fit
