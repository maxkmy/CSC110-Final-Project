""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
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


def choropleth_percentage_change(root: str):
    """Displays global chloropleth map representing percentage change of 'Root' over the years (2017-2020)

    Sample Usage:
    >>> choropleth_percentage_change('gdp_')
    >>> choropleth_percentage_change('unemployment_')
    """
    countries, codes = clean_data.populate_dictionary()

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
            colorscale='RdBu',
            autocolorscale=False,
            reversescale=True,
            colorbar={"title": 'Percentage Change'})
        )

        buttons.append(dict(
            label=year,
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


def choropleth_percent_wholegdp() -> None:
    """ Displays percentage national GDP of a country to global total GDP

    Sample Usage:
    >>> choropleth_percent_wholegdp()
    """
    root = 'gpd_'
    countries = clean_data.populate_dictionary()[0]
    codes = clean_data.populate_dictionary()[1]

    data2016 = computations.get_percent_of_whole_all_countries('gdp_2016')
    data2017 = computations.get_percent_of_whole_all_countries('gdp_2017')
    data2018 = computations.get_percent_of_whole_all_countries('gdp_2018')
    data2019 = computations.get_percent_of_whole_all_countries('gdp_2019')
    data2020 = computations.get_percent_of_whole_all_countries('gdp_2020')

    data_so_far = []

    for country in countries:
        key = country
        if key in data2016 and key in data2017 and key in data2018 and key in data2019 and key in data2020:
            list.append(data_so_far, (codes[country], data2016[key],
                                      data2017[key], data2018[key],
                                      data2019[key], data2020[key],
                                      countries[country].name))

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    df = pd.DataFrame(data_so_far, columns=['Country Code', '2016', '2017', '2018', '2019', '2020', 'Country Name'])
    fig = go.Figure()

    fig.update_layout(title=f'Global  {yaxis_title} Percentage of Countries (Please select a specific year)')

    buttons = []

    for i in range(5):
        year = str(2016 + i)
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
            args=[{'visible': [x == i for x in range(5)]},
                  {'title': f'Global {yaxis_title} Percentage of Countries in  {year}',
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


def choropleth_percent_wholegdp_slide() -> None:
    """ Displays percentage national GDP of a country to global total GDP with built-in time slider

    Sample Usage:
    >>> choropleth_percent_wholegdp_slide()
    """
    countries, codes = clean_data.populate_dictionary()

    data2016 = computations.get_percent_of_whole_all_countries('gdp_2016')
    data2017 = computations.get_percent_of_whole_all_countries('gdp_2017')
    data2018 = computations.get_percent_of_whole_all_countries('gdp_2018')
    data2019 = computations.get_percent_of_whole_all_countries('gdp_2019')
    data2020 = computations.get_percent_of_whole_all_countries('gdp_2020')

    data_so_far = []
    for country in countries:
        key = country
        if key in data2016 and key in data2017 and key in data2018 and key in data2019 and key in data2020:
            data_so_far.append((codes[country], 2016, data2016[key], countries[country].name))
            data_so_far.append((codes[country], 2017, data2017[key], countries[country].name))
            data_so_far.append((codes[country], 2018, data2018[key], countries[country].name))
            data_so_far.append((codes[country], 2019, data2019[key], countries[country].name))
            data_so_far.append((codes[country], 2020, data2020[key], countries[country].name))

    gapminder = pd.DataFrame(data_so_far, columns=['Country Code', 'Year', 'Data', 'Country Name'])

    fig = px.choropleth(gapminder, locations='Country Code', color='Data', hover_name='Country Name',
                        animation_frame='Year', range_color=[0, 3], color_continuous_scale=px.colors.sequential.Agsunset,
                        projection='natural earth')
    fig.update_layout(title=f'Global GDP Percentage of Countries Throughout Years (2016-2020)')
    fig.show()


def choropleth_percent_change_wholegdp(start: str, end: str):
    """ Displays percentage national GDP of a country to global total GDP

    Sample Usage:
    >>> choropleth_percent_change_wholegdp('2016', '2020')
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
            data = computations.get_percent_change('gdp_', start, end, key)
            list.append(data_so_far, (codes[country], data, countries[country].name))

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    df = pd.DataFrame(data_so_far, columns=['Country Code', 'Change', 'Country Name'])
    fig = go.Figure()

    fig.update_layout(title=f'{yaxis_title} Global GDP Percentage Change of Countries Between {start} and {end}')

    fig.add_trace(go.Choropleth(
        locations=df['Country Code'],
        z=df['Change'],
        text=df['Country Name'],
        colorscale='RdBu',
        autocolorscale=False,
        reversescale=True,
        colorbar={"title": 'Percentage Change %'})
    )

    fig.update_layout(
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
    text = [[], [], [], []]
    for country in country_dict:
        quartile = getattr(country_dict[country], f'gdp_quartile_{year}')
        if quartile not in {1, 2, 3, 4}:
            continue
        gdp = getattr(country_dict[country], f'gdp_{year}')
        percentage_change = computations.get_percent_change(root, str(year), str(year - 1), country)
        x_data[quartile - 1].append(gdp)
        y_data[quartile - 1].append(percentage_change)
        text[quartile - 1].append(country)

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
                name=num_to_quartile[i + 1],
                text=text[i]
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
    title = title + '% Change in ' + str(year)

    # Configure the figure
    fig.update_layout(title=title,
                      xaxis_title=f'{year} Gdp',
                      yaxis_title=title)

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
