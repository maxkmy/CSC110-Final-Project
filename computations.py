""" Contains functions to perform various computations
"""

from clean_data import clean_data
import math

country_dict = clean_data()


def get_percent_change(root: str, new_attr_suffix: str, old_attr_suffix, country: str) -> float:
    """ Calculates the percent change between the attributes root + new_attr_suffix and
    root + old_attr_suffix
    """
    # retrieve the country instance
    country = country_dict[country]
    # assign new_attr and old_attr
    new_attr = root + new_attr_suffix
    old_attr = root + old_attr_suffix
    # get the old and new attribute values
    new = getattr(country, new_attr)
    old = getattr(country, old_attr)
    # return percentage change
    return (new - old) / old * 100


def get_percent_change_over_time(root: str, start: int, end: int, country: str) -> \
        list[tuple[int, float]]:
    """ Calculates the percentage change of the desired attribute (root) between consecutive years
    ranging from start to end inclusive
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
    """ Calculates the sum of the attribute in country_dict where the attribute is available
    (i.e. the attribute is not an empty string)
    """
    # initialize accumulator
    accum = 0
    # iterate through every country in country_dict
    for country in country_dict:
        # retrieve attribute from the country's Country instance
        to_add = getattr(country_dict[country], attribute)
        # if the attribute is available, add it to the accumulator
        if to_add != '':
            accum += to_add
    # return the accumulator
    return accum


def get_percent_of_aggregate(aggregate: float, attr: str, country: str) -> float:
    """ Returns the percentage the attribute takes up of the aggregate for a given country.
    If the country does not have the attribute, return float('nan') (Not a number)
    """
    # get the attribute from country's Country instance
    portion = getattr(country_dict[country], attr)
    # if the attribute is available, return the percent it takes up from aggregate
    if portion != '':
        return portion / aggregate * 100
    # if the attribute isn't available, return it as float('nan') (not a number)
    return float('nan')


def get_percent_of_whole_all_countries(attr: str) -> dict[str, float]:
    """ Returns a mapping of the percentage the attribute takes up of the aggregate for all
    countries. If the country does not have the attribute, return float('nan') (Not a number).
    The return type is a dict where a country's name maps to its percentage of whole
    """
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


def get_xy_data(ordered_data: list[tuple[int, float]]) -> tuple[list[int], list[float]]:
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
