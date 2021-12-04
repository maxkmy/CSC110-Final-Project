""" Contains functions to perform various computations
"""


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
