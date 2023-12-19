import statistics as st
from utils.conversion import to_order, Order
from utils.dir import get_values_from_file
from utils.paths import data
from models.ops import table_creation
import os


def params_analysis():
    energy_connected_minimum_inverter_file_path = os.path.join(
        data, 'out', 'minimum-inverter', 'connected', 'energy_connected_minimum_inverter_analysis.txt'
    )
    energy_connected_minimum_inverter = get_values_from_file(file_path=energy_connected_minimum_inverter_file_path)

    energy_disconnected_minimum_inverter_file_path = os.path.join(
        data, 'out', 'minimum-inverter', 'disconnected', 'energy_disconnected_minimum_inverter_analysis.txt'
    )
    energy_disconnected_minimum_inverter = get_values_from_file(file_path=energy_disconnected_minimum_inverter_file_path)

    delay_disconnected_minimum_inverter_file_path = os.path.join(
        data, 'out', 'minimum-inverter', 'disconnected', 'delay_disconnected_minimum_inverter_analysis.txt'
    )
    delay_disconnected_minimum_inverter = get_values_from_file(file_path=delay_disconnected_minimum_inverter_file_path)

    delay_connected_buffer_file_path = os.path.join(
        data, 'out', 'buffer', 'standard', 'delay_connected_buffer_analysis.txt'
    )
    delay_connected_buffer = get_values_from_file(file_path=delay_connected_buffer_file_path)

    s1_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard', 's1_buffer_analysis.txt')
    s1 = get_values_from_file(s1_buffer_analysis_file_path)

    s2_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard', 's2_buffer_analysis.txt')
    s2 = get_values_from_file(s2_buffer_analysis_file_path)

    vdd = 1
    vdd_file_path = os.path.join(data, 'out', 'params', 'vdd_analysis.txt')
    with open(vdd_file_path, 'w') as file:
        file.write(f'{vdd}\n')

    c_tot = [energy / (vdd * vdd) for energy in energy_connected_minimum_inverter]
    c_tot_file_path = os.path.join(data, 'out', 'params', 'c_tot_analysis.txt')
    with open(c_tot_file_path, 'w') as file:
        for val in c_tot:
            file.write(f'{val}\n')

    c_out = [energy / (vdd * vdd) for energy in energy_disconnected_minimum_inverter]
    c_out_file_path = os.path.join(data, 'out', 'params', 'c_out_analysis.txt')
    with open(c_out_file_path, 'w') as file:
        for val in c_out:
            file.write(f'{val}\n')

    c_in = [c_tot - c_out for c_tot, c_out in zip(c_tot, c_out)]
    c_in_file_path = os.path.join(data, 'out', 'params', 'c_in_analysis.txt')
    with open(c_in_file_path, 'w') as file:
        for val in c_in:
            file.write(f'{val}\n')

    c_min = c_in[0]
    print(f"c_min = {c_min}")
    c_min_file_path = os.path.join(data, 'out', 'params', 'c_min_analysis.txt')
    with open(c_min_file_path, 'w') as file:
        file.write(f'{c_min}\n')

    c_min_for_optimization = to_order(c_min, Order.FEMTO)
    c_min_for_optimization_file_path = os.path.join(data, 'out', 'params', 'c_min_for_optimization_analysis.txt')
    with open(c_min_for_optimization_file_path, 'w') as file:
        file.write(f'{c_min_for_optimization}\n')
    print(f"c_min_for_optimization = {c_min_for_optimization}")

    gamma_e = [c_out / c_in for c_out, c_in in zip(c_out, c_in)]
    print(f"gamma_e_max = {max(gamma_e)}")
    print(f"gamma_e_min = {min(gamma_e)}")
    gamma_e = st.mean(gamma_e)
    print(f"gamma_e = {gamma_e}")
    gamma_e_file_path = os.path.join(data, 'out', 'params', 'gamma_e_analysis.txt')
    with open(gamma_e_file_path, 'w') as file:
        file.write(f'{gamma_e}\n')

    """Considering that E = C * Vdd^2 then it is possible to derive the capacity with the inverse formula: C = E / 
    Vdd^2. Therefore, the total capacity c_tot will be obtained by considering the energy associated with the minimum 
    connected inverter, the output capacity c_out will be obtained by considering the energy associated with the 
    minimum disconnected inverter, and finally, the input capacity c_in is obtained via the difference between the 
    total capacity c_tot and the output capacity c_out. Therefore, the gamma_e parameter can be calculated via the 
    ratio of the intrinsic output capacitance c_out to the input capacitance c_in."""

    tau_nom = delay_disconnected_minimum_inverter
    tau_nom = st.mean(tau_nom)
    print(f"tau_nom = {tau_nom}")
    tau_nom_file_path = os.path.join(data, 'out', 'params', 'tau_nom_analysis.txt')
    with open(tau_nom_file_path, 'w') as file:
        file.write(f'{tau_nom}\n')

    tau_nom_for_optimization = to_order(tau_nom, Order.PICO)
    print(f"tau_nom_for_optimization = {tau_nom_for_optimization}")
    tau_nom_for_optimization_file_path = os.path.join(data, 'out', 'params', 'tau_nom_for_optimization_analysis.txt')
    with open(tau_nom_for_optimization_file_path, 'w') as file:
        file.write(f'{tau_nom_for_optimization}\n')

    tau_tot = delay_connected_buffer
    tau_tot_file_path = os.path.join(data, 'out', 'params', 'tau_tot_analysis.txt')
    with open(tau_tot_file_path, 'w') as file:
        for val in tau_tot:
            file.write(f'{val}\n')

    s_load = 50
    s_load_file_path = os.path.join(data, 'out', 'params', 's_load_analysis.txt')
    with open(s_load_file_path, 'w') as file:
        file.write(f'{s_load}\n')

    temp1 = [tau_nom / (tau_tot - (3 * tau_nom)) for tau_tot in tau_tot]
    temp2 = [s1 + (s2 / s1) + (s_load / s2) for s1, s2 in zip(s1, s2)]
    gamma_d = [tmp1 * tmp2 for tmp1, tmp2 in zip(temp1, temp2)]
    print(f"gamma_d_max = {max(gamma_d)}")
    print(f"gamma_d_min = {min(gamma_d)}")
    gamma_d = st.mean(gamma_d)
    print(f"gamma_d = {gamma_d}")
    gamma_d_file_path = os.path.join(data, 'out', 'params', 'gamma_d_analysis.txt')
    with open(gamma_d_file_path, 'w') as file:
        file.write(f'{gamma_d}\n')

    """The parameter tau_nom is equal to the delay associated with the minimum disconnected inverter. Specifically, 
    the latter is obtained by averaging the rise time and the fall time of the inverter itself. The tau_tot, 
    on the other hand, is equal to the delay associated with the connected buffer where the latter is calculated as 
    the average between the rise time and the fall time of the buffer itself. Therefore, considering a load inverter 
    sizing factor of 50, through the delay model associated with the 3-stage buffer, the associated gamma_d can be 
    calculated."""

    tmp1 = []
    tmp1.append(c_min)
    tmp2 = []
    tmp2.append(gamma_e)
    tmp3 = []
    tmp3.append(tau_nom)
    tmp4 = []
    tmp4.append(gamma_d)
    data_table_params_analysis = {
        'c_min': tmp1,
        'gamma_e': tmp2,
        'tau_nom': tmp3,
        'gamma_d': tmp4
    }
    table_creation(
        data_table=data_table_params_analysis,
        title_plot="Params Analysis",
        title_image_saving="table_params_analysis.png",
        figsize=[18, 4]
    )


if __name__ == "__main__":
    params_analysis()
