""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go

import pandas as pd

import clean_data
import computations


def plot_percentage_change(root: str, start: int, end: int) -> None:
    """Plot trend.

    Preconditions:
        - outputs != {}

    Sample Usage:
    >>> plot_percentage_change('gdp_', 2016, 2020)
    >>> plot_percentage_change('unemployment_', 2016, 2020)

    """

    countries = [clean_data.clean_data()[x] for x in clean_data.clean_data()]

    # Create the figure
    fig = go.Figure()
    counter = 0
    country_list = []
    for country in countries:
        try:
            ordered_data = computations.get_percent_change_over_time(root, start, end, country.name)
            x_data, y_data = computations.get_xy_data(ordered_data)

            fig.add_trace(go.Scatter(x=x_data, y=y_data, name=country.name))
            list.append(country_list, country.name)
            counter += 1
        except TypeError:
            pass

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ''.join(yaxis_title)

    # Configure the figure
    fig.update_layout(title=f'Annual {yaxis_title} Percent Change of Selected Country',
                      xaxis_title='Year',
                      yaxis_title=f'{yaxis_title} Percentage Change')

    # Add dropdown

    buttons_so_far = [dict(
        label='All',
        method='update',
        args=[{'visible': [True for x in range(len(country_list))]},
              {'title': f'Annual {yaxis_title} Percent Change of Countries',
               'showlegend': True}])]

    for i in range(len(country_list)):
        list.append(buttons_so_far, dict(
            label=country_list[i],
            method='update',
            args=[{'visible': [x == i for x in range(len(country_list))]},
                  {'title': f'Annual {yaxis_title} Percent Change of {country_list[i]}',
                   'showlegend': True}]))

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=buttons_so_far
        )

        ]
    )

    fig.show()


