""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import clean_data
import computations


def choropleth_percentage_change_slide(root: str, start: int, end: int):
    """Displays global chloropleth map representing percentage change of 'Root' over the years
    (2017-2020) with built-in time slider.

    Sample Usage:
    >>> choropleth_percentage_change_slide('gdp_', 2016, 2020)
    >>> choropleth_percentage_change_slide('unemployment_', 2016, 2020)

    """
    countries, codes = clean_data.populate_dictionary()
    countries.pop('Qatar')

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ' '.join(yaxis_title)

    data_so_far = []
    for country in countries:
        ordered_data = computations.get_percent_change_over_time(root, start, end, countries[country].name)
        for i in range(end - start):
            list.append(data_so_far, (codes[country], 2016 + i + 1, ordered_data[i][1], countries[country].name))

    gapminder = pd.DataFrame(data_so_far, columns=['Country Code', 'Year', 'Data', 'Country Name'])

    fig = px.choropleth(gapminder, locations='Country Code', color='Data', hover_name='Country Name',
                        animation_frame='Year', color_continuous_scale=px.colors.sequential.RdBu,
                        projection='natural earth')
    fig.update_layout(title=f'{yaxis_title} Percent Change of Countries Through Years ({start}-{end})')
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
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
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
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


def visualize_aggregates(start: int, end: int) -> None:
    """Visualize aggregates.

    >>> visualize_aggregates(2016, 2020)
    """
    sectors = ['Manufacturing', 'Service', 'Industry', 'Agriculture']
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

    fig = go.Figure()
    # Add traces(bars) to the figure
    for year in range(start, end + 1):
        for quartile in range(1, 5):
            gdp = sum([aq_m[(year, quartile)], aq_s[(year, quartile)], aq_i[(year, quartile)],
                       aq_a[(year, quartile)]])
            aq_percentages = [aq_m[(year, quartile)] / gdp,
                              aq_s[(year, quartile)] / gdp,
                              aq_i[(year, quartile)] / gdp,
                              aq_a[(year, quartile)] / gdp]
            fig.add_trace(go.Bar(x=sectors, y=aq_percentages,
                                 name=str(year) + ' Quartile ' + str(quartile),
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

    fig.update_layout(
        sliders=sliders,
        xaxis_title='Sector',
        yaxis_title='% of Aggregate GDP',
        title=f'Aggregate Sector GDP as a % of Aggregate GDP for {start}-{end} '
              f'by GDP Quartile'
    )

    fig.show()
