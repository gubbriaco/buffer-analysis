from scipy.optimize import minimize
from optimization.models.objective_functions import energy_function as energy
from optimization.models.constraints import delay_constraint


def optimize_considering_delay(delay, tau_nom, gamma_d, s_load, vdd, c_min, gamma_e, s0, max_iter):
    delay_constraints = ({'type': 'eq', 'fun': delay_constraint, 'args': (delay, tau_nom, gamma_d, s_load)})
    result = minimize(energy, s0, args=(gamma_e, vdd, c_min, s_load), constraints=delay_constraints, method='SLSQP',
                      options={'maxiter': max_iter})
    return result.x, result.fun, result.nit
