""" CSC110 Fall 2021 Final Project: clean_data

This Python module contains several function headers and descriptions. Functions located
in this file are meant to:
    1. Extract country metrics from external csv files
    2. Process country metrics obtained from csv files to set new metrics
"""

import csv
from typing import Optional


class Country:
    """ A class representing each country with their associated statistics

    Instance Attributes:
        - name: the name of 'self'
        - gdp_2016: national GDP value of 'self' reported in the year 2016
        - gdp_2017: national GDP value of 'self' reported in the year 2017
        - gdp_2018: national GDP value of 'self' reported in the year 2018
        - gdp_2019: national GDP value of 'self' reported in the year 2019
        - gdp_2020: national GDP value of 'self' reported in the year 2020
        - gdp_quartile_2016: the quartile of 'self's 2016 GDP where 4 is the top 25% quartile
        and 1 is the bottom 25% quartile
        - gdp_quartile_2017: the quartile of 'self's 2017 GDP where 4 is the top 25% quartile
        and 1 is the bottom 25% quartile
        - gdp_quartile_2018: the quartile of 'self's 2018 GDP where 4 is the top 25% quartile
        and 1 is the bottom 25% quartile
        - gdp_quartile_2019: the quartile of 'self's 2019 GDP where 4 is the top 25% quartile
        and 1 is the bottom 25% quartile
        - gdp_quartile_2020: the quartile of 'self's 2020 GDP where 4 is the top 25% quartile
        and 1 is the bottom 25% quartile
        - gdp_manufacturing_2016: GDP value of self in manufactoring sector in 2016
        - gdp_service_2016: GDP value of self in service sector in 2016
        - gdp_industry_2016: GDP value of self in industry sector in 2016
        - gdp_agriculture_forestry_fishing_2016: GDP value of self in agriculture sector in 2016
        - gdp_manufacturing_2017: GDP value of self in manufacturing sector in 2017
        - gdp_service_2017: GDP value of self in service sector in 2017
        - gdp_industry_2017: GDP value of self in industry sector in 2017
        - gdp_agriculture_forestry_fishing_2017: GDP value of self in agriculture sector in 2017
        - gdp_manufacturing_2018: GDP value of self in manufacturing sector in 2018
        - gdp_service_2018: GDP value of self in service sector in 2018
        - gdp_industry_2018: GDP value of self in industry sector in 2018
        - gdp_agriculture_forestry_fishing_2018: GDP value of self in agriculture sector in 2018
        - gdp_manufacturing_2019: GDP value of self in manufactoring sector in 2019
        - gdp_service_2019: GDP value of self in service sector in 2019
        - gdp_industry_2019: GDP value of self in industry sector in 2019
        - gdp_agriculture_forestry_fishing_2019: GDP value of self in agriculture sector in 2019
        - gdp_manufacturing_2020: GDP value of self in manufactoring sector in 2020
        - gdp_service_2020: GDP value of self in service sector in 2020
        - gdp_industry_2020: GDP value of self in industry sector in 2020
        - gdp_agriculture_forestry_fishing_2020: GDP value of self in agriculture section in 2020
        - unemployment_2016: unemployment rate of 'self' reported in year 2016
        - unemployment_2017: unemployment rate of 'self' in year 2017
        - unemployment_2018: unemployment rate of 'self' in year 2018
        - unemployment_2019: unemployment rate of 'self' in year 2019
        - unemployment_2020: unemployment rate of 'self' in year 2020

    Representation Invariants:
        - self.name != ''
        - (self.gdp_2016 == '' or self.gdp_2016 >= 0) and \
        (self.gdp_2017 == '' or self.gdp_2017 >= 0) and \
        (self.gdp_2018 == '' or self.gdp_2018 >= 0) and \
        (self.gdp_2019 == '' or self.gdp_2019 >= 0) and \
        (self.gdp_2020 == '' or self.gdp_2020 >= 0)
        - self.gdp_2016 in {1, 2, 3, 4, None} and self.gdp_2017 in {1, 2, 3, 4, None} and \
        self.gdp_2018 in {1, 2, 3, 4, None} and self.gdp_2019 in {1, 2, 3, 4, None} and \
        self.gdp_2020 in {1, 2, 3, 4, None}

    Sample Usage
    >>> Country('Canada')
    Country(name='Canada')
    """
    name: str
    gdp_2016: Optional[float]
    gdp_2017: Optional[float]
    gdp_2018: Optional[float]
    gdp_2019: Optional[float]
    gdp_2020: Optional[float]
    gdp_quartile_2016: Optional[float]
    gdp_quartile_2017: Optional[float]
    gdp_quartile_2018: Optional[float]
    gdp_quartile_2019: Optional[float]
    gdp_quartile_2020: Optional[float]
    gdp_manufacturing_2016: Optional[float]
    gdp_service_2016: Optional[float]
    gdp_industry_2016: Optional[float]
    gdp_agriculture_2016: Optional[float]
    gdp_manufacturing_2017: Optional[float]
    gdp_service_2017: Optional[float]
    gdp_industry_2017: Optional[float]
    gdp_agriculture_2017: Optional[float]
    gdp_manufacturing_2018: Optional[float]
    gdp_service_2018: Optional[float]
    gdp_industry_2018: Optional[float]
    gdp_agriculture_2018: Optional[float]
    gdp_manufacturing_2019: Optional[float]
    gdp_service_2019: Optional[float]
    gdp_industry_2019: Optional[float]
    gdp_agriculture_2019: Optional[float]
    gdp_manufacturing_2020: Optional[float]
    gdp_service_2020: Optional[float]
    gdp_industry_2020: Optional[float]
    gdp_agriculture_2020: Optional[float]
    unemployment_2016: Optional[float]
    unemployment_2017: Optional[float]
    unemployment_2018: Optional[float]
    unemployment_2019: Optional[float]
    unemployment_2020: Optional[float]

    def __init__(self, name: str) -> None:
        self.name = name

        self.gdp_2016 = None
        self.gdp_2017 = None
        self.gdp_2018 = None
        self.gdp_2019 = None
        self.gdp_2020 = None

        self.gdp_quartile_2016 = None
        self.gdp_quartile_2017 = None
        self.gdp_quartile_2018 = None
        self.gdp_quartile_2019 = None
        self.gdp_quartile_2020 = None

        self.gdp_manufacturing_2016 = None
        self.gdp_service_2016 = None
        self.gdp_industry_2016 = None
        self.gdp_agriculture_2016 = None
        self.gdp_manufacturing_2017 = None
        self.gdp_service_2017 = None
        self.gdp_industry_2017 = None
        self.gdp_agriculture_2017 = None
        self.gdp_manufacturing_2018 = None
        self.gdp_service_2018 = None
        self.gdp_industry_2018 = None
        self.gdp_agriculture_2018 = None
        self.gdp_manufacturing_2019 = None
        self.gdp_service_2019 = None
        self.gdp_industry_2019 = None
        self.gdp_agriculture_2019 = None
        self.gdp_manufacturing_2020 = None
        self.gdp_service_2020 = None
        self.gdp_industry_2020 = None
        self.gdp_agriculture_2020 = None

        self.unemployment_2016 = None
        self.unemployment_2017 = None
        self.unemployment_2018 = None
        self.unemployment_2019 = None
        self.unemployment_2020 = None

    def __str__(self) -> str:
        return self.name


def populate_dictionary() -> tuple[dict[str, Country], dict[str, str]]:
    """ Return a tuple of dictionary. The first dictionary maps the country code to a country name
    and the second dictionary maps the country name to a Country instance.
    """
    # initialize accumulators
    country_dict = {}
    code_dict = {}
    # open csv file
    with open('raw_data/national_gdp.csv') as file:
        reader = csv.reader(file, delimiter=',')
        # skip the first 5 lines
        for _ in range(5):
            next(reader)
        # iterate through all the remaining rows
        for row in reader:
            # get the country's name and country code
            name = row[0].capitalize()
            code = row[1]
            # map the name to a Country instance and the code to the name
            country_dict[name] = Country(name)
            code_dict[name] = code
    # return both accumulators
    return country_dict, code_dict


def populate_attribute_name(country_dict: dict, filename: str, lines: int, attributes: [str],
                            columns: [int]) -> None:
    """ Populate the attributes of Country instance attribute where the csv file contains the
    desired attribute in the attributes list. 'attributes' and 'columns' are parallel lists
    where attribute[i] can be found in columns[i] of the csv file.

    Preconditions:
        - len(attributes) == len(columns)
        - attribute[i] is an attribute of the Country class
        - all values in columns are less than the number of columns in the csv file row
    """
    # open csv file
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        # skip the first 'lines' lines
        for _ in range(lines):
            next(reader)
        # iterate through all the remaining rows
        for row in reader:
            # get the name of the country
            country = row[0].capitalize()
            # check country is in country_dict
            if country in country_dict:
                # iterate through all attributes and their respective columns
                for i in range(len(attributes)):
                    # convert data in csv file to float if possible, else keep as string
                    try:
                        setattr(country_dict[country], attributes[i], float(row[columns[i]]))
                    except ValueError:
                        setattr(country_dict[country], attributes[i], (row[columns[i]]))


def get_national_gdp(country_dict: dict) -> None:
    """ Retrieve national gdp data from national_gdp.csv
    """
    filename = 'raw_data/national_gdp.csv'
    attributes = ['gdp_2016', 'gdp_2017', 'gdp_2018', 'gdp_2019', 'gdp_2020']
    columns = [-5, -4, -3, -2, -1]
    populate_attribute_name(country_dict, filename, 4, attributes, columns)


def get_sector_gdp(country_dict: dict) -> None:
    """ Retrieve sector gdp data from sector_gdp.csv
    """
    # getting sector gdp attribute
    filename = 'raw_data/sector_gdp.csv'
    attributes = [
        'gdp_manufacturing_2016', 'gdp_service_2016', 'gdp_industry_2016',
        'gdp_agriculture_2016', 'gdp_manufacturing_2017',
        'gdp_service_2017', 'gdp_industry_2017', 'gdp_agriculture_2017',
        'gdp_manufacturing_2018', 'gdp_service_2018', 'gdp_industry_2018',
        'gdp_agriculture_2018', 'gdp_manufacturing_2019', 'gdp_service_2019',
        'gdp_industry_2019', 'gdp_agriculture_2019', 'gdp_manufacturing_2020',
        'gdp_service_2020', 'gdp_industry_2020', 'gdp_agriculture_2020'
    ]
    columns = list(range(2, 22))
    populate_attribute_name(country_dict, filename, 1, attributes, columns)


def get_unemployment(country_dict: dict) -> None:
    """ Retrieve unemployment rate data from unemployment_rate.csv
    """
    filename = 'raw_data/unemployment_rate.csv'
    attributes = [
        'unemployment_2016', 'unemployment_2017', 'unemployment_2018', 'unemployment_2019',
        'unemployment_2020'
    ]
    columns = [-5, -4, -3, -2, -1]
    populate_attribute_name(country_dict, filename, 4, attributes, columns)


def get_median(data: list[float], start: int, end: int) -> float:
    """ Return the median of the subarray data[start:end] where data is an increasing list

    Preconditions:
        - all(data[i] <= data[i + 1] for i in range(len(data) - 1))

    >>> get_median([1.0, 2.0, 3.0], 0, 3)
    2.0
    >>> get_median([1.0, 2.0, 3.0, 4.0], 0, 4)
    2.5
    """
    length = end - start
    if length % 2 == 0:
        mid1 = start + length // 2 - 1
        mid2 = start + length // 2
        median = (data[mid1] + data[mid2]) / 2
    else:
        mid = start + length // 2
        median = data[mid]
    return median


def get_quartile_split(country_dict: [str, Country], root: str, year: int) -> None:
    """ Sets the attribute gdp_quartile_xxxx where xxxx is year. The attribute can be assigned to
    1, 2, 3 or 4 (or remain unassigned if the country's GDP that year isn't available).
    """
    attr = root + str(year)
    data = []
    for country in country_dict:
        val = getattr(country_dict[country], attr)
        if isinstance(val, float):
            data.append(val)
    data.sort()
    median = get_median(data, 0, len(data))
    mid = len(data) // 2
    # get the median from lower half. 'mid' is never included
    lower_half_median = get_median(data, 0, mid)
    # get the median from upper half. 'mid' is included if len(data) is even and excluded if
    # len(data) is odd
    upper_half_median = get_median(data, mid + len(data) % 2, len(data))

    for country in country_dict:
        val = getattr(country_dict[country], attr)
        if not isinstance(val, float):
            continue
        if val <= lower_half_median:
            setattr(country_dict[country], f'gdp_quartile_{year}', 1)
        elif val <= median:
            setattr(country_dict[country], f'gdp_quartile_{year}', 2)
        elif val <= upper_half_median:
            setattr(country_dict[country], f'gdp_quartile_{year}', 3)
        else:
            setattr(country_dict[country], f'gdp_quartile_{year}', 4)


def get_gdp_quartile(country_dict: dict[str, Country], start: int, end: int) -> None:
    """ Sets the attribute gdp_quartile_xxxx where xxxx is in range [start, end + 1].
    The attribute can be assigned to 1, 2, 3 or 4 (or remain unassigned if the country's GDP
    that year isn't available).
    """
    for year in range(start, end + 1):
        get_quartile_split(country_dict, 'gdp_', year)


def clean_data() -> dict[str, Country]:
    """ Main method that contains helper function calls to clean data
    """
    # populate the dictionary with country names and Country instances
    country_dict = populate_dictionary()[0]
    # get required attributes from csv files
    get_national_gdp(country_dict)
    get_sector_gdp(country_dict)
    get_unemployment(country_dict)
    get_gdp_quartile(country_dict, 2016, 2020)
    # return cleaned data
    return country_dict


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'allowed-io': ['populate_dictionary', 'populate_attribute_name'],
        'extra-imports': ['python_ta.contracts', 'csv', 'typing'],
        'max-line-length': 100,
        'max-nested-blocks': 4,
        'disable': ['R1705', 'C0200']
    })
