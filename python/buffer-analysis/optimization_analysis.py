import os
import matplotlib.pyplot as plt
from optimization.optimize_function import optimize_considering_delay
from models.ops import save_image, table_creation
from utils.dir import get_values_from_file
from utils.paths import images
from utils.paths import data


def optimization_analysis():
    optimal_results = []

    c_min_for_optimization_file_path = os.path.join(data, 'out', 'params', 'c_min_for_optimization_analysis.txt')
    c_min_for_optimization = get_values_from_file(c_min_for_optimization_file_path)
    c_min_for_optimization = c_min_for_optimization[0]

    tau_nom_for_optimization_file_path = os.path.join(data, 'out', 'params', 'tau_nom_for_optimization_analysis.txt')
    tau_nom_for_optimization = get_values_from_file(tau_nom_for_optimization_file_path)
    tau_nom_for_optimization = tau_nom_for_optimization[0]

    vdd_file_path = os.path.join(data, 'out', 'params', 'vdd_analysis.txt')
    vdd = get_values_from_file(vdd_file_path)
    vdd = vdd[0]

    s_load_file_path = os.path.join(data, 'out', 'params', 's_load_analysis.txt')
    s_load = get_values_from_file(s_load_file_path)
    s_load = s_load[0]

    gamma_e_file_path = os.path.join(data, 'out', 'params', 'gamma_e_analysis.txt')
    gamma_e = get_values_from_file(gamma_e_file_path)
    gamma_e = gamma_e[0]

    gamma_d_file_path = os.path.join(data, 'out', 'params', 'gamma_d_analysis.txt')
    gamma_d = get_values_from_file(gamma_d_file_path)
    gamma_d = gamma_d[0]

    c_min = c_min_for_optimization
    tau_nom = tau_nom_for_optimization
    s0 = [10, 10]
    max_iter = 10000

    s1_from_python = []
    s2_from_python = []
    delay_values = []

    d_max = 510
    d_min = 100
    step_opt = 10

    for delay in range(d_max, d_min - 1, -step_opt):
        variables, energy_value, iteration_count = optimize_considering_delay(
            delay=delay,
            tau_nom=tau_nom,
            gamma_d=gamma_d,
            s_load=s_load,
            vdd=vdd,
            c_min=c_min,
            gamma_e=gamma_e,
            s0=s0,
            max_iter=max_iter
        )
        optimal_results.append((delay, variables, energy_value, iteration_count))
        s1_from_python.append(variables[0])
        s2_from_python.append(variables[1])
        delay_values.append(delay)

    plt.plot(delay_values, s1_from_python, label='S1')
    plt.plot(delay_values, s2_from_python, label='S2')
    plt.legend()
    plt.xlabel('Delay')
    plt.ylabel('Factor Sizing')
    plt.title('Optimal Factor Sizing Trend')
    save_image(image_path=os.path.join(images, "s1_s2_optimized.png"), plt=plt)
    plt.show()

    delay_optmization_analysis = []
    optimal_point_optmization_analysis = []
    objective_f_value_optmization_analysis = []
    iterations_optmization_analysis = []
    for delay, variables, energy_value, iteration_count in optimal_results:
        delay_optmization_analysis.append(delay)
        optimal_point_optmization_analysis.append(str(variables))
        objective_f_value_optmization_analysis.append(energy_value)
        iterations_optmization_analysis.append(iteration_count)

    data_table_optimization_analysis = {
        'delay': delay_optmization_analysis,
        'optimal_point': optimal_point_optmization_analysis,
        'objective_f_value': objective_f_value_optmization_analysis,
        'iterations': iterations_optmization_analysis
    }
    table_creation(
        data_table=data_table_optimization_analysis,
        title_plot="Optimization Analysis",
        title_image_saving="table_optimization_analysis.png",
        figsize=[18, 12]
    )

    delay_optimization_analysis_file_path = os.path.join(data, 'out', 'optimization', 'delay_optimization_analysis.txt')
    with open(delay_optimization_analysis_file_path, 'w') as file:
        for val in delay_optmization_analysis:
            file.write(f'{val}\n')

    s1_optimization_analysis_file_path = os.path.join(data, 'out', 'optimization', 's1_optimization_analysis.txt')
    with open(s1_optimization_analysis_file_path, 'w') as file:
        for val in s1_from_python:
            file.write(f'{val}\n')

    s2_optimization_analysis_file_path = os.path.join(data, 'out', 'optimization', 's2_optimization_analysis.txt')
    with open(s2_optimization_analysis_file_path, 'w') as file:
        for val in s2_from_python:
            file.write(f'{val}\n')

    """Optimization unconstrained by 2 variables, S1 and S2, can be performed using the scipy.minimise optimization 
    algorithm. Specifically, the SLSQP algorithm was chosen, which performs a non-linear optimization and, 
    in addition, 2 constraints on the delay were considered: one of equality and one of inequality. The parameters 
    used, scaled appropriately, are those previously calculated. It must be specified that an initial point S0 was 
    chosen for the optimization, assuming, therefore, that the initial scaling factors S1 and S2 are both equal to 
    10. Furthermore, it has been specified that the maximum number of iterations of the algorithm, 
    for each optimization performed, is equal to 10000. Therefore, considering a delay range [d_max,d_min] = [510,
    100] to obtain a better optimization scaling of the sizing, we will obtain d_max-d_min/step, where step=10 is the 
    optimization step between one delay considered and the next, optimum sizing factors considering the design 
    parameters calculated previously."""


if __name__ == "__main__":
    optimization_analysis()
