""" Contains functions to perform various visualizations
"""

import plotly.graph_objects as go
import computations as compute


def plot_percentage_change(name: str, root: str, start: int, end: int) -> None:
    """Plot trend.

    Preconditions:

        - outputs != {}


    Sample Usage:
    >>> plot_percentage_change('Australia','unemployment')
    >>> plot_percentage_change('Canada', 'gdp', 2016, 2020)

    """

    # Convert the outputs into parallel x and y lists
    x_data, y_data = compute.get_xy_data(compute.get_percent_change_over_time(root, start, end, name))


    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name=name))

    # Configure the figure
    fig.update_layout(title=f'Annual {root} Percent Change of {name}',
                      xaxis_title='(Year)',
                      yaxis_title=f'Calculated Percentage Change')

    # Show the figure in the browser
    fig.show()
    # Is the above not working for you? Comment it out, and uncomment the following:
    # fig.write_html('my_figure.html')
    # You will need to manually open the my_figure.html file created above.

