""" CSC110 Fall 2021 Final Project: computations

This Python module contains several function headers and descriptions. Functions located
in this file are meant to:
    1. Compute certain metrics of interest for visualization
"""

import math
from clean_data import clean_data


def get_percent_change(root: str, new_attr_suffix: str, old_attr_suffix: str, country: str) -> \
        float:
    """ Calculates the percent change between the attributes (root + new_attr_suffix) and
    (root + old_attr_suffix).

    Preconditions:
        - root + new_attr_suffix is an attribute of country
        - root + old_attr_suffix is an attribute of country
    """
    # retrieve the country instance
    country_dict = clean_data()
    country = country_dict[country]
    # assign new_attr and old_attr
    new_attr = root + new_attr_suffix
    old_attr = root + old_attr_suffix
    # get the old and new attribute values
    new = getattr(country, new_attr)
    old = getattr(country, old_attr)
    # return percentage change
    if isinstance(old, float) and isinstance(new, float):
        return (new - old) / old * 100
    return float('nan')


def get_percent_change_over_time(root: str, start: int, end: int, country: str) -> \
        list[tuple[int, float]]:
    """ Calculates the percentage change of the desired attribute (root) between consecutive years
    ranging from start to end inclusive.

    Preconditions:
        - 0 <= start < end
    """
    # initialize accumulator
    percentage_changes = []
    # iterate through all pairs of consecutive years
    for year in range(start, end):
        # cur is the cur year and nxt is the the next year after cur
        cur = str(year)
        nxt = str(year + 1)
        # calculate and append the percent change between the attribute root + nxt and root + cur
        percentage_changes.append((year + 1, get_percent_change(root, nxt, cur, country)))
    # return the list of percentage change
    return percentage_changes


def get_aggregate(attribute: str) -> float:
    """ Calculates the aggregate of the attribute in country_dict where the attribute is available
    (i.e. the attribute is not an empty string).

    Preconditions:
        - 'attribute' is an attribute of a Country instance
    """
    country_dict = clean_data()
    # initialize accumulator
    accum = 0
    # iterate through every country in country_dict
    for country in country_dict:
        # retrieve attribute from the country's Country instance
        to_add = getattr(country_dict[country], attribute)
        # if the attribute is available, add it to the accumulator
        if isinstance(to_add, float):
            accum += to_add
    # return the accumulator
    return accum


def get_percent_of_aggregate(aggregate: float, attr: str, country: str) -> float:
    """ Returns the percentage the attribute takes up of the aggregate for a given country.
    If the country does not have the attribute, return float('nan') (Not a number).

    Preconditions:
        - 'attr' is an attribute of a Country instance
        - country in clean_data()
    """
    country_dict = clean_data()
    # get the attribute from country's Country instance
    portion = getattr(country_dict[country], attr)
    # if the attribute is available, return the percent it takes up from aggregate
    if portion != '':
        return portion / aggregate * 100
    # if the attribute isn't available, return it as float('nan') (not a number)
    return float('nan')


def get_percent_of_whole(attr: str) -> dict[str, float]:
    """ Returns a mapping of the percentage the attribute takes up of the aggregate for all
    countries. If the country does not have the attribute, return float('nan') (Not a number).
    The return type is a dict where a country's name maps to its percentage of whole.

    Preconditions:
        - 'attr' is an attribute of a Country instance
    """
    country_dict = clean_data()
    # initialize the accumulator
    country_to_percent_of_aggregate = {}
    # calculate the aggregate for the given attribute
    aggregate = get_aggregate(attr)
    # iterate through all country in country_dict
    for country in country_dict:
        # calculate the percent the country's attribute takes up from aggregate
        percent_of_aggregate = get_percent_of_aggregate(aggregate, attr, country)
        # if percent_of_aggregate is a number (i.e. not NaN), add it to the accumulator
        if not math.isnan(percent_of_aggregate):
            country_to_percent_of_aggregate[country] = percent_of_aggregate
    # return the accumulator
    return country_to_percent_of_aggregate


def get_attribute_by_gdp_quartile(root: str, year: int) -> list[list[tuple[int, int]]]:
    """
    Returns a list of 4 lists. Each of the 4 lists contain lists with 2 elements, in the form
    (gdp, attribute) where the attribute is root + year.

    Preconditions:
        - year >= 0
    """
    country_dict = clean_data()
    cur = [[], [], [], []]
    attr = root + str(year)
    gdp_quartile = 'gdp_quartile_' + str(year)
    for country in country_dict:
        gdp = getattr(country_dict[country], f'gdp_{year}')
        attr_val = getattr(country_dict[country], attr)
        if not isinstance(attr_val, float) or not isinstance(gdp, float):
            continue
        quartile = getattr(country_dict[country], gdp_quartile)
        if quartile == 1:
            cur[0].append((gdp, attr_val))
        elif quartile == 2:
            cur[1].append((gdp, attr_val))
        elif quartile == 3:
            cur[2].append((gdp, attr_val))
        elif quartile == 4:
            cur[3].append((gdp, attr_val))
    return cur


def get_aggregate_quartile(root: str, desired_quartile: int, year: int) -> float:
    """ Calculates the sum of the attribute in country_dict where the country is in the desired
    quartile and the attribute is available (i.e. the attribute is not an empty string).

    Preconditions:
        - year >= 0
        - desired_quartile in {1, 2, 3, 4}
        - root + year is an attribute of a Country instance
    """
    country_dict = clean_data()
    # initialize accumulator
    accum = 0
    attr = root + str(year)
    # iterate through every country in country_dict
    for country in country_dict:
        quartile = getattr(country_dict[country], f'gdp_quartile_{year}')
        if desired_quartile == quartile:
            to_add = getattr(country_dict[country], attr)
            if isinstance(to_add, float):
                accum += to_add
    return accum


def get_xy_data(ordered_data: list[tuple[int, float]]) -> tuple[list[int], list[float]]:
    """Return a tuple of two parallel lists. The first list contains the first element of each
    element in ordered_data and the second list contains the second elemeent of each element
    in ordered_data.

    >>> data = [(2016, 4.5), (2017, 8.8) ,(2018, 12.4) ,(2019, 17.8) ,(2020, 40.2)]
    >>> get_xy_data(data)
    ([2016, 2017, 2018, 2019, 2020], [4.5, 8.8, 12.4, 17.8, 40.2])

    Preconditions:
        - all(len(data) == 2 for data in ordered_data)
    """
    x_data, y_data = [], []
    for x, y in ordered_data:
        x_data.append(x)
        y_data.append(y)
    return x_data, y_data


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    import doctest

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    doctest.testmod()

    python_ta.check_all(config={
        'allowed-io': [],
        'extra-imports': ['clean_data', 'math', 'doctest'],
        'max-line-length': 100,
        'max-nested-blocks': 4,
        'disable': ['R1705', 'C0200']
    })
