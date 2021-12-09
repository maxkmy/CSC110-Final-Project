""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go

import clean_data
import computations


def plot_percentage_change(root: str, start: int, end: int) -> None:
    """Plot percentage change of desired attribute (root) over the years start to end inclusive.

    Preconditions:
        - 0 < start < end

    Sample Usage:
    >>> plot_percentage_change('gdp_', 2016, 2020)
    >>> plot_percentage_change('unemployment_', 2016, 2020)

    """
    # get cleaned data
    country_dict = clean_data.clean_data()
    countries = [country_dict[country] for country in country_dict]

    # Create the figure
    fig = go.Figure()
    country_list = []
    for country in countries:
        # get ordered pair in the form (year, percentage change) and split into x and y data
        ordered_data = computations.get_percent_change_over_time(root, start, end, country.name)
        x_data, y_data = computations.get_xy_data(ordered_data)
        # add the plot to fig and append country to country_list
        fig.add_trace(go.Scatter(x=x_data, y=y_data, name=country.name))
        country_list.append(country.name)

    # set y-axis title
    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    # Configure the figure
    fig.update_layout(title=f'Annual {yaxis_title} Percent Change of All Countries',
                      xaxis_title='Year',
                      yaxis_title=f'{yaxis_title} Percentage Change')

    # Add dropdown buttons
    buttons = [dict(
        label='All',
        method='update',
        args=[{'visible': [True for _ in range(len(country_list))]},
              {'title': f'Annual {yaxis_title} Percent Change of Countries',
               'showlegend': True}])]

    for i in range(len(country_list)):
        buttons.append(dict(
            label=country_list[i],
            method='update',
            args=[{'visible': [x == i for x in range(len(country_list))]},
                  {'title': f'Annual {yaxis_title} Percent Change of {country_list[i]}',
                   'showlegend': True}]))

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=buttons
        )]
    )

    fig.show()
