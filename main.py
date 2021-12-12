""" CSC110 Fall 2021 Final Project: main

This Python module contains contains the code necessary to run the entire program. When run, the module:
    1. Loads the necessary files from the datasets
    2. Performs the relevant computations on the data
    3. Produces visualizations investigating the research question:
        To what extent did COVID-19 cause the wealth gap to increase between developed and undeveloped countries?
"""
import visualizations


def main() -> None:
    """ Creates the visualizations of interest.
    """
    visualizations.map_percentage_change('gdp_', 2016, 2020)
    visualizations.map_percentage_change('unemployment_', 2016, 2020)
    visualizations.map_percent_difference_gdp(2018, 2020)
    visualizations.scatter_percentage_change('gdp_', 2016, 2020)
    visualizations.scatter_percentage_change('unemployment_', 2016, 2020)
    visualizations.visualize_aggregates(2016, 2020)


if __name__ == "__main__":
    main()
