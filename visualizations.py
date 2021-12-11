""" CSC110 Fall 2021 Final Project: visualizations

This Python module contains several function headers and descriptions. Functions located
in this file are meant to:
    1. Help visualize data that is extracted from clean_data.py and processed by computations.py
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import clean_data
import computations


def choropleth_percentage_change_slide(root: str, start: int, end: int):
    """Displays global chloropleth map representing percentage change of 'Root' over the years
    [start, end] with time slider.

    Preconditions:
        - root != ''
        - 0 <= start < end

    >>> choropleth_percentage_change_slide('gdp_', 2016, 2020)
    >>> choropleth_percentage_change_slide('unemployment_', 2016, 2020)
    """
    countries, codes = clean_data.populate_dictionary()
    # Qatar and Vietnam are outliers which prevents proper colour differences from being displayed
    # Qatar and Vietnam has extremely high unemployement rate % change after COVID-19
    if root == 'unemployment_':
        countries.pop('Qatar')
        countries.pop('Vietnam')

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    data_so_far = []
    for country in countries:
        ordered_data = computations.get_percent_change_over_time(root, start, end, countries[country].name)
        for i in range(end - start):
            list.append(data_so_far, (codes[country], 2016 + i + 1, ordered_data[i][1], countries[country].name))

    gapminder = pd.DataFrame(data_so_far, columns=['Country Code', 'Year', 'Percent Change %', 'Country Name'])

    fig = px.choropleth(gapminder, locations='Country Code', color='Percent Change %', hover_name='Country Name',
                        animation_frame='Year', color_continuous_scale=px.colors.sequential.RdBu[
                                                                       ::-1],
                        projection='natural earth')
    fig.update_layout(title=f'{yaxis_title}Percent Change of Countries Through Years ({start + 1}-{end})')
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.show()


def choropleth_percent_difference_wholegdp(start: int, end: int):
    """ Display the difference in global GDP all countries contribute to in year 'start' and year
    'end' through a chropleth map

    Preconditions:
        - 0 <= start < end

    >>> choropleth_percent_difference_wholegdp(2016, 2020)
    """
    root = 'gdp_'
    countries, codes = clean_data.populate_dictionary()
    year_start = root + str(start)
    year_end = root + str(end)
    data_start = computations.get_percent_of_whole_all_countries(year_start)
    data_end = computations.get_percent_of_whole_all_countries(year_end)

    data_so_far = []

    # iterate through all countries and compute the % change
    for country in countries:
        if country in data_start and country in data_end:
            data = data_end[country] - data_start[country]
            data_so_far.append((codes[country], data, country))

    # create the dataframe
    df = pd.DataFrame(data_so_far, columns=['Country Code', 'Percent Difference %', 'Country Name'])

    # create and configure the figure
    fig = go.Figure()

    fig.update_layout(title=f'GDP as a % Global GDP Difference between {start} and {end}')

    fig.add_trace(go.Choropleth(
        locations=df['Country Code'],
        z=df['Percent Difference %'],
        text=df['Country Name'],
        colorscale='RdBu',
        autocolorscale=False,
        reversescale=True,
        colorbar={"title": 'Percentage Difference %'})
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    # display the figure
    fig.show()


def plot_percentage_change_cluster_slider(root: str, start: int, end: int) -> None:
    """ Plots percentage change of the desired attribute from years [start, end] on a scatter plot
    where points are in the form (GDP, attribute % change)

    Preconditions:
        - root != ''
        - 0 <= start < end

    >>> plot_percentage_change_cluster_slider('gdp_', 2016, 2020)
    """
    country_dict = clean_data.clean_data()
    # Qatar and Vietnam are outliers which affects the scaling of y-axes
    # Qatar and Vietnam has extremely high unemployement rate % change after COVID-19
    if root == 'unemployment_':
        country_dict.pop('Qatar')
        country_dict.pop('Vietnam')
    data = []
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    quartile_to_str = {1: 'Low GDP', 2: 'Lower Middle GDP', 3: 'Higher Middle GDP', 4: 'High GDP'}

    # iterate over all countries
    for country in country_dict:
        country_data = computations.get_percent_change_over_time(root, start, end, country)
        for i in range(len(country_data)):
            quartile = getattr(country_dict[country], f'gdp_quartile_{start + i}')
            gdp = getattr(country_dict[country], f'gdp_{start + i}')
            # verify that the country has a GDP quartile (thus verifying GDP data exists)
            if quartile in {1, 2, 3, 4}:
                quartile = quartile_to_str[quartile]
                data.append((country_data[i][0], country_data[i][1], country, quartile, gdp))
                min_x = min(min_x, gdp)
                max_x = max(max_x, gdp)
                min_y = min(min_y, country_data[i][1])
                max_y = max(max_y, country_data[i][1])

    attribute = ' '.join([word.capitalize() for word in root.split('_')])
    if attribute == 'Gdp ':
        attribute = attribute.upper()
    attribute += '% Change'

    # create the dafaframe
    gapminder = pd.DataFrame(data, columns=['Year', attribute, 'Country', 'Quartile', 'GDP'])

    # create and configure the figure
    fig = px.scatter(gapminder, color='Quartile', hover_name='Country', animation_frame='Year',
                     x='GDP', y=attribute, color_discrete_sequence=px.colors.qualitative.G10)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(title=f'{attribute} from {start + 1} to {end}')

    # make sure that all points over the years can be captured in the xy-plane
    x_delta = (max_x - min_x) * 0.1
    y_delta = (max_y - min_y) * 0.1
    fig.update_xaxes(range=[min_x - x_delta, max_x + x_delta])
    fig.update_yaxes(range=[min_y - y_delta, max_y + y_delta])

    # display the figure
    fig.show()


def visualize_aggregates(start: int, end: int) -> None:
    """Visualize aggergate sector gdp as a % of aggeregate gdp grouped by gdp quartile.

    Preconditions:
        - 0 <= start < end

    >>> visualize_aggregates(2016, 2020)
    """
    sectors = ['Manufacturing', 'Service', 'Industry', 'Agriculture']
    quartiles = ['Low GDP', 'Lower Middle GDP', 'Upper Middle GDP', 'High GDP']
    aq_m, aq_s, aq_i, aq_a = {}, {}, {}, {}

    # Execute computations
    for year in range(start, end + 1):
        for quartile in range(1, 5):
            aq_m[(year, quartile)] = computations.get_aggregate_quartile('gdp_manufacturing_',
                                                                         quartile, year)
            aq_s[(year, quartile)] = computations.get_aggregate_quartile('gdp_service_',
                                                                         quartile, year)
            aq_i[(year, quartile)] = computations.get_aggregate_quartile('gdp_industry_',
                                                                         quartile, year)
            aq_a[(year, quartile)] = \
                computations.get_aggregate_quartile('gdp_agriculture_forestry_fishing_',
                                                    quartile, year)

    # create the figure
    fig = go.Figure()
    # Add traces(bars) to the figure
    for year in range(start, end + 1):
        for quartile in range(1, 5):
            gdp = sum([aq_m[(year, quartile)], aq_s[(year, quartile)], aq_i[(year, quartile)],
                       aq_a[(year, quartile)]])
            aq_percentages = [aq_m[(year, quartile)] / gdp * 100,
                              aq_s[(year, quartile)] / gdp * 100,
                              aq_i[(year, quartile)] / gdp * 100,
                              aq_a[(year, quartile)] / gdp * 100]
            fig.add_trace(go.Bar(x=sectors, y=aq_percentages,
                                 name=str(year) + ' ' + quartiles[quartile - 1] + ' GDP',
                                 visible=(year == start)))

    # Slider for changing the year
    steps = []
    for i in range(end - start + 1):
        steps.append(dict(
            label=str(start + i),
            method='update',
            args=[{'visible': [i * 4 <= x < i * 4 + 4
                               for x in range(len(fig.data))]},
                  {'title': f'Aggregate Sector GDP as a % of Aggregate GDP for {start}-{end} '
                            f'by Quartile',
                   'showlegend': True}]))

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Year: "},
        pad={"t": 50},
        steps=steps
    )]

    # configure the figure
    fig.update_layout(
        sliders=sliders,
        xaxis_title='Sector',
        yaxis_title='% of Aggregate GDP',
        title=f'Aggregate Sector GDP as a % of Aggregate GDP for {start}-{end} '
              f'by GDP Quartile'
    )

    # display the figure
    fig.show()
