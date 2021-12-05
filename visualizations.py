""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import clean_data as data
import computations as compute


def plot_percentage_change(name: str, metric: str) -> None:
    """Plot trend.

    Preconditions:

        - outputs != {}


    Sample Usage:
    >>> plot_percentage_change('Canada','gdp')
    >>> plot_percentage_change('Australia','unemployment')
    """
    # Convert the outputs into parallel x and y lists
    x_data, y_data = compute.get_xy_data(compute.percent_change_list(data.clean_data()[name], metric))


    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=name))

    # Configure the figure
    fig.update_layout(title=f'Annual {metric} Percent Change of {name}',
                      xaxis_title='(Year)',
                      yaxis_title=f'Calculated Percentage Change')

    # Show the figure in the browser
    fig.show()
    # Is the above not working for you? Comment it out, and uncomment the following:
    # fig.write_html('my_figure.html')
    # You will need to manually open the my_figure.html file created above.

