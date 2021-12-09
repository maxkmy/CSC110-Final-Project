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
    fig.update_layout(title=f'Annual {yaxis_title} Percent Change of Selected Countries',
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


def plot_cluster(root: str, year: int) -> None:
    """ Plot the desired attribute (root) on an xy-plane as (gdp, desired attribute). Cluster the
    points based on income quartile to observe trends

    Preconditions:
        - year > 0
        - root != ''

    Sample Usage:
    >>> plot_cluster('gdp_', 2016)
    >>> plot_cluster('unemployment_', 2020)
    """
    data = computations.get_attribute_by_gdp_quartile(root, year)
    x_data = []
    y_data = []
    for i in range(4):
        x_data_quartile, y_data_quartile = computations.get_xy_data(data[i])
        x_data.append(x_data_quartile)
        y_data.append(y_data_quartile)

    # Create the figure
    fig = go.Figure()

    # set up colour of cluster for each income quartile
    num_to_colour = {
        1: 'DarkOrange',
        2: 'Crimson',
        3: 'RebeccaPurple',
        4: 'DarkGreen'
    }
    num_to_quartile = {
        1: 'Low GDP',
        2: 'Lower Middle GDP',
        3: 'Upper Middle GDP',
        4: 'High GDP'
    }
    # adding each cluster
    for i in range(4):
        fig.add_trace(
            go.Scatter(
                x=x_data[i],
                y=y_data[i],
                mode='markers',
                marker=dict(color=num_to_colour[i + 1]),
                name=num_to_quartile[i + 1]
            )
        )

    # define each cluster
    cluster1 = [dict(
        type='circle',
        xref='x', y_ref='y',
        x0=min(x_data[0]), y0=min(y_data[0]),
        x1=max(x_data[0]), y1=max(y_data[0]),
        line=dict(color=num_to_colour[1])
    )]

    cluster2 = [dict(
        type='circle',
        xref='x', y_ref='y',
        x0=min(x_data[1]), y0=min(y_data[1]),
        x1=max(x_data[1]), y1=max(y_data[1]),
        line=dict(color=num_to_colour[2])
    )]

    cluster3 = [dict(
        type='circle',
        xref='x', y_ref='y',
        x0=min(x_data[2]), y0=min(y_data[2]),
        x1=max(x_data[2]), y1=max(y_data[2]),
        line=dict(color=num_to_colour[3])
    )]

    cluster4 = [dict(
        type='circle',
        xref='x', y_ref='y',
        x0=min(x_data[3]), y0=min(y_data[3]),
        x1=max(x_data[3]), y1=max(y_data[3]),
        line=dict(color=num_to_colour[4])
    )]

    # add buttons that add the cluster circle
    fig.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                buttons=[
                    dict(label='All',
                         method='relayout',
                         args=['shapes', cluster1 + cluster2 + cluster3 + cluster4]),
                    dict(label='None',
                         method='relayout',
                         args=['shapes', []]),
                    dict(label='High GDP',
                         method='relayout',
                         args=['shapes', cluster4]),
                    dict(label='Upper Middle GDP',
                         method='relayout',
                         args=['shapes', cluster3]),
                    dict(label='Lower Middle GDP',
                         method='relayout',
                         args=['shapes', cluster2]),
                    dict(label='Low GDP',
                         method='relayout',
                         args=['shapes', cluster1])
                ]
            )
        ]
    )

    title = ' '.join(root.split('_')) + 'in year ' + str(year)

    # Configure the figure
    fig.update_layout(title=title,
                      xaxis_title=f'Gdp in year {year}',
                      yaxis_title=title)

    fig.show()
