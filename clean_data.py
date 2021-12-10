"""
Process data from csv files into a dictionary populate with Country class instance
"""

import csv


class Country:
    """ A class representing each country with their associated statistics


    Instance Attributes:
        - gdp_2016: national GDP value of 'self' reported in the year 2016
        - gdp_2017: national GDP value of 'self' reported in the year 2017
        - gdp_2018: national GDP value of 'self' reported in the year 2018
        - gdp_2019: national GDP value of 'self' reported in the year 2019
        - gdp_2020: national GDP value of 'self' reported in the year 2020
        - income_group: income rating of country ('High...', 'Medium...', 'Low..')
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
        - unemployment_2016: unemployment value of 'self' reported in year 2016
        - unemployment_2017: unemployment value of 'self' reported in year 2017
        - unemployment_2018: unemployment value of 'self' reported in year 2018
        - unemployment_2019: unemployment value of 'self' reported in year 2019
        - unemployment_2020: unemployment value of 'self' reported in year 2020

    Representation Invariants:
        - self.name != ''


    """

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
        self.gdp_agriculture_forestry_fishing_2016 = None
        self.gdp_manufacturing_2017 = None
        self.gdp_service_2017 = None
        self.gdp_industry_2017 = None
        self.gdp_agriculture_forestry_fishing_2017 = None
        self.gdp_manufacturing_2018 = None
        self.gdp_service_2018 = None
        self.gdp_industry_2018 = None
        self.gdp_agriculture_forestry_fishing_2018 = None
        self.gdp_manufacturing_2019 = None
        self.gdp_service_2019 = None
        self.gdp_industry_2019 = None
        self.gdp_agriculture_forestry_fishing_2019 = None
        self.gdp_manufacturing_2020 = None
        self.gdp_service_2020 = None
        self.gdp_industry_2020 = None
        self.gdp_agriculture_forestry_fishing_2020 = None

        self.unemployment_2016 = None
        self.unemployment_2017 = None
        self.unemployment_2018 = None
        self.unemployment_2019 = None
        self.unemployment_2020 = None

    def __str__(self) -> str:
        return self.name


def populate_dictionary() -> dict[str, Country]:
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
            # map the name to a Country instance
            country_dict[name] = Country(name)

    # return accumulator
    return country_dict


def populate_attribute_name(country_dict: dict, filename: str, lines: int, attributes: [str],
                            columns: [int], name_col: int) -> None:
    """ Populate the attributes of Country instance attribute where csv file contains the country
    name.
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
            country = row[name_col].capitalize()
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
    populate_attribute_name(country_dict, filename, 4, attributes, columns, 0)


def get_sector_gdp(country_dict: dict) -> None:
    """ Retrieve sector gdp data from sector_gdp.csv"""
    # getting sector gdp attribute
    filename = 'raw_data/sector_gdp.csv'
    attributes = [
        'gdp_manufacturing_2016', 'gdp_service_2016', 'gdp_industry_2016',
        'gdp_agriculture_forestry_fishing_2016', 'gdp_manufacturing_2017',
        'gdp_service_2017', 'gdp_industry_2017', 'gdp_agriculture_forestry_fishing_2017',
        'gdp_manufacturing_2018', 'gdp_service_2018', 'gdp_industry_2018',
        'gdp_agriculture_forestry_fishing_2018', 'gdp_manufacturing_2019', 'gdp_service_2019',
        'gdp_industry_2019', 'gdp_agriculture_forestry_fishing_2019', 'gdp_manufacturing_2020',
        'gdp_service_2020', 'gdp_industry_2020', 'gdp_agriculture_forestry_fishing_2020'
    ]
    columns = list(range(2, 22))
    populate_attribute_name(country_dict, filename, 1, attributes, columns, 0)


def get_unemployment(country_dict: dict) -> None:
    """ Retrieve unemployment data from unemployment_rate.csv
    """
    filename = 'raw_data/unemployment_rate.csv'
    attributes = [
        'unemployment_2016', 'unemployment_2017', 'unemployment_2018', 'unemployment_2019',
        'unemployment_2020'
    ]
    columns = [-5, -4, -3, -2, -1]
    populate_attribute_name(country_dict, filename, 4, attributes, columns, 0)


def get_gdp_quartile(country_dict: dict[str, Country]) -> None:
    """ Assign each country to a gdp_quartile for years 2016 to 2020
    """
    for year in range(2016, 2021):
        get_quartile_split(country_dict, 'gdp_', year)


def get_median(data: list[float], start: int, end: int) -> float:
    """ Return the median of the subarray data[start:end]
    """
    length = end - start
    if length % 2 == 0:
        mid1 = start + length // 2
        mid2 = start + length // 2 + 1
        median = (data[mid1] + data[mid2]) / 2
    else:
        mid = start + length // 2
        median = data[mid]
    return median


def get_quartile_split(country_dict: [str, Country], root: str, year: int) -> None:
    """ Returns a list of 4 sets where each set contains name of countries in each quartile
    for the given attribute (root + year)
    """
    attr = root + str(year)
    data = []
    for country in country_dict:
        val = getattr(country_dict[country], attr)
        if type(val) == float:
            data.append(val)
    data.sort()
    median = get_median(data, 0, len(data))
    mid = len(data) // 2
    lower_half_median = get_median(data, 0, mid)
    upper_half_median = get_median(data, mid + len(data) % 2, len(data))

    for country in country_dict:
        val = getattr(country_dict[country], attr)
        if type(val) != float:
            continue
        if val <= lower_half_median:
            setattr(country_dict[country], f'gdp_quartile_{year}', 1)
        elif val <= median:
            setattr(country_dict[country], f'gdp_quartile_{year}', 2)
        elif val <= upper_half_median:
            setattr(country_dict[country], f'gdp_quartile_{year}', 3)
        else:
            setattr(country_dict[country], f'gdp_quartile_{year}', 4)


def clean_data() -> dict[str, Country]:
    """ Main method that contains helper function calls to clean data
    """
    # populate the dictionary with country names and Country instances
    country_dict = populate_dictionary()
    # get required attributes from csv files
    get_national_gdp(country_dict)
    get_gdp_quartile(country_dict)
    get_sector_gdp(country_dict)
    get_unemployment(country_dict)
    # return cleaned data
    return country_dict
