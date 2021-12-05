""" Contains functions to perform various computations
"""

from clean_data import Country


def percentage_change(new: float, old: float) -> float:
    """ Returns the percentage change between old and new

    TODO: add doctest
    """
    return (new - old) / old * 100


def percentage_of_whole(portion, whole: float) -> float:
    """ Returns the percentage the portion makes up of whole

    TODO: add doctest

    """
    return portion / whole * 100


# TODO: Add computations for predictor

def percent_change_list(country_data: Country, metric: str) -> list[tuple[float, float]]:
    """ Return list of tuples representing annual percent change of 'metric' from 2016-2020.
    The tuple keys represent the year and correponds to the specific percentage change of 'metric'
    of the year.

    TODO: add doctest

    """
    percent_change_so_far = []
    if metric == 'gdp':
        data = [country_data.gdp_2016, country_data.gdp_2017,
                country_data.gdp_2018, country_data.gdp_2019,
                country_data.gdp_2020]
    elif metric == 'unemployment':
        data = [country_data.unemployment_2016, country_data.unemployment_2017,
                country_data.unemployment_2018, country_data.unemployment_2019,
                country_data.unemployment_2020]
    else:
        return []
    if all(len(str(x)) == 0 for x in data):
        return []
    year_so_far = 2016
    for i in range(len(data) - 1):
        value = percentage_change(data[i + 1], data[i])
        list.append(percent_change_so_far, (year_so_far, value))
        year_so_far += 1
    return percent_change_so_far


def get_xy_data(ordered_data: list[tuple[float, float]]) -> tuple[list[int], list[float]]:
    """Return a tuple of two parallel lists. The first list contains the keys of outputs as
        ints representing the year. The second list contains the corresponding value of
        the attribute of the specific metric for data (gdp or unemployment % change)

    TODO: add doctest
    """
    # ACCUMULATOR year_so_far: strings from outputs
    year_so_far = []
    # ACCUMULATOR outputs_so_far: floats from outputs
    data_so_far = []
    for put in ordered_data:
        list.append(year_so_far, put[0])
        list.append(data_so_far, put[1])
    return year_so_far, data_so_far
