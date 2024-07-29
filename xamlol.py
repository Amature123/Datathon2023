import os
filepath = "./InventoryAndSale_snapshot_data/Sales_snapshot_data"
for i,file in enumerate(os.listdir(filepath)):
# Extract the date from the file name
  old_file_path = os.path.join(filepath, file)
  # New file name
  new_file_name = f"TT{i}.csv"
  new_file_path = os.path.join(filepath, new_file_name)
  # Rename the file
  os.rename(old_file_path, new_file_name)

  print(f"File '{file}' renamed to '{new_file_name}'")