import os
from PyLTSpice import SimRunner
from models.ops import load_asc, energy_connected, rise_delay_connected, fall_delay_connected
from properties import l_min_pmos, l_min_nmos, w_min_nmos, tran, rit_models
from utils.paths import ltspice, images, data
from utils.patterns import energy_connected_pattern, rise_delay_connected_pattern, fall_delay_connected_pattern
import re


def minimum_inverter_connected_analysis():
    w_min_pmos_file_path = os.path.join(data, 'out', 'minimum-inverter', 'get_sizing', 'w_min_pmos.txt')
    values = []
    with open(w_min_pmos_file_path, 'r') as file:
        values = [line.strip() for line in file]
    w_min_pmos = values[0]

    minimum_inverter_connected_netlist = load_asc(
        asc_file_path=os.path.join(ltspice, "minimum-inverter/connected/minimum_inverter_connected.asc"),
        schematic_image_path=os.path.join(images, "minimum_inverter_connected.png")
    )
    minimum_inverter_connected_netlist.set_parameter('l_min_pmos', l_min_pmos)
    minimum_inverter_connected_netlist.set_parameter('w_min_pmos', w_min_pmos)
    minimum_inverter_connected_netlist.set_parameter('l_min_nmos', l_min_nmos)
    minimum_inverter_connected_netlist.set_parameter('w_min_nmos', w_min_nmos)
    minimum_inverter_connected_netlist.add_instructions(
        rit_models,
        tran,
        ".step param run 1 2 1",
        energy_connected(18, 22),
        rise_delay_connected(),
        fall_delay_connected()
    )
    minimum_inverter_connected_runner = SimRunner(output_folder=f"{data}/in/minimum-inverter/connected/")
    minimum_inverter_connected_runner.run(minimum_inverter_connected_netlist)

    minimum_inverter_connected_raw = ""
    minimum_inverter_connected_log = ""
    for minimum_inverter_connected_raw, minimum_inverter_connected_log in minimum_inverter_connected_runner:
        print("Raw file: %s, Log file: %s" % (minimum_inverter_connected_raw, minimum_inverter_connected_log))

    minimum_inverter_connected_log_file_path = f"./{minimum_inverter_connected_log}"
    with open(minimum_inverter_connected_log_file_path, "r") as file:
        content = file.read()

    energy_connected_minimum_inverter_data = re.search(energy_connected_pattern, content, re.DOTALL).group(1)
    rise_delay_connected_minimum_inverter_data = re.search(rise_delay_connected_pattern, content, re.DOTALL).group(1)
    fall_delay_connected_minimum_inverter_data = re.search(fall_delay_connected_pattern, content, re.DOTALL).group(1)

    energy_connected_minimum_inverter_lines = energy_connected_minimum_inverter_data.strip().split('\n')[1:]
    rise_delay_connected_minimum_inverter_lines = rise_delay_connected_minimum_inverter_data.strip().split('\n')[1:]
    fall_delay_connected_minimum_inverter_lines = fall_delay_connected_minimum_inverter_data.strip().split('\n')[1:]

    energy_connected_minimum_inverter = [float(line.split('\t')[1]) for line in energy_connected_minimum_inverter_lines]
    energy_connected_minimum_inverter = [abs(energy) for energy in energy_connected_minimum_inverter]
    energy_connected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter', 'connected',
                                                                        'energy_connected_minimum_inverter_analysis.txt')
    with open(energy_connected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in energy_connected_minimum_inverter:
            file.write(f'{val}\n')

    rise_delay_connected_minimum_inverter = [float(line.split('\t')[1]) for line in
                                             rise_delay_connected_minimum_inverter_lines]
    rise_delay_connected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter',
                                                                            'connected',
                                                                            'rise_delay_connected_minimum_inverter_analysis.txt')
    with open(rise_delay_connected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in rise_delay_connected_minimum_inverter:
            file.write(f'{val}\n')

    fall_delay_connected_minimum_inverter = [float(line.split('\t')[1]) for line in
                                             fall_delay_connected_minimum_inverter_lines]
    fall_delay_connected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter',
                                                                            'connected',
                                                                            'fall_delay_connected_minimum_inverter_analysis.txt')
    with open(fall_delay_connected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in fall_delay_connected_minimum_inverter:
            file.write(f'{val}\n')


if __name__ == "__main__":
    minimum_inverter_connected_analysis()
