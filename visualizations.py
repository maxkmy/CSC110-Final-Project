""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import clean_data
import computations


def choropleth_percentage_change_slide(root: str):
    """Displays global chloropleth map representing percentage change of 'Root' over the years
    (2017-2020) with built-in time slider.

    Sample Usage:
    >>> choropleth_percentage_change_slide('gdp_')
    >>> choropleth_percentage_change_slide('unemployment_')

    """
    countries, codes = clean_data.populate_dictionary()
    countries.pop('Qatar')

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    data_so_far = []
    for country in countries:
        ordered_data = computations.get_percent_change_over_time(root, 2016, 2020, countries[country].name)
        for i in range(4):
            list.append(data_so_far, (codes[country], 2016 + i + 1, ordered_data[i][1], countries[country].name))

    gapminder = pd.DataFrame(data_so_far, columns=['Country Code', 'Year', 'Data', 'Country Name'])

    fig = px.choropleth(gapminder, locations='Country Code', color='Data', hover_name='Country Name',
                        animation_frame='Year', color_continuous_scale=px.colors.sequential.RdBu,
                        projection='natural earth')
    fig.update_layout(title=f'{yaxis_title} Percent Change of Countries Through Years (2017-2020)')
    fig.show()


def choropleth_percent_wholegdp(start: int, end: int) -> None:
    """ Displays percentage national GDP of a country to global total GDP

    Sample Usage:
    >>> choropleth_percent_wholegdp(2016, 2020)
    """
    countries = clean_data.populate_dictionary()[0]
    codes = clean_data.populate_dictionary()[1]

    data = []
    for year in range(start, end + 1):
        data.append(computations.get_percent_of_whole_all_countries(f'gdp_{year}'))

    data_so_far = []
    for country in countries:
        if all(country in data[i] for i in range(len(data))):
            cur_list = [codes[country]]
            for year in range(start, end + 1):
                cur_list.append(data[year - start][country])
            cur_list.append(country)
            data_so_far.append(tuple(cur_list))

    column_name = ['Country Code']
    for year in range(start, end + 1):
        column_name.append(str(year))
    column_name.append('Country Name')

    df = pd.DataFrame(data_so_far, columns=column_name)
    fig = go.Figure()

    fig.update_layout(title=f'Global GDP Percentage of Countries (Please select a specific year)')

    buttons = []

    for i in range(end - start + 1):
        year = str(start + i)
        fig.add_trace(go.Choropleth(
            locations=df['Country Code'],
            z=df[year],
            text=df['Country Name'],
            colorscale='Agsunset',
            autocolorscale=False,
            reversescale=True,
            zmin=0,
            zmax=3,
            colorbar={"title": 'Global GDP Percentage'})
        )

        buttons.append(dict(
            label=year,
            method='update',
            args=[{'visible': [x == i for x in range(end - start + 1)]},
                  {'title': f'Global GDP Percentage of Countries in  {year}',
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


def choropleth_percent_wholegdp_slider(start: int, end: int) -> None:
    """ Displays percentage national GDP of a country to global total GDP with built-in time slider
    where the years range from start to end inclusive
    Sample Usage:
    >>> choropleth_percent_wholegdp_slider(2016, 2020)
    """
    countries, codes = clean_data.populate_dictionary()

    data = []
    for year in range(start, end + 1):
        data.append(computations.get_percent_of_whole_all_countries(f'gdp_{year}'))

    data_so_far = []
    for country in countries:
        if all(country in data[i] for i in range(len(data))):
            for year in range(start, end + 1):
                data_so_far.append((codes[country], year, data[year - start][country], country))

    gapminder = pd.DataFrame(data_so_far, columns=['Country Code', 'Year', 'Data', 'Country Name'])

    fig = px.choropleth(gapminder, locations='Country Code', color='Data', hover_name='Country Name',
                        animation_frame='Year', range_color=[0, 3], color_continuous_scale=px.colors.sequential.Agsunset,
                        projection='natural earth')
    fig.update_layout(title=f'Global GDP Percentage of Countries Throughout Years ({start}-{end})')
    fig.show()


def choropleth_percent_difference_wholegdp(start: str, end: str):
    """ Displays percentage national GDP of a country to global total GDP

    Sample Usage:
    >>> choropleth_percent_difference_wholegdp('2016', '2020')
    """
    root = 'gdp_'
    countries = clean_data.populate_dictionary()[0]
    codes = clean_data.populate_dictionary()[1]
    yearstart = root + str(start)
    yearend = root + str(end)
    datastart = computations.get_percent_of_whole_all_countries(yearstart)
    dataend = computations.get_percent_of_whole_all_countries(yearend)

    data_so_far = []

    for country in countries:
        key = country
        if key in datastart and key in dataend:
            data = dataend[key] - datastart[key]
            list.append(data_so_far, (codes[country], data, countries[country].name))

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    df = pd.DataFrame(data_so_far, columns=['Country Code', 'Change', 'Country Name'])
    fig = go.Figure()

    fig.update_layout(title=f'{yaxis_title} Global GDP Percentage Difference of Countries Between {start} and {end}')

    fig.add_trace(go.Choropleth(
        locations=df['Country Code'],
        z=df['Change'],
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

    fig.show()


def plot_percentage_change_cluster_slider(root: str, start: int, end: int) -> None:
    """ Plots percentage of the desired attribute from years 2016 to 2020 (inclusive).
    """
    country_dict = clean_data.clean_data()
    country_dict.pop('Myanmar')
    country_dict.pop('Qatar')
    data = []
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    quartile_to_str = {1: 'Low GDP', 2: 'Lower Middle GDP', 3: 'Higher Middle GDP', 4: 'High GDP'}
    for country in country_dict:
        country_data = computations.get_percent_change_over_time(root, start, end, country)
        for i in range(len(country_data)):
            quartile = getattr(country_dict[country], f'gdp_quartile_{start + i}')
            gdp = getattr(country_dict[country], f'gdp_{start + i}')
            if quartile in {1, 2, 3, 4}:
                quartile = quartile_to_str[quartile]
                data.append((country_data[i][0], country_data[i][1], country, quartile, gdp))
                min_x = min(min_x, gdp)
                max_x = max(max_x, gdp)
                min_y = min(min_y, country_data[i][1])
                max_y = max(max_y, country_data[i][1])

    attribute = ' '.join([word.capitalize() for word in root.split('_')]) + '% Change'
    gapminder = pd.DataFrame(data, columns=['Year', attribute, 'Country', 'Quartile', 'GDP'])
    fig = px.scatter(gapminder, color='Quartile', hover_name='Country', animation_frame='Year',
                     x='GDP', y=attribute, color_discrete_sequence=px.colors.qualitative.G10)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(title=f'{attribute} from {start} to {end}')
    x_delta = (max_x - min_x) * 0.1
    y_delta = (max_y - min_y) * 0.1
    fig.update_xaxes(range=[min_x - x_delta, max_x + x_delta])
    fig.update_yaxes(range=[min_y - y_delta, max_y + y_delta])
    fig.show()


def plot_attribute_cluster_slider(root: str, start: int, end: int) -> None:
    """ Plots percentage of the desired attribute from years 2016 to 2020 (inclusive).
    """
    country_dict = clean_data.clean_data()
    # country_dict.pop('Myanmar')
    # country_dict.pop('Qatar')
    data = []
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    quartile_to_str = {1: 'Low GDP', 2: 'Lower Middle GDP', 3: 'Higher Middle GDP', 4: 'High GDP'}
    for country in country_dict:
        for year in range(start, end + 1):
            quartile = getattr(country_dict[country], f'gdp_quartile_{year}')
            gdp = getattr(country_dict[country], f'gdp_{year}')
            attribute = getattr(country_dict[country], root + str(year))
            if quartile in {1, 2, 3, 4} and type(attribute) == float:
                quartile = quartile_to_str[quartile]
                data.append((year, attribute, country, quartile, gdp))
                min_x = min(min_x, gdp)
                max_x = max(max_x, gdp)
                min_y = min(min_y, attribute)
                max_y = max(max_y, attribute)

    attribute = ' '.join([word.capitalize() for word in root.split('_')])
    gapminder = pd.DataFrame(data, columns=['Year', attribute, 'Country', 'Quartile', 'GDP'])
    fig = px.scatter(gapminder, color='Quartile', hover_name='Country', animation_frame='Year',
                     x='GDP', y=attribute, color_discrete_sequence=px.colors.qualitative.G10)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(title=f'{attribute} from {start} to {end}')
    x_delta = (max_x - min_x) * 0.1
    y_delta = (max_y - min_y) * 0.1
    fig.update_xaxes(range=[min_x - x_delta, max_x + x_delta])
    fig.update_yaxes(range=[min_y - y_delta, max_y + y_delta])
    fig.show()


def visualize_aggregates(year: int) -> None:
    """Visualize aggregates.

    >>> visualize_aggregates(2016)
    """
    sectors = ['Manufacturing', 'Service', 'Industry', 'Agriculture']

    fig = go.Figure()
    # Execute computations
    aq_m = {quartile: computations.get_aggregate_quartile('gdp_manufacturing_', quartile, year)
            for quartile in range(1, 5)}
    aq_s = {quartile: computations.get_aggregate_quartile('gdp_service_', quartile, year)
            for quartile in range(1, 5)}
    aq_i = {quartile: computations.get_aggregate_quartile('gdp_industry_', quartile, year)
            for quartile in range(1, 5)}
    aq_a = {quartile: computations.get_aggregate_quartile('gdp_agriculture_forestry_fishing_',
                                                          quartile, year)
            for quartile in range(1, 5)}

    # Create Visualizations
    for quartile in range(1, 5):
        aq_percentages = [aq_m[quartile] / sum([aq_m[quartile], aq_s[quartile],
                                                aq_i[quartile], aq_a[quartile]]),
                          aq_s[quartile] / sum([aq_m[quartile], aq_s[quartile],
                                                aq_i[quartile], aq_a[quartile]]),
                          aq_i[quartile] / sum([aq_m[quartile], aq_s[quartile],
                                                aq_i[quartile], aq_a[quartile]]),
                          aq_a[quartile] / sum([aq_m[quartile], aq_s[quartile],
                                                aq_i[quartile], aq_a[quartile]])]
        fig.add_trace(go.Bar(x=sectors, y=aq_percentages, name=quartile))

    # Add dropdown buttons
    buttons = [dict(
        label='All',
        method='update',
        args=[{'visible': [True for _ in range(1, 5)]},
              {'title': f'Aggregate Sector GDP as a % of Aggregate GDP for {year} by Quartile',
               'showlegend': True}])]

    for i in range(1, 5):
        buttons.append(dict(
            label='Quartile' + str(i),
            method='update',
            args=[{'visible': [x == i for x in range(1, 5)]},
                  {'title': f'Aggregate Sector GDP as a % of Aggregate GDP for {year} by Quartile',
                   'showlegend': True}]))

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=buttons
        )],
        xaxis_title='Sector',
        yaxis_title='% of Aggregate GDP',
        title=f'Aggregate Sector GDP as a % of Aggregate GDP for {year} by Quartile'
    )

    fig.show()
