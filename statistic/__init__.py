from .google_sheets import update_statistic_table
from .statistic_data import make_statistic


__all__ = ['update_statistic']


def update_statistic():
    update_statistic_table(make_statistic())