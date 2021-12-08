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
        - gdp_manufacturing_2017: GDP value of self in manufacturing sector in 2016
        - gdp_service_2017: GDP value of self in service sector in 2016
        - gdp_industry_2017: GDP value of self in industry sector in 2016
        - gdp_agriculture_forestry_fishing_2017: GDP value of self in agriculture sector in 2016
        - gdp_manufacturing_2018: GDP value of self in manufacturing sector in 2016
        - gdp_service_2018: GDP value of self in service sector in 2016
        - gdp_industry_2018: GDP value of self in industry sector in 2016
        - gdp_agriculture_forestry_fishing_2018: GDP value of self in agriculture sector in 2016
        - gdp_manufacturing_2019: GDP value of self in manufactoring sector in 2016
        - gdp_service_2019: GDP value of self in service sector in 2016
        - gdp_industry_2019: GDP value of self in industry sector in 2016
        - gdp_agriculture_forestry_fishing_2019: GDP value of self in agriculture sector in 2016
        - gdp_manufacturing_2020: GDP value of self in manufactoring sector in 2016
        - gdp_service_2020: GDP value of self in service sector in 2016
        - gdp_industry_2020: GDP value of self in industry sector in 2016
        - gdp_agriculture_forestry_fishing_2020: GDP value of self in agriculture section in 2016
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

        self.income_group = None

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


def populate_dictionary() -> tuple[dict[str, str], dict[str, Country]]:
    """ Return a tuple of dictionary. The first dictionary maps the country code to a country name
    and the second dictionary maps the country name to a Country instance.
    """
    # initialize accumulators
    country_dict = {}
    code_to_country = {}
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
            code_to_country[code] = name
    # return both accumulators
    return code_to_country, country_dict


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


def populate_attribute_code(country_dict: dict, code_to_country: dict, filename: str, lines: int,
                            attributes: [str], columns: [int], code_col: int) -> None:
    """ Populate the attributes of Country instance attribute where csv file contains the country
    code.
    """
    # open csv file
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        # skip the first 'lines' lines
        for _ in range(lines):
            next(reader)
        # iterate through all the remaining rows
        for row in reader:
            # get the country's code and map the code to the name
            country = code_to_country[row[code_col]]
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


def get_income_group(country_dict: dict, code_to_country: dict) -> None:
    """ Retrieve income quartile data from country_income_quartile.csv
    """
    filename = 'raw_data/country_income_quartile.csv'
    attributes = ['income_group']
    columns = [2]
    populate_attribute_code(country_dict, code_to_country, filename, 1, attributes, columns, 0)


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


def clean_data() -> dict[str, Country]:
    """ Main method that contains helper function calls to clean data
    """
    # populate the dictionary with country names and Country instances
    code_to_country, country_dict = populate_dictionary()
    # get required attributes from csv files
    get_national_gdp(country_dict)
    get_income_group(country_dict, code_to_country)
    get_sector_gdp(country_dict)
    get_unemployment(country_dict)
    # return cleaned data
    return country_dict
