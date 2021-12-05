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
    new_attr = root + new_attr_suffix
    old_attr = root + old_attr_suffix
    new = getattr(country, new_attr)
    old = getattr(country, old_attr)
    return percent_change(new, old)


def get_percent_change_over_time(root: str, start: int, end: int, country: str) -> List[float]:
    """ Calculates the percentage change of the desired attribute (root) between adjacent years
    rangging from start to end inclusive
    """
    percentage_changes = []
    for year in range(start, end):
        cur = str(year)
        nxt = str(year + 1)
        percentage_changes.append(get_percent_change(root, nxt, cur, country))
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
