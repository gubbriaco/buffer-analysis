import os
import matplotlib.pyplot as plt
from PyLTSpice import SimRunner
from models.ops import load_asc, load_ltr, energy_connected, rise_delay_connected, fall_delay_connected, save_image
from properties import nr_runs, l_min_pmos, l_min_nmos, w_min_nmos, S1, S2, S_LOAD, tran, rit_models, save_s1, save_s2
from utils.paths import data
from utils.paths import ltspice, images
from utils.patterns import (s1_pattern, s2_pattern, energy_connected_pattern, rise_delay_connected_pattern,
                            fall_delay_connected_pattern)
import re


def buffer_analysis():
    """
    The buffer considered for the analysis of this project is a 3-stage chain inverter where the first inverter
    corresponds to the minimum sized inverter according to the previous analysis, the second inverter is sized S1
    times the minimum inverter and the third inverter is sized S2 times the minimum inverter. Specifically,
    S1 and S2 are parameters defined according to Monte Carlo experiments. It must be specified that, to carry out
    the analysis, the buffer is connected to a load inverter sized 50 times the minimum inverter.
    :return:
    """

    w_min_pmos_file_path = os.path.join(data, 'out', 'minimum-inverter', 'get_sizing', 'w_min_pmos.txt')
    values = []
    with open(w_min_pmos_file_path, 'r') as file:
        values = [line.strip() for line in file]
    w_min_pmos = values[0]

    buffer_netlist = load_asc(
        asc_file_path=os.path.join(ltspice, "buffer/standard/buffer.asc"),
        schematic_image_path=os.path.join(images, "buffer.png")
    )
    buffer_netlist.set_parameter('l_min_pmos', l_min_pmos)
    buffer_netlist.set_parameter('w_min_pmos', w_min_pmos)
    buffer_netlist.set_parameter('l_min_nmos', l_min_nmos)
    buffer_netlist.set_parameter('w_min_nmos', w_min_nmos)
    buffer_netlist.set_parameter('S1', S1)
    buffer_netlist.set_parameter('S2', S2)
    buffer_netlist.set_parameter('S_LOAD', S_LOAD)
    buffer_netlist.add_instructions(
        rit_models,
        tran,
        f".step param run 1 {nr_runs} 1",
        save_s1,
        save_s2,
        energy_connected(13, 22),
        rise_delay_connected(),
        fall_delay_connected()
    )
    buffer_runner = SimRunner(output_folder=f"{data}/in/buffer/standard/")
    buffer_runner.run(netlist=buffer_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(buffer_runner.okSim) + '/' + str(buffer_runner.runno))

    buffer_raw = ""
    buffer_log = ""
    for buffer_raw, buffer_log in buffer_runner:
        print("Raw file: %s, Log file: %s" % (buffer_raw, buffer_log))

    buffer_ltr = load_ltr(raw_file_path=buffer_raw)
    v_in_buffer = buffer_ltr.get_trace("V(in)")
    v_out_buffer = buffer_ltr.get_trace("V(out)")
    v_supply_buffer = buffer_ltr.get_trace("V(supply)")
    time = buffer_ltr.get_trace('time')
    steps = buffer_ltr.get_steps()

    plt.figure(figsize=(16, 4))
    for step in range(len(steps)):
        plt.plot(time.get_wave(step), v_in_buffer.get_wave(step), label=steps[step], color='blue')
        plt.plot(time.get_wave(step), v_out_buffer.get_wave(step), label=steps[step], color='red')
        plt.plot(time.get_wave(step), v_supply_buffer.get_wave(step), label=steps[step], color='green')
    plt.legend(["V(in)", "V(out)", "V(supply)"])
    save_image(image_path=os.path.join(images, "buffer_simulation.png"), plt=plt)
    plt.show()

    buffer_log_file_path = f"./{buffer_log}"

    with open(buffer_log_file_path, "r") as file:
        content = file.read()

    s1_data = re.search(s1_pattern, content, re.DOTALL).group(1)
    s2_data = re.search(s2_pattern, content, re.DOTALL).group(1)
    energy_connected_buffer_data = re.search(energy_connected_pattern, content, re.DOTALL).group(1)
    rise_delay_connected_buffer_data = re.search(rise_delay_connected_pattern, content, re.DOTALL).group(1)
    fall_delay_connected_buffer_data = re.search(fall_delay_connected_pattern, content, re.DOTALL).group(1)

    s1_lines = s1_data.strip().split('\n')[1:]
    s2_lines = s2_data.strip().split('\n')[1:]
    energy_connected_buffer_lines = energy_connected_buffer_data.strip().split('\n')[1:]
    rise_delay_connected_buffer_lines = rise_delay_connected_buffer_data.strip().split('\n')[1:]
    fall_delay_connected_buffer_lines = fall_delay_connected_buffer_data.strip().split('\n')[1:]

    s1 = [float(line.split('\t')[1]) for line in s1_lines]
    s1_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard', 's1_buffer_analysis.txt')
    with open(s1_buffer_analysis_file_path, 'w') as file:
        for val in s1:
            file.write(f'{val}\n')
    s2 = [float(line.split('\t')[1]) for line in s2_lines]
    s2_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard', 's2_buffer_analysis.txt')
    with open(s2_buffer_analysis_file_path, 'w') as file:
        for val in s2:
            file.write(f'{val}\n')

    energy_connected_buffer = [float(line.split('\t')[1]) for line in energy_connected_buffer_lines]
    energy_connected_buffer = [abs(energy) for energy in energy_connected_buffer]
    energy_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                              'energy_connected_buffer_analysis.txt')
    with open(energy_connected_buffer_analysis_file_path, 'w') as file:
        for val in energy_connected_buffer:
            file.write(f'{val}\n')

    rise_delay_connected_buffer = [float(line.split('\t')[1]) for line in rise_delay_connected_buffer_lines]
    rise_delay_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                                  'rise_delay_connected_buffer_analysis.txt')
    with open(rise_delay_connected_buffer_analysis_file_path, 'w') as file:
        for val in rise_delay_connected_buffer:
            file.write(f'{val}\n')

    fall_delay_connected_buffer = [float(line.split('\t')[1]) for line in fall_delay_connected_buffer_lines]
    fall_delay_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                                  'fall_delay_connected_buffer_analysis.txt')
    with open(fall_delay_connected_buffer_analysis_file_path, 'w') as file:
        for val in fall_delay_connected_buffer:
            file.write(f'{val}\n')

    delay_connected_buffer = [(rise_delay + fall_delay) / 2 for rise_delay, fall_delay in
                              zip(rise_delay_connected_buffer, fall_delay_connected_buffer)]
    delay_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                             'delay_connected_buffer_analysis.txt')
    with open(delay_connected_buffer_analysis_file_path, 'w') as file:
        for val in delay_connected_buffer:
            file.write(f'{val}\n')


if __name__ == "__main__":
    buffer_analysis()
