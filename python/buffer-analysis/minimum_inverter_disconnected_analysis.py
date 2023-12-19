import os
from PyLTSpice import SimRunner
from models.ops import load_asc, energy_disconnected, rise_delay_disconnected, fall_delay_disconnected
from properties import l_min_pmos, l_min_nmos, w_min_nmos, tran, rit_models
from utils.paths import ltspice, images, data
from utils.patterns import energy_disconnected_pattern, rise_delay_disconnected_pattern, fall_delay_disconnected_pattern
import re


def minimum_inverter_disconnected_analysis():
    """
    The minimum disconnected inverter is used to calculate the energy, rise time and fall time from disconnected.
    These parameters will be used later for further analysis. Considering the inverter disconnected means considering
    the output OUT from the load inverter to be disconnected.
    :return:
    """
    w_min_pmos_file_path = os.path.join(data, 'out', 'minimum-inverter', 'get_sizing', 'w_min_pmos.txt')
    values = []
    with open(w_min_pmos_file_path, 'r') as file:
        values = [line.strip() for line in file]
    w_min_pmos = values[0]

    minimum_inverter_disconnected_netlist = load_asc(
        asc_file_path=os.path.join(ltspice, "minimum-inverter/disconnected/minimum_inverter_disconnected.asc"),
        schematic_image_path=os.path.join(images, "minimum_inverter_disconnected.png")
    )
    minimum_inverter_disconnected_netlist.set_parameter('l_min_pmos', l_min_pmos)
    minimum_inverter_disconnected_netlist.set_parameter('w_min_pmos', w_min_pmos)
    minimum_inverter_disconnected_netlist.set_parameter('l_min_nmos', l_min_nmos)
    minimum_inverter_disconnected_netlist.set_parameter('w_min_nmos', w_min_nmos)
    minimum_inverter_disconnected_netlist.add_instructions(
        rit_models,
        tran,
        ".step param run 1 2 1",
        energy_disconnected(18, 22),
        rise_delay_disconnected(),
        fall_delay_disconnected()
    )
    minimum_inverter_disconnected_runner = SimRunner(output_folder=f"{data}/in/minimum-inverter/disconnected/")
    minimum_inverter_disconnected_runner.run(minimum_inverter_disconnected_netlist)

    minimum_inverter_disconnected_raw = ""
    minimum_inverter_disconnected_log = ""
    for minimum_inverter_disconnected_raw, minimum_inverter_disconnected_log in minimum_inverter_disconnected_runner:
        print("Raw file: %s, Log file: %s" % (minimum_inverter_disconnected_raw, minimum_inverter_disconnected_log))

    minimum_inverter_disconnected_log_file_path = f"./{minimum_inverter_disconnected_log}"
    with open(minimum_inverter_disconnected_log_file_path, "r") as file:
        content = file.read()

    energy_disconnected_minimum_inverter_data = re.search(energy_disconnected_pattern, content, re.DOTALL).group(1)
    rise_delay_disconnected_minimum_inverter_data = re.search(rise_delay_disconnected_pattern, content,
                                                              re.DOTALL).group(1)
    fall_delay_disconnected_minimum_inverter_data = re.search(fall_delay_disconnected_pattern, content,
                                                              re.DOTALL).group(1)

    energy_disconnected_minimum_inverter_lines = energy_disconnected_minimum_inverter_data.strip().split('\n')[1:]
    rise_delay_disconnected_minimum_inverter_lines = rise_delay_disconnected_minimum_inverter_data.strip().split('\n')[
                                                     1:]
    fall_delay_disconnected_minimum_inverter_lines = fall_delay_disconnected_minimum_inverter_data.strip().split('\n')[
                                                     1:]

    energy_disconnected_minimum_inverter = [float(line.split('\t')[1]) for line in
                                            energy_disconnected_minimum_inverter_lines]
    energy_disconnected_minimum_inverter = [abs(energy) for energy in energy_disconnected_minimum_inverter]
    energy_disconnected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter', 'disconnected',
                                                                        'energy_disconnected_minimum_inverter_analysis.txt')
    with open(energy_disconnected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in energy_disconnected_minimum_inverter:
            file.write(f'{val}\n')

    rise_delay_disconnected_minimum_inverter = [float(line.split('\t')[1]) for line in
                                                rise_delay_disconnected_minimum_inverter_lines]
    rise_delay_disconnected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter', 'disconnected',
                                                                        'rise_delay_disconnected_minimum_inverter_analysis.txt')
    with open(rise_delay_disconnected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in rise_delay_disconnected_minimum_inverter:
            file.write(f'{val}\n')

    fall_delay_disconnected_minimum_inverter = [float(line.split('\t')[1]) for line in
                                                fall_delay_disconnected_minimum_inverter_lines]
    fall_delay_disconnected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter', 'disconnected',
                                                                        'fall_delay_disconnected_minimum_inverter_analysis.txt')
    with open(fall_delay_disconnected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in fall_delay_disconnected_minimum_inverter:
            file.write(f'{val}\n')

    delay_disconnected_minimum_inverter = [(rise_delay + fall_delay) / 2 for rise_delay, fall_delay in
                                           zip(rise_delay_disconnected_minimum_inverter,
                                               fall_delay_disconnected_minimum_inverter)]
    delay_disconnected_minimum_inverter_analysis_file_path = os.path.join(data, 'out', 'minimum-inverter', 'disconnected',
                                                                        'delay_disconnected_minimum_inverter_analysis.txt')
    with open(delay_disconnected_minimum_inverter_analysis_file_path, 'w') as file:
        for val in delay_disconnected_minimum_inverter:
            file.write(f'{val}\n')


if __name__ == "__main__":
    minimum_inverter_disconnected_analysis()
