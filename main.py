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
    visualizations.choropleth_percentage_change_slide('gdp_', 2016, 2020)
    # visualizations.choropleth_percentage_change_slide('unemployment_', 2016, 2020)
    # visualizations.choropleth_percent_difference_wholegdp(2018, 2020)
    # visualizations.plot_percentage_change_cluster_slider('gdp_', 2016, 2020)
    # visualizations.plot_percentage_change_cluster_slider('unemployment_', 2016, 2020)
    # visualizations.visualize_aggregates(2016, 2020)


if __name__ == "__main__":
    main()
