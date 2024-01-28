import os
import csv
import torch

# Import your embedding and token calculation functions here
from embeddings import encode_java_code, calculate_tokens

def load_design_patterns(design_patterns_csv):
    design_pattern_dict = {}
    with open(design_patterns_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) >= 3:  # Ensure there are at least three columns in a row
                package_name = row[0]
                class_name = row[1]
                design_pattern = row[2]
                # Concatenate package name and class name to form the file name
                file_name = f"{package_name}.{class_name}"
                design_pattern_dict[file_name] = design_pattern
    return design_pattern_dict

def save_to_csv(root_directory, output_csv, design_patterns_csv):
    design_pattern_dict = load_design_patterns(design_patterns_csv)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Modify the header to include separate columns for each embedding feature
        header = ["Directory", "File", "DesignPattern"] + [f"Feature_{i}" for i in range(300)]
        csv_writer.writerow(header)  # Write the modified header

        for root, dirs, files in os.walk(root_directory):
            for file_name in files:
                if file_name.endswith('.java'):  # Change the file extension as needed
                    file_path = os.path.join(root, file_name)

                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()

                    if calculate_tokens(file_content) < 2400:
                        # Extract the directory name from the path
                        directory_name = os.path.basename(root)

                        # Remove the ".java" extension from the file name
                        file_base_name = os.path.splitext(file_name)[0]

                        # Form the complete file name (package name + class name)
                        complete_file_name = f"{directory_name}.{file_base_name}"

                        # Look up the design pattern for the current file
                        design_pattern = design_pattern_dict.get(complete_file_name, "Unknown")

                        # Embed the file content using your custom embedding function
                        file_embeddings = encode_java_code(file_content)

                        # Convert the tensor to a Python list
                        file_embeddings_list = file_embeddings.tolist()

                        # Write the directory name, file name (without extension), design pattern, and embeddings to the CSV
                        row = [directory_name, file_base_name, design_pattern] + file_embeddings_list
                        csv_writer.writerow(row)

if __name__ == "__main__":
    root_directory = "data_java"  # Replace with the root directory containing your files
    output_csv = "dataset_original.csv"  # Specify the output CSV file name
    design_patterns_csv = "input-13000.csv"  # Specify the path to the design patterns CSV file

    save_to_csv(root_directory, output_csv, design_patterns_csv)

    print(f"Dataset saved to {output_csv}")
