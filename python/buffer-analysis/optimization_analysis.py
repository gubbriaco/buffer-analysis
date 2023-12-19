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


if __name__ == "__main__":
    optimization_analysis()
