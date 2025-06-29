import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Path to the CSV file in the Downloads folder
csv_file_path = os.path.join("C:\\Users\\223106182\\Downloads", "waterData.csv")

# Initialize empty lists for date, time, and depth
dates = []
times = []
depths = []

# Open and read the CSV file
with open(csv_file_path, "r") as file:
    reader = csv.reader(file, delimiter="\t")  # Use tab as the delimiter
    for row in reader:
        # Skip rows that are comments or headers
        if row[0].startswith("#") or row[0] == "agency_cd":
            continue
        
        # Extract the datetime and depth
        datetime_str = row[2] if len(row) > 2 else ""  # Ensure the row has enough columns
        depth = row[4] if len(row) > 4 else ""        # Ensure the row has enough columns
        
        # Validate the datetime field
        if " " in datetime_str:  # Check if datetime contains a space
            try:
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")  # Convert to datetime object
                dates.append(datetime_obj)  # Append datetime object for better formatting
            except ValueError:
                print(f"Skipping malformed datetime: {datetime_str}")
        else:
            print(f"Skipping malformed datetime: {datetime_str}")
        
        # Validate and append depth
        if depth:
            try:
                depths.append(float(depth))  # Convert depth to a float
            except ValueError:
                print(f"Skipping malformed depth: {depth}")

# Set resolution to reduce the number of samples
resolution = 50  # Change this value to control the number of samples
dates_reduced = dates[::resolution]  # Take every 'resolution'-th date
depths_reduced = depths[::resolution]  # Take every 'resolution'-th depth

# Plot the data using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(dates_reduced, depths_reduced, marker='o', linestyle='-', color='b', label='Depth to Water Level')

# Format the graph
plt.title("Depth to Water Level Over Time (Reduced Resolution)", fontsize=16)
plt.xlabel("Datetime", fontsize=14)
plt.ylabel("Depth (ft)", fontsize=14)

# Format x-axis to show month and year, and make labels vertical
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Display months and years (e.g., Jan 2009)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to months
plt.xticks(rotation=90, fontsize=4)  # Rotate labels vertically

plt.legend(fontsize=12)
plt.grid(True)

# Show the graph
plt.tight_layout()  # Adjust layout to prevent label overlap
plt.show()