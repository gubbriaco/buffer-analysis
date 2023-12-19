import os
from utils.paths import matlab, data
from utils.dir import get_values_from_file


def optimization_analysis_matlab():
    data_to_matlab_file_path = os.path.join(matlab, "buffer_data.txt")

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

    d_max = 510
    d_min = 100

    with open(data_to_matlab_file_path, "w") as file:
        file.truncate(0)
        file.write(f"{vdd}\n")
        file.write(f"{c_min}\n")
        file.write(f"{gamma_e}\n")
        file.write(f"{tau_nom}\n")
        file.write(f"{gamma_d}\n")
        file.write(f"{s_load}\n")
        file.write(f"{s0[0]}\n")
        file.write(f"{s0[1]}\n")
        file.write(f"{d_max}\n")
        file.write(f"{d_min}\n")

    print(f"Variables written successfully: {data_to_matlab_file_path}")
    print("#### Open MATLAB and execute the 'optimisation.m' script and then return here in Python to execute the "
          "associated subsequent plots. ####")


if __name__ == "__main__":
    optimization_analysis_matlab()
