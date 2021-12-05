""" Contains functions to perform various computations
"""

from clean_data import clean_data
from typing import List
import math

country_dict = clean_data()


def get_percent_change(root: str, new_attr_suffix: str, old_attr_suffix, country: str) -> float:
    """ Calculates the percent change between the attributes root + new_attr_suffix and
    root + old_attr_suffix
    """
    country = country_dict[country]
    new_attr = root + new_attr_suffix
    old_attr = root + old_attr_suffix
    new = getattr(country, new_attr)
    old = getattr(country, old_attr)
    return (new - old) / old * 100


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


def get_aggregate(attribute: str) -> float:
    """ Calculates the sum of the attribute in country_dict where the attribute is available
    (i.e. the attribute is not an empty string)
    """
    accum = 0
    for country in country_dict:
        to_add = getattr(country_dict[country], attribute)
        if to_add != '':
            accum += to_add
    return accum


def get_percent_of_aggregate(aggregate: float, attr: str, country: str) -> float:
    """ Returns the percentage the attribute takes up of the aggregate for a given country.
    If the country does not have the attribute, return float('nan') (Not a number)
    """
    portion = getattr(country_dict[country], attr)
    if portion != '':
        return portion / aggregate * 100
    return float('nan')


def get_percent_of_whole_all_countries(attr: str) -> dict[str, float]:
    """ Returns a mapping of the percentage the attribute takes up of the aggregate for all
    countries. If the country does not have the attribute, return float('nan') (Not a number).
    The return type is a dict where a country's name maps to its percentage of whole
    """
    country_to_percent_of_aggregate = {}
    aggregate = get_aggregate(attr)
    for country in country_dict:
        percent_of_aggregate = get_percent_of_aggregate(aggregate, attr, country)
        if not math.isnan(percent_of_aggregate):
            country_to_percent_of_aggregate[country] = percent_of_aggregate
    return country_to_percent_of_aggregate
