import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class WaterDataPlotter:
    def __init__(self, filename, year, resolution=10):
        """
        Initialize the WaterDataPlotter class.

        :param filename: Path to the CSV file.
        :param year: Year to filter the data.
        :param resolution: Number of samples to skip for reduced resolution.
        """
        self.filename = filename
        self.year = year
        self.resolution = resolution
        self.dates = []
        self.depths = []

    def load_data(self):
        """Load data from the CSV file."""
        with open(self.filename, "r") as file:
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
                        self.dates.append(datetime_obj)  # Append datetime object for better formatting
                    except ValueError:
                        print(f"Skipping malformed datetime: {datetime_str}")
                else:
                    print(f"Skipping malformed datetime: {datetime_str}")
                
                # Validate and append depth
                if depth:
                    try:
                        self.depths.append(float(depth))  # Convert depth to a float
                    except ValueError:
                        print(f"Skipping malformed depth: {depth}")

    def filter_data_by_year(self):
        """Filter data by the specified year."""
        filtered_dates = [date for date in self.dates if date.year == self.year]
        filtered_depths = [self.depths[i] for i, date in enumerate(self.dates) if date.year == self.year]
        return filtered_dates, filtered_depths

    def reduce_resolution(self, dates, depths):
        """Reduce the resolution of the data."""
        dates_reduced = dates[::self.resolution]  # Take every 'resolution'-th date
        depths_reduced = depths[::self.resolution]  # Take every 'resolution'-th depth
        return dates_reduced, depths_reduced

    def plot_data(self):
        """Plot the filtered and reduced data."""
        # Filter data by year
        filtered_dates, filtered_depths = self.filter_data_by_year()

        # Reduce resolution
        dates_reduced, depths_reduced = self.reduce_resolution(filtered_dates, filtered_depths)

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(dates_reduced, depths_reduced, marker='o', linestyle='-', color='b', label=f'Depth to Water Level ({self.year})')

        # Format the graph
        plt.title(f"Depth to Water Level Over Time ({self.year})", fontsize=16)
        plt.xlabel("Datetime", fontsize=14)
        plt.ylabel("Depth (ft)", fontsize=14)

        # Format x-axis to show month and year, and make labels vertical
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Display months and years (e.g., Jan 2009)
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to months
        plt.xticks(rotation=90, fontsize=10)  # Rotate labels vertically

        plt.legend(fontsize=12)
        plt.grid(True)

        # Show the graph
        plt.tight_layout()  # Adjust layout to prevent label overlap
        plt.show()


# Example Usage:
if __name__ == "__main__":
    # Initialize the class with the filename, year, and resolution
    filename = "C:\\Users\\223106182\\Downloads\\waterData.csv"
    year = 2009
    resolution = 50

    # Create an instance of the WaterDataPlotter class
    plotter = WaterDataPlotter(filename, year, resolution)

    # Load the data, filter, and plot
    plotter.load_data()
    plotter.plot_data()