from utils.paths import matlab, images, data
from utils.dir import get_values_from_file
from models.ops import save_image, table_creation
import os
from matplotlib import pyplot as plt


def optimization_plotting_matlab():
    delay_values_file_path = os.path.join(data, 'out', 'optimization', 'delay_optimization_analysis.txt')
    delay_values = get_values_from_file(delay_values_file_path)

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

    plt.plot(delay_values, s1_from_matlab, label='S1')
    plt.plot(delay_values, s2_from_matlab, label='S2')
    plt.legend()
    plt.xlabel('Delay')
    plt.ylabel('Factor Sizing')
    plt.title('Optimal Factor Sizing Trend from MATLAB')
    save_image(image_path=os.path.join(images, "s1_s2_matlab_optimized.png"), plt=plt)
    plt.show()

    data_table_optimization_analysis_matlab = {
        'delay': delay_values,
        's1_from_matlab': s1_from_matlab,
        's2_from_matlab': s2_from_matlab
    }
    table_creation(
        data_table=data_table_optimization_analysis_matlab,
        title_plot="Optimization Analysis MATLAB",
        title_image_saving="table_optimization_analysis_matlab.png",
        figsize=[18, 12]
    )

    s1_from_python_file_path = os.path.join(data, 'out', 'optimization', 's1_optimization_analysis.txt')
    s1_from_python = get_values_from_file(s1_from_python_file_path)

    s2_from_python_file_path = os.path.join(data, 'out', 'optimization', 's2_optimization_analysis.txt')
    s2_from_python = get_values_from_file(s2_from_python_file_path)

    data_table_optimization_analysis_matlab_comparative_python = {
        'delay': delay_values,
        's1_from_python': s1_from_python,
        's1_from_matlab': s1_from_matlab,
        's2_from_python': s2_from_python,
        's2_from_matlab': s2_from_matlab
    }
    table_creation(
        data_table=data_table_optimization_analysis_matlab_comparative_python,
        title_plot="Optimization Analysis MATLAB vs Python",
        title_image_saving="table_optimization_analysis_matlab_comparative_python.png",
        figsize=[22, 12]
    )

    s1_error = []
    s2_error = []
    for (
            delay,
            s1_python,
            s2_python,
            s1_matlab,
            s2_matlab
    ) in zip(
        delay_values,
        s1_from_python,
        s2_from_python,
        s1_from_matlab,
        s2_from_matlab
    ):
        s1_error_current = abs(s1_python - s1_matlab)
        s2_error_current = abs(s2_python - s2_matlab)
        s1_error.append(s1_error_current)
        s2_error.append(s2_error_current)

    data_table_optimization_analysis_comparative_accuracy = {
        'delay': delay_values,
        's1_error': s1_error,
        's2_error': s2_error
    }
    table_creation(
        data_table=data_table_optimization_analysis_comparative_accuracy,
        title_plot="Optimization Analysis MATLAB vs Python Accuracy",
        title_image_saving="table_optimization_analysis_comparative_accuracy.png",
        figsize=[18, 12]
    )

    plt.plot(delay_values, s1_error, label='S1-error')
    plt.plot(delay_values, s2_error, label='S2-error')
    plt.legend()
    plt.xlabel('Delay')
    plt.ylabel('Error Factor Sizing')
    plt.title('Optimization Analysis MATLAB vs Python Accuracy')
    save_image(image_path=os.path.join(images, "s_optimized_error.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    optimization_plotting_matlab()
