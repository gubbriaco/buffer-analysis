from utils.paths import images, data
from utils.dir import get_values_from_file
from matplotlib import pyplot as plt
from models.ops import save_image
import os


def buffer_optimized_plotting():
    """
    A comparative graphical analysis is carried out between the newly obtained optimal curve, via an optimisation
    algorithm, and the empirical analysis, previously obtained via Monte Carlo experiments.
    :return:
    """
    delay_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                             'delay_connected_buffer_analysis.txt')
    delay_connected_buffer = get_values_from_file(delay_connected_buffer_analysis_file_path)
    energy_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                              'energy_connected_buffer_analysis.txt')
    energy_connected_buffer = get_values_from_file(energy_connected_buffer_analysis_file_path)

    delay_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized',
                                                             'delay_connected_buffer_optimized_analysis.txt')
    delay_connected_buffer_optimized = get_values_from_file(delay_connected_buffer_optimized_analysis_file_path)
    energy_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized',
                                                              'energy_connected_buffer_optimized_analysis.txt')
    energy_connected_buffer_optimized = get_values_from_file(energy_connected_buffer_optimized_analysis_file_path)


    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    axs[0].plot(delay_connected_buffer_optimized, energy_connected_buffer_optimized, color='red')
    axs[0].set_xlabel('Delay')
    axs[0].set_ylabel('Energy')
    axs[0].set_title('Energy-Delay Curve')
    axs[0].legend(["Energy-Delay Curve"])

    axs[1].scatter(delay_connected_buffer, energy_connected_buffer, edgecolors='black')
    axs[1].plot(delay_connected_buffer_optimized, energy_connected_buffer_optimized, color='red')
    axs[1].set_xlabel('Delay')
    axs[1].set_ylabel('Energy')
    axs[1].set_title('Monte Carlo Experiments and Energy-Delay Curve')
    axs[1].legend(["Monte Carlo Experiments", "Energy-Delay Curve"])

    plt.tight_layout()
    save_image(image_path=os.path.join(images, "comparative_analysis.png"), plt=plt)
    plt.show()

    """It is possible to observe how the optimal curve obtained by means of the optimisation algorithm slightly 
    approximates the minimum points obtained by means of Monte Carlo experiments, i.e. the possible empirical curve 
    hypothesised to contour the minimum points of the scatter plot according to the reasoning previously made. It 
    must be specified that this possible optimal Pareto curve obtained by means of the optimisation algorithm depends 
    on the implementation of the algorithm itself and, therefore, with different algorithms one could obtain a better 
    approximation of the hypothesised empirical curve or even a worse one."""


if __name__ == "__main__":
    buffer_optimized_plotting()
