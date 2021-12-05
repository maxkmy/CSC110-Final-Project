""" Contains functions to perform various computations
"""

from clean_data import clean_data
from typing import List

country_dict = clean_data()


def percent_change(new: float, old: float) -> float:
    """ Returns the percentage change between old and new
    """
    return (new - old) / old * 100


def percent_of_whole(portion, whole: float) -> float:
    """ Returns the percentage the portion makes up of whole
    """
    return portion / whole * 100


def get_percent_change(root: str, new_attr_suffix: str, old_attr_suffix, country: str) -> float:
    """ Calculates the percent change between the attributes root + new_attr_suffix and
    root + old_attr_suffix
    """
    country = country_dict[country]
    new_attr = root + '_' + new_attr_suffix
    old_attr = root + '_' + old_attr_suffix
    new = getattr(country, new_attr)
    old = getattr(country, old_attr)
    return percent_change(new, old)


def get_percent_change_over_time(root: str, start: int, end: int, country: str) -> List[tuple[float, float]]:
    """ Calculates the percentage change of the desired attribute (root) between adjacent years
    ranging from start to end inclusive
    """
    percentage_changes = []
    for year in range(start, end):
        cur = str(year)
        nxt = str(year + 1)
        percentage_changes.append((float(nxt), get_percent_change(root, nxt, cur, country)))
    return percentage_changes


def aggregate(attribute: str) -> float:
    """ Calculates the sum of the attribute in country_dict where the attribute is available
    (i.e. the attribute is not an empty string)
    """
    accum = 0
    for country in country_dict:
        to_add = getattr(country_dict[country], attribute)
        if to_add != '':
            accum += to_add
    return accum


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
