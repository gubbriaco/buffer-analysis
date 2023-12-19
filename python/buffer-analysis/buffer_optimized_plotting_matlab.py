from utils.paths import images, data
from utils.dir import get_values_from_file
from matplotlib import pyplot as plt
from models.ops import save_image, table_creation
import os


def buffer_optimized_plotting_matlab():
    delay_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                             'delay_connected_buffer_analysis.txt')
    delay_connected_buffer = get_values_from_file(delay_connected_buffer_analysis_file_path)
    energy_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                              'energy_connected_buffer_analysis.txt')
    energy_connected_buffer = get_values_from_file(energy_connected_buffer_analysis_file_path)

    delay_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized', 'matlab',
                                                                       'delay_connected_buffer_optimized_analysis.txt')
    delay_connected_buffer_optimized = get_values_from_file(delay_connected_buffer_optimized_analysis_file_path)
    energy_connected_buffer_optimized_analysis_file_path = os.path.join(data, 'out', 'buffer', 'optimized', 'matlab',
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
    save_image(image_path=os.path.join(images, "comparative_analysis_matlab.png"), plt=plt)
    plt.show()
    """It can be seen that the Pareto optimal curve obtained via MATLAB's optimal dimensioning factors better 
    approximates the hypothetical empirical curve than the one generated via the scipy.minimise optimisation 
    algorithm."""

    delay_connected_buffer_optimized_matlab = delay_connected_buffer_optimized
    energy_connected_buffer_optimized_matlab = energy_connected_buffer_optimized

    delay_values_file_path = os.path.join(data, 'out', 'optimization', 'delay_optimization_analysis.txt')
    delay_values = get_values_from_file(delay_values_file_path)
    delay_connected_buffer_optimized_analysis_python_file_path = os.path.join(data, 'out', 'buffer', 'optimized',
                                                                       'delay_connected_buffer_optimized_analysis.txt')
    delay_connected_buffer_optimized_python = get_values_from_file(delay_connected_buffer_optimized_analysis_python_file_path)
    energy_connected_buffer_optimized_analysis_python_file_path = os.path.join(data, 'out', 'buffer', 'optimized',
                                                                        'energy_connected_buffer_optimized_analysis.txt')
    energy_connected_buffer_optimized_python = get_values_from_file(energy_connected_buffer_optimized_analysis_python_file_path)

    data_table_optimization_comparative_matlab_python = {
        'delay': delay_values,
        'delay_from_python': delay_connected_buffer_optimized_python,
        'delay_from_matlab': delay_connected_buffer_optimized_matlab,
        'energy_from_python': energy_connected_buffer_optimized_python,
        'energy_from_matlab': energy_connected_buffer_optimized_matlab
    }
    table_creation(
        data_table=data_table_optimization_comparative_matlab_python,
        title_plot="Optimization Analysis MATLAB vs Python",
        title_image_saving="table_optimization_analysis_comparative_matlab_python.png",
        figsize=[22, 12]
    )

    delay_error = []
    energy_error = []
    for (
            delay,
            delay_python,
            energy_python,
            delay_matlab,
            energy_matlab
    ) in zip(
        delay_values,
        delay_connected_buffer_optimized_python,
        energy_connected_buffer_optimized_python,
        delay_connected_buffer_optimized_matlab,
        energy_connected_buffer_optimized_matlab
    ):
        delay_error_current = abs(delay_python - delay_matlab)
        energy_error_current = abs(energy_python - energy_matlab)
        delay_error.append(delay_error_current)
        energy_error.append(energy_error_current)

    data_table_optimization_comparative_matlab_python_accuracy = {
        'delay': delay_values,
        'delay_error': delay_error,
        'energy_error': energy_error
    }
    table_creation(
        data_table=data_table_optimization_comparative_matlab_python_accuracy,
        title_plot="Optimization Analysis MATLAB vs Python Accuracy",
        title_image_saving="table_optimization_analysis_comparative_matlab_python_accuracy.png",
        figsize=[22, 12]
    )

    plt.plot(delay_values, delay_error, label='delay-error')
    plt.plot(delay_values, energy_error, label='energy-error')
    plt.legend()
    plt.xlabel('Delay')
    plt.ylabel('Energy-Delay Error')
    plt.title('Energy-Delay Buffer Optimized MATLAB vs Python Error')
    save_image(image_path=os.path.join(images, "energy_delay_error.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    buffer_optimized_plotting_matlab()
