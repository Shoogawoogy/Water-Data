import requests
import os

from water_data_plotter import WaterDataPlotterALL, WaterDataPlotterYEAR, WaterDataPlotterYearCompare

# Initialize the class with the URL, year, and resolution
url = "https://nwis.waterservices.usgs.gov/nwis/iv/?sites=392902084255900&agencyCd=USGS&startDT=2009-01-03T00:00:00.000-05:00&endDT=2025-06-25T23:59:59.999-04:00&parameterCd=72019&format=rdb"
#url = "https://nwis.waterservices.usgs.gov/nwis/iv/?sites=03272100&agencyCd=USGS&startDT=2009-01-03T00:00:00.000-05:00&endDT=2025-06-25T23:59:59.999-04:00&parameterCd=00065&format=rdb"
year = 2023
year2 = 2010
resolution = 50

    # Create an instance of the WaterDataPlotter class

    # Load the data, filter, and plot
#plotterALL = WaterDataPlotterALL(url, resolution)
#plotterALL.load_data()
#plotterALL.plot_data()

plotterYEAR = WaterDataPlotterYEAR(url, year, resolution)
plotterYEAR.load_data()
plotterYEAR.plot_data()

#plotterYearCompare = WaterDataPlotterYearCompare(url, year, year2, resolution)
#plotterYearCompare.load_data()
#plotterYearCompare.plot_data()
