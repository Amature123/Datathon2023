import pandas as pd

# Define the directory path where your CSV files are stored

directory_path = "path_to_your_csv_files"

# Iterate through the CSV files in the directory

for filename in os.listdir(directory_path):

    # Check if the file is a CSV file

    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)

        # Load the CSV file into a DataFrame

        df = pd.read_csv(file_path)

        # Perform any data transformations or concatenation operations
        

        # Save the concatenated DataFrame to a new CSV file

        df.to_csv("concatenated_output.csv", index=False)