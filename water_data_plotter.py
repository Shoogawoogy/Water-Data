import csv
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from io import StringIO
# url = "https://nwis.waterservices.usgs.gov/nwis/iv/?sites=392902084255900&agencyCd=USGS&startDT=2009-01-03T00:00:00.000-05:00&endDT=2025-06-25T23:59:59.999-04:00&parameterCd=72019&format=rdb"

class WaterDataPlotterYEAR:
    def __init__(self, url, year, resolution=10):
        """
        Initialize the WaterDataPlotter class.

        :param url: URL to fetch the CSV data.
        :param year: Year to filter the data.
        :param resolution: Number of samples to skip for reduced resolution.
        """
        self.url = url
        self.year = year
        self.resolution = resolution
        self.dates = []
        self.depths = []

    def load_data(self):
        """Load data from the URL."""
        # Fetch the data from the URL
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from URL: {self.url} (Status code: {response.status_code})")
        
        # Read the data as if it were a file
        data = StringIO(response.text)
        reader = csv.reader(data, delimiter="\t")  # Use tab as the delimiter
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
        """Plot the filtered and reduced data with peak annotations."""
        # Filter data by year
        filtered_dates, filtered_depths = self.filter_data_by_year()

        # Reduce resolution
        dates_reduced, depths_reduced = self.reduce_resolution(filtered_dates, filtered_depths)

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(dates_reduced, depths_reduced, marker='o', linestyle='-', color='b', label=f'Depth to Water Level ({self.year})')

        # Annotate peaks (maximum values)
        for i in range(1, len(depths_reduced) - 1):
            # Check if the current point is a peak
            if depths_reduced[i] > depths_reduced[i - 1] and depths_reduced[i] > depths_reduced[i + 1]:
                plt.annotate(f'{depths_reduced[i]:.2f}',  # Annotate with the depth value
                             (dates_reduced[i], depths_reduced[i]),  # Position of the annotation
                             textcoords="offset points",  # Offset the text
                             xytext=(0, 10),  # Offset by 10 points above the peak
                             ha='center', fontsize=8, color='red')  # Center alignment and red color

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

class WaterDataPlotterALL:
    def __init__(self, url, resolution=10):
        """
        Initialize the WaterDataPlotter class.

        :param url: URL to fetch the CSV data.
        :param resolution: Number of samples to skip for reduced resolution.
        """
        self.url = url
        self.resolution = resolution
        self.dates = []
        self.depths = []

    def load_data(self):
        """Load data from the URL."""
        # Fetch the data from the URL
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from URL: {self.url} (Status code: {response.status_code})")
        
        # Read the data as if it were a file
        data = StringIO(response.text)
        reader = csv.reader(data, delimiter="\t")  # Use tab as the delimiter
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

    def reduce_resolution(self):
        """Reduce the resolution of the data."""
        dates_reduced = self.dates[::self.resolution]  # Take every 'resolution'-th date
        depths_reduced = self.depths[::self.resolution]  # Take every 'resolution'-th depth
        return dates_reduced, depths_reduced

    def plot_data(self):
        """Plot the reduced data."""
        # Reduce resolution
        dates_reduced, depths_reduced = self.reduce_resolution()

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(dates_reduced, depths_reduced, marker='o', linestyle='-', color='b', label='Depth to Water Level')

        # Format the graph
        plt.title("Depth to Water Level Over Time (All Years)", fontsize=16)
        plt.xlabel("Datetime", fontsize=14)
        plt.ylabel("Depth (ft)", fontsize=14)

        # Format x-axis to show month and year, and make labels vertical
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Display months and years (e.g., Jan 2009)
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Set major ticks to years
        plt.xticks(rotation=90, fontsize=10)  # Rotate labels vertically

        plt.legend(fontsize=12)
        plt.grid(True)

        # Show the graph
        plt.tight_layout()  # Adjust layout to prevent label overlap
        plt.show()


# Example Usage:
if __name__ == "__main__":
    # Initialize the class with the URL and resolution
    url = "https://nwis.waterservices.usgs.gov/nwis/iv/?sites=392902084255900&agencyCd=USGS&startDT=2009-01-03T00:00:00.000-05:00&endDT=2025-06-25T23:59:59.999-04:00&parameterCd=72019&format=rdb"
    resolution = 50

    # Create an instance of the WaterDataPlotter class
    plotter = WaterDataPlotter(url, resolution)

    # Load the data and plot
    plotter.load_data()
    plotter.plot_data()