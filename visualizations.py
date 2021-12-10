""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import pandas as pd
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


def chloropleth_percentage_change(root: str):
    """Displays global chloropleth map representing percentage change of 'Root' over the years (2017-2020)

    Sample Usage:

    >>> chloropleth_percentage_change('gdp_')
    >>> chloropleth_percentage_change('unemployment_')
    """
    countries = clean_data.populate_dictionary()[0]
    codes = clean_data.populate_dictionary()[1]

    data_so_far = []
    for country in countries:

        if countries[country].name != 'Qatar':  # Qatar due to significant outlier
            ordered_data = computations.get_percent_change_over_time(root, 2016, 2020, countries[country].name)
            list.append(data_so_far, (codes[country], ordered_data[0][1], ordered_data[1][1], ordered_data[2][1],
                                      ordered_data[3][1], countries[country].name))

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    df = pd.DataFrame(data_so_far, columns=['Country Code', '2017', '2018', '2019', '2020', 'Country Name'])
    fig = go.Figure()

    fig.update_layout(title=f'{yaxis_title} Percent Change of Countries (Please select a specific year)')

    buttons = []

    for i in range(4):
        year = str(2017 + i)
        fig.add_trace(go.Choropleth(
            locations=df['Country Code'],
            z=df[year],
            text=df['Country Name'],
            colorscale='Blues',
            autocolorscale=False,
            reversescale=True,
            colorbar={"title": 'Percentage Change'})
        )

        buttons.append(dict(
            label=(year),
            method='update',
            args=[{'visible': [x == i for x in range(4)]},
                  {'title': f'{yaxis_title} Percent Change of Countries in  {year}',
                   'showlegend': True}]))

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=buttons
        )],
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    fig.show()


def plot_percentage_change_cluster(root: str, year: int) -> None:
    """ Plot the percentage change of the desired attribute (root) from year - 1 to year on the
    xy-plane as (gdp, desired attribute). Cluster the points based on GDP quartile.

    Preconditions:
        - year > 0
        - root != ''

    Sample Usage:
    >>> plot_percentage_change_cluster('gdp_', 2016)
    >>> plot_percentage_change_cluster('unemployment_', 2020)
    """
    country_dict = clean_data.clean_data()
    x_data = [[], [], [], []]
    y_data = [[], [], [], []]
    for country in country_dict:
        quartile = getattr(country_dict[country], f'gdp_quartile_{year}')
        if quartile not in {1, 2, 3, 4}:
            continue
        gdp = getattr(country_dict[country], f'gdp_{year}')
        percentage_change = computations.get_percent_change(root, str(year), str(year - 1), country)
        x_data[quartile - 1].append(gdp)
        y_data[quartile - 1].append(percentage_change)

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

    title = ' '.join([word.capitalize() for word in root.split('_')])
    title = title + 'Percent Change in Year' + str(year)

    # Configure the figure
    fig.update_layout(title=title,
                      xaxis_title=f'Gdp in year {year}',
                      yaxis_title=title)

    fig.show()


def plot_percentage_change_cluster_overtime(root: str, start: int, end: int) -> None:
    """ Plots percentage of the desired attribute from years start to end (inclusive).
    """
    country_dict = clean_data.clean_data()
    years = list(range(start, end + 1))

    fig_dict = {
        'data': [],
        'layout': {},
        'frames': []
    }

    yaxis_title = ' '.join([word.capitalize() for word in root.split('_')]) + ' Percentage Change'
    fig_dict['layout']['xaxis'] = {'title': 'GDP'}
    fig_dict['layout']['yaxis'] = {'title': f'{yaxis_title}'}
    fig_dict['layout']['hovermode'] = 'closest'
    fig_dict['layout']['updatemenus'] = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                    'fromcurrent': True, 'transition': {'duration': 300,
                                                                        'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                      'mode': 'immediate',
                                      'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]

    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Year:',
            'visible': True,
            'xanchor': 'right',
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }

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

    year = start
    for country in country_dict:
        quartile = getattr(country_dict[country], f'gdp_quartile_{year}')
        gdp = getattr(country_dict[country], f'gdp_{year}')
        percentage_change = computations.get_percent_change(root, str(year), str(year - 1), country)
        if type(gdp) != float or type(percentage_change) != float:
            continue

        data_dict = {
            'x': [gdp],
            'y': [percentage_change],
            'mode': 'markers',
            'text': country,
            'marker': {
                'color': num_to_colour[quartile]
            }
        }

        fig_dict['data'].append(data_dict)

    for year in years:
        frame = {'data': [], 'name': str(year)}
        for country in country_dict:
            quartile = getattr(country_dict[country], f'gdp_quartile_{year}')
            gdp = getattr(country_dict[country], f'gdp_{year}')
            percentage_change = computations.get_percent_change(root, str(year), str(year - 1), country)
            if type(gdp) != float or type(percentage_change) != float:
                continue

            data_dict = {
                'x': [gdp],
                'y': [percentage_change],
                'mode': 'markers',
                'text': country,
                'marker': {
                    'color': num_to_colour[quartile]
                }
            }
            frame['data'].append(data_dict)
        fig_dict['frames'].append(frame)
        slider_step = {'args': [
            [year],
            {'frame': {'duration': 300, 'redraw': False},
             'mode': 'immediate',
             'transition': {'duration': 300}}
        ],
            'label': year,
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)

    fig_dict['layout']['sliders'] = [sliders_dict]

    fig = go.Figure(fig_dict)

    fig.show()

# def plot_cluster(root: str, year: int) -> None:
#     """ Plot the desired attribute (root) on an xy-plane as (gdp, desired attribute). Cluster the
#     points based on income quartile to observe trends
#
#     Preconditions:
#         - year > 0
#         - root != ''
#
#     Sample Usage:
#     >>> plot_cluster('gdp_', 2016)
#     >>> plot_cluster('unemployment_', 2020)
#     """
#     data = computations.get_attribute_by_gdp_quartile(root, year)
#     x_data = []
#     y_data = []
#     for i in range(4):
#         x_data_quartile, y_data_quartile = computations.get_xy_data(data[i])
#         x_data.append(x_data_quartile)
#         y_data.append(y_data_quartile)
#
#     # Create the figure
#     fig = go.Figure()
#
#     # set up colour of cluster for each income quartile
#     num_to_colour = {
#         1: 'DarkOrange',
#         2: 'Crimson',
#         3: 'RebeccaPurple',
#         4: 'DarkGreen'
#     }
#     num_to_quartile = {
#         1: 'Low GDP',
#         2: 'Lower Middle GDP',
#         3: 'Upper Middle GDP',
#         4: 'High GDP'
#     }
#     # adding each cluster
#     for i in range(4):
#         fig.add_trace(
#             go.Scatter(
#                 x=x_data[i],
#                 y=y_data[i],
#                 mode='markers',
#                 marker=dict(color=num_to_colour[i + 1]),
#                 name=num_to_quartile[i + 1]
#             )
#         )
#
#     # define each cluster
#     cluster1 = [dict(
#         type='circle',
#         xref='x', y_ref='y',
#         x0=min(x_data[0]), y0=min(y_data[0]),
#         x1=max(x_data[0]), y1=max(y_data[0]),
#         line=dict(color=num_to_colour[1])
#     )]
#
#     cluster2 = [dict(
#         type='circle',
#         xref='x', y_ref='y',
#         x0=min(x_data[1]), y0=min(y_data[1]),
#         x1=max(x_data[1]), y1=max(y_data[1]),
#         line=dict(color=num_to_colour[2])
#     )]
#
#     cluster3 = [dict(
#         type='circle',
#         xref='x', y_ref='y',
#         x0=min(x_data[2]), y0=min(y_data[2]),
#         x1=max(x_data[2]), y1=max(y_data[2]),
#         line=dict(color=num_to_colour[3])
#     )]
#
#     cluster4 = [dict(
#         type='circle',
#         xref='x', y_ref='y',
#         x0=min(x_data[3]), y0=min(y_data[3]),
#         x1=max(x_data[3]), y1=max(y_data[3]),
#         line=dict(color=num_to_colour[4])
#     )]
#
#     # add buttons that add the cluster circle
#     fig.update_layout(
#         updatemenus=[
#             dict(
#                 type='buttons',
#                 buttons=[
#                     dict(label='All',
#                          method='relayout',
#                          args=['shapes', cluster1 + cluster2 + cluster3 + cluster4]),
#                     dict(label='None',
#                          method='relayout',
#                          args=['shapes', []]),
#                     dict(label='High GDP',
#                          method='relayout',
#                          args=['shapes', cluster4]),
#                     dict(label='Upper Middle GDP',
#                          method='relayout',
#                          args=['shapes', cluster3]),
#                     dict(label='Lower Middle GDP',
#                          method='relayout',
#                          args=['shapes', cluster2]),
#                     dict(label='Low GDP',
#                          method='relayout',
#                          args=['shapes', cluster1])
#                 ]
#             )
#         ]
#     )
#
#     title = ' '.join(root.split('_')) + 'in year ' + str(year)
#
#     # Configure the figure
#     fig.update_layout(title=title,
#                       xaxis_title=f'Gdp in year {year}',
#                       yaxis_title=title)
#
#     fig.show()
