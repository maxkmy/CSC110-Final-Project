""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import computations


def plot_percentage_change(country: str, root: str, start: int, end: int) -> None:
    """Plot trend.

    Preconditions:
        - outputs != {}

    Sample Usage:
    >>> plot_percentage_change('Australia', 'unemployment', 2016, 2020)
    >>> plot_percentage_change('Canada', 'gdp', 2016, 2020)

    """
    ordered_data = computations.get_percent_change_over_time(root, start, end, country)
    x_data, y_data = computations.get_xy_data(ordered_data)

    yaxis_title = [word.capitalize() for word in (root.split('_'))]
    yaxis_title = ''.join(yaxis_title)

    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=country))

    # Configure the figure
    fig.update_layout(title=f'Annual {root} Percent Change of {country}',
                      xaxis_title='(Year)',
                      yaxis_title=f'{yaxis_title} Percentage Change')

    # Show the figure in the browser
    fig.show()
    # Is the above not working for you? Comment it out, and uncomment the following:
    # fig.write_html('my_figure.html')
    # You will need to manually open the my_figure.html file created above.

