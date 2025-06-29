import csv
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from io import StringIO
import numpy as np

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
        """Plot the reduced data with a trendline, display its equation, and set the graph as Figure 1."""
        # Filter data by year
        filtered_dates, filtered_depths = self.filter_data_by_year()

        # Reduce resolution
        dates_reduced, depths_reduced = self.reduce_resolution(filtered_dates, filtered_depths)

        # Convert datetime objects to numerical values for trendline calculation
        dates_numeric = mdates.date2num(dates_reduced)

        # Calculate the trendline using numpy's polyfit (linear regression)
        trendline_coeffs = np.polyfit(dates_numeric, depths_reduced, 1)  # Degree 1 for linear trendline
        trendline = np.poly1d(trendline_coeffs)

        # Extract the slope and intercept for the equation
        slope = trendline_coeffs[0]
        intercept = trendline_coeffs[1]

        # Create the trendline equation string
        equation = f"y = {slope:.5f}x + {intercept:.2f}"

        # Set the graph as Figure 1
        plt.figure(1, figsize=(10, 6))  # Explicitly set the figure number to 1

        # Plot the data using matplotlib
        plt.plot(dates_reduced, depths_reduced, marker='o', linestyle='-', color='b', label='Depth to Water Level')

        # Plot the trendline
        plt.plot(dates_reduced, trendline(dates_numeric), color='r', linestyle='--', label='Trendline')

        # Annotate the trendline equation on the graph
        plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, fontsize=12, color='red', verticalalignment='top')

        # Format the graph
        plt.title(f"Depth to Water Level Over Time ({self.year})", fontsize=16)
        plt.xlabel("Datetime", fontsize=14)
        plt.ylabel("Depth (ft)", fontsize=14)

        # Format x-axis to show each month and make labels vertical
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
        """Plot the reduced data with a trendline and display its equation."""
        # Reduce resolution
        dates_reduced, depths_reduced = self.reduce_resolution()

        # Convert datetime objects to numerical values for trendline calculation
        dates_numeric = mdates.date2num(dates_reduced)

        # Calculate the trendline using numpy's polyfit (linear regression)
        trendline_coeffs = np.polyfit(dates_numeric, depths_reduced, 1)  # Degree 1 for linear trendline
        trendline = np.poly1d(trendline_coeffs)

        # Extract the slope and intercept for the equation
        slope = trendline_coeffs[0]
        intercept = trendline_coeffs[1]

        # Create the trendline equation string
        equation = f"y = {slope:.5f}x + {intercept:.2f}"

        # Plot the data using matplotlib
        plt.figure(2, figsize=(10, 6))  # Explicitly set the figure number to 1
        plt.plot(dates_reduced, depths_reduced, marker='o', linestyle='-', color='b', label='Depth to Water Level')

        # Plot the trendline
        plt.plot(dates_reduced, trendline(dates_numeric), color='r', linestyle='--', label='Trendline')

        # Annotate the trendline equation on the graph
        plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, fontsize=12, color='red', verticalalignment='top')

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

class WaterDataPlotterYearCompare:
    def __init__(self, url, year1, year2=None, resolution=10):
        """
        Initialize the WaterDataPlotter class.

        :param url: URL to fetch the CSV data.
        :param year1: First year to filter the data.
        :param year2: Second year to filter the data (optional).
        :param resolution: Number of samples to skip for reduced resolution.
        """
        self.url = url
        self.year1 = year1
        self.year2 = year2
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

    def filter_data_by_year(self, year):
        """Filter data by the specified year."""
        filtered_dates = [date for date in self.dates if date.year == year]
        filtered_depths = [self.depths[i] for i, date in enumerate(self.dates) if date.year == year]
        return filtered_dates, filtered_depths

    def reduce_resolution(self, dates, depths):
        """Reduce the resolution of the data."""
        dates_reduced = dates[::self.resolution]  # Take every 'resolution'-th date
        depths_reduced = depths[::self.resolution]  # Take every 'resolution'-th depth
        return dates_reduced, depths_reduced

    def plot_data(self):
        """
        Plot the reduced data for one or two years on the same figure but in different subplots.
        Display datetime labels only for the bottom graph if there are two graphs.
        """
        # Create a figure with subplots
        fig, axes = plt.subplots(2 if self.year2 else 1, 1, figsize=(10, 12))  # Two subplots if year2 is provided

        # Filter and plot data for the first year
        filtered_dates1, filtered_depths1 = self.filter_data_by_year(self.year1)
        dates_reduced1, depths_reduced1 = self.reduce_resolution(filtered_dates1, filtered_depths1)
        dates_numeric1 = mdates.date2num(dates_reduced1)

        # Calculate the trendline for the first year
        trendline_coeffs1 = np.polyfit(dates_numeric1, depths_reduced1, 1)
        trendline1 = np.poly1d(trendline_coeffs1)
        slope1 = trendline_coeffs1[0]
        intercept1 = trendline_coeffs1[1]
        equation1 = f"y = {slope1:.5f}x + {intercept1:.2f}"

        # Plot the first year's data
        axes[0].plot(dates_reduced1, depths_reduced1, marker='o', linestyle='-', color='b', label=f'{self.year1} Depth to Water Level')
        axes[0].plot(dates_reduced1, trendline1(dates_numeric1), color='r', linestyle='--', label=f'{self.year1} Trendline')
        axes[0].text(0.05, 0.95, equation1, transform=axes[0].transAxes, fontsize=12, color='red', verticalalignment='top')
        axes[0].set_title(f"Depth to Water Level Over Time ({self.year1})", fontsize=16)
        axes[0].set_ylabel("Depth (ft)", fontsize=14)
        axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        axes[0].xaxis.set_major_locator(mdates.MonthLocator())
        axes[0].tick_params(axis='x', rotation=90, labelsize=10)
        axes[0].legend(fontsize=12)
        axes[0].grid(True)

        # Hide x-axis labels for the top graph if there is a second graph
        if self.year2:
            axes[0].set_xticklabels([])

            # Filter and plot data for the second year
            filtered_dates2, filtered_depths2 = self.filter_data_by_year(self.year2)
            dates_reduced2, depths_reduced2 = self.reduce_resolution(filtered_dates2, filtered_depths2)
            dates_numeric2 = mdates.date2num(dates_reduced2)

            # Calculate the trendline for the second year
            trendline_coeffs2 = np.polyfit(dates_numeric2, depths_reduced2, 1)
            trendline2 = np.poly1d(trendline_coeffs2)
            slope2 = trendline_coeffs2[0]
            intercept2 = trendline_coeffs2[1]
            equation2 = f"y = {slope2:.5f}x + {intercept2:.2f}"

            # Plot the second year's data
            axes[1].plot(dates_reduced2, depths_reduced2, marker='o', linestyle='-', color='g', label=f'{self.year2} Depth to Water Level')
            axes[1].plot(dates_reduced2, trendline2(dates_numeric2), color='orange', linestyle='--', label=f'{self.year2} Trendline')
            axes[1].text(0.05, 0.95, equation2, transform=axes[1].transAxes, fontsize=12, color='orange', verticalalignment='top')
            axes[1].set_title(f"Depth to Water Level Over Time ({self.year2})", fontsize=16)
            axes[1].set_xlabel("Datetime", fontsize=14)
            axes[1].set_ylabel("Depth (ft)", fontsize=14)
            axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            axes[1].xaxis.set_major_locator(mdates.MonthLocator())
            axes[1].tick_params(axis='x', rotation=90, labelsize=10)
            axes[1].legend(fontsize=12)
            axes[1].grid(True)

        # Adjust layout and show the figure
        plt.tight_layout()
        plt.show()
