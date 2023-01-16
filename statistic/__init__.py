from os import getenv

from .google_sheets import update_statistic_table
from .statistic_data import make_purchases_statistic, make_fueling_statistic


__all__ = ['update_purchases_statistic']


def update_purchases_statistic():
    SHEET_NAME = getenv('GOOGLE_SHEET_NAME')
    PURCHASES_WORKSHEET_NAME = getenv('GOOGLE_PURCHASES_WORKSHEET')

    if not PURCHASES_WORKSHEET_NAME or not SHEET_NAME:
        return

    update_statistic_table(
        make_purchases_statistic(),
        SHEET_NAME,
        PURCHASES_WORKSHEET_NAME
    )


def update_fuelings_statistic():
    SHEET_NAME = getenv('GOOGLE_SHEET_NAME')
    FUELINGS_WORKSHEET_NAME = getenv('GOOGLE_FUELINGS_WORKSHEET')

    if not FUELINGS_WORKSHEET_NAME or not SHEET_NAME:
        return

    update_statistic_table(
        make_fueling_statistic(),
        SHEET_NAME,
        FUELINGS_WORKSHEET_NAME
    )
