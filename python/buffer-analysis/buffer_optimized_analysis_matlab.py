import os
import matplotlib.pyplot as plt
from PyLTSpice import SimRunner
from models.ops import load_asc, load_ltr, energy_connected, rise_delay_connected, fall_delay_connected, save_image
from properties import l_min_pmos, l_min_nmos, w_min_nmos, S_LOAD, tran, rit_models
from utils.paths import ltspice, images, data, matlab
from utils.dir import get_values_from_file
from utils.patterns import energy_connected_pattern, rise_delay_connected_pattern, fall_delay_connected_pattern
import re


def buffer_optimized_analysis_matlab():
    w_min_pmos_file_path = os.path.join(data, 'out', 'minimum-inverter', 'get_sizing', 'w_min_pmos.txt')
    values = []
    with open(w_min_pmos_file_path, 'r') as file:
        values = [line.strip() for line in file]
    w_min_pmos = values[0]

    d_max = 510
    d_min = 100
    step_opt = 10

    data_from_matlab_directory = f"{matlab}/data"
    s1_data_from_matlab_file = "s1_data.txt"
    s2_data_from_matlab_file = "s2_data.txt"
    s1_data_from_matlab_file_path = os.path.join(data_from_matlab_directory, s1_data_from_matlab_file)
    s2_data_from_matlab_file_path = os.path.join(data_from_matlab_directory, s2_data_from_matlab_file)
    with open(s1_data_from_matlab_file_path, 'r') as s1_file:
        s1_lines = s1_file.readlines()
    with open(s2_data_from_matlab_file_path, 'r') as s2_file:
        s2_lines = s2_file.readlines()

    s1_from_matlab = []
    s2_from_matlab = []

    for line in s1_lines:
        columns = line.split()
        if columns:
            s1_value = columns[0]
            s1_from_matlab.append(float(s1_value))
    for line in s2_lines:
        columns = line.split()
        if columns:
            s2_value = columns[0]
            s2_from_matlab.append(float(s2_value))

    buffer_optimized_netlist = load_asc(
        asc_file_path=os.path.join(ltspice, "buffer/optimized/buffer_optimized.asc"),
        schematic_image_path=os.path.join(images, "buffer_optimized.png")
    )
    n_runs_optimized = ((d_max - d_min) / step_opt) + 1

    tmp_s1_from_matlab = [(str(var1) + "," if var1 != s1_from_matlab[len(s1_from_matlab) - 1] else str(var1)) for var1
                          in s1_from_matlab]
    s1_table_optimized_from_matlab = ""
    for item in tmp_s1_from_matlab:
        s1_table_optimized_from_matlab = s1_table_optimized_from_matlab + item
    tmp_s2_from_matlab = [(str(var2) + "," if var2 != s2_from_matlab[len(s2_from_matlab) - 1] else str(var2)) for var2
                          in s2_from_matlab]
    s2_table_optimized_from_matlab = ""
    for item in tmp_s2_from_matlab:
        s2_table_optimized_from_matlab = s2_table_optimized_from_matlab + item

    S1_optimized = f' table(index,{s1_table_optimized_from_matlab})'
    S2_optimized = f' table(index,{s2_table_optimized_from_matlab})'

    buffer_optimized_netlist.set_parameter('l_min_pmos', l_min_pmos)
    buffer_optimized_netlist.set_parameter('w_min_pmos', w_min_pmos)
    buffer_optimized_netlist.set_parameter('l_min_nmos', l_min_nmos)
    buffer_optimized_netlist.set_parameter('w_min_nmos', w_min_nmos)
    buffer_optimized_netlist.set_parameter('S1', S1_optimized)
    buffer_optimized_netlist.set_parameter('S2', S2_optimized)
    buffer_optimized_netlist.set_parameter('S_LOAD', S_LOAD)
    buffer_optimized_netlist.add_instructions(
        rit_models,
        tran,
        f".step param index 1 {n_runs_optimized} 1",
        energy_connected(13, 22),
        rise_delay_connected(),
        fall_delay_connected()
    )
    buffer_optimized_runner = SimRunner(output_folder=f"{data}/in/buffer/optimized/")
    buffer_optimized_runner.run(buffer_optimized_netlist)

    buffer_optimized_raw = ""
    buffer_optimized_log = ""
    for buffer_optimized_raw, buffer_optimized_log in buffer_optimized_runner:
        print("Raw file: %s, Log file: %s" % (buffer_optimized_raw, buffer_optimized_log))

    buffer_optimized_ltr = load_ltr(raw_file_path=buffer_optimized_raw)

    v_in_buffer_optimized = buffer_optimized_ltr.get_trace("V(in)")
    v_out_buffer_optimized = buffer_optimized_ltr.get_trace("V(out)")
    v_supply_buffer_optimized = buffer_optimized_ltr.get_trace("V(supply)")
    time = buffer_optimized_ltr.get_trace('time')
    steps = buffer_optimized_ltr.get_steps()

    plt.figure(figsize=(16, 4))
    for step in range(len(steps)):
        plt.plot(time.get_wave(step), v_in_buffer_optimized.get_wave(step), label=steps[step], color='blue')
        plt.plot(time.get_wave(step), v_out_buffer_optimized.get_wave(step), label=steps[step], color='red')
        plt.plot(time.get_wave(step), v_supply_buffer_optimized.get_wave(step), label=steps[step], color='green')
    plt.legend(["V(in)", "V(out)", "V(supply)"])
    save_image(image_path=os.path.join(images, "buffer_optimized_simulation.png"), plt=plt)
    plt.show()

    buffer_optimized_log_file_path = f"./{buffer_optimized_log}"
    with open(buffer_optimized_log_file_path, "r") as file:
        content = file.read()

    energy_connected_buffer_optimized_data = re.search(energy_connected_pattern, content, re.DOTALL).group(1)
    rise_delay_connected_buffer_optimized_data = re.search(rise_delay_connected_pattern, content, re.DOTALL).group(1)
    fall_delay_connected_buffer_optimized_data = re.search(fall_delay_connected_pattern, content, re.DOTALL).group(1)

    energy_connected_buffer_optimized_lines = energy_connected_buffer_optimized_data.strip().split('\n')[1:]
    rise_delay_connected_buffer_optimized_lines = rise_delay_connected_buffer_optimized_data.strip().split('\n')[1:]
    fall_delay_connected_buffer_optimized_lines = fall_delay_connected_buffer_optimized_data.strip().split('\n')[1:]

    energy_connected_buffer_optimized = [float(line.split('\t')[1]) for line in energy_connected_buffer_optimized_lines]
    energy_connected_buffer_optimized = [abs(energy) for energy in energy_connected_buffer_optimized]
    energy_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized', 'matlab',
                                                              'energy_connected_buffer_optimized_analysis.txt')
    with open(energy_connected_buffer_optimized_analysis_file_path, 'w') as file:
        for val in energy_connected_buffer_optimized:
            file.write(f'{val}\n')

    rise_delay_connected_buffer_optimized = [float(line.split('\t')[1]) for line in
                                             rise_delay_connected_buffer_optimized_lines]
    rise_delay_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized', 'matlab',
                                                              'rise_delay_connected_buffer_optimized_analysis.txt')
    with open(rise_delay_connected_buffer_optimized_analysis_file_path, 'w') as file:
        for val in rise_delay_connected_buffer_optimized:
            file.write(f'{val}\n')

    fall_delay_connected_buffer_optimized = [float(line.split('\t')[1]) for line in
                                             fall_delay_connected_buffer_optimized_lines]
    fall_delay_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized', 'matlab',
                                                              'fall_delay_connected_buffer_optimized_analysis.txt')
    with open(fall_delay_connected_buffer_optimized_analysis_file_path, 'w') as file:
        for val in fall_delay_connected_buffer_optimized:
            file.write(f'{val}\n')

    delay_connected_buffer_optimized = [(rise_delay + fall_delay) / 2 for rise_delay, fall_delay in
                                        zip(rise_delay_connected_buffer_optimized,
                                            fall_delay_connected_buffer_optimized)]
    delay_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized', 'matlab',
                                                              'delay_connected_buffer_optimized_analysis.txt')
    with open(delay_connected_buffer_optimized_analysis_file_path, 'w') as file:
        for val in delay_connected_buffer_optimized:
            file.write(f'{val}\n')


if __name__ == "__main__":
    buffer_optimized_analysis_matlab()