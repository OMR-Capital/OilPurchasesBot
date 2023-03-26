from typing import Any, Optional

from gspread.exceptions import WorksheetNotFound
from gspread.spreadsheet import Spreadsheet
from gspread.utils import ValueInputOption
from gspread.worksheet import Worksheet
from gspread.cell import Cell
from google_sheets_utils.cells import get_cells_range

from google_sheets_utils.client import get_client


def get_worksheet(table_name: str, worksheet_name: str) -> Optional[Worksheet]:
    """Return worksheet from table by name. If worksheet not found, create new one"""

    client = get_client()
    if not client:
        return None

    sheet: Spreadsheet = client.open(table_name)
    try:
        worksheet: Worksheet = sheet.worksheet(worksheet_name)
    except WorksheetNotFound:
        worksheet: Worksheet = sheet.add_worksheet(worksheet_name, rows=1, cols=1)

    return worksheet


def update_header(worksheet: Worksheet, header_data: list[Any]):
    """Update first line of worksheet with header data"""

    worksheet.update(
        get_cells_range(1, 1, len(header_data), 1),
        [header_data],
        value_input_option=ValueInputOption.user_entered
    )
    worksheet.freeze(rows=1)


def add_row(worksheet: Worksheet, row_data: list[Any]):
    """Add new row to worksheet"""

    worksheet.append_row(row_data, value_input_option=ValueInputOption.user_entered)
    return worksheet.row_count + 1


def update_row_by_key(worksheet: Worksheet, key: str, row_data: list[Any]) -> Optional[int]:
    """Update row with specified key in first column. Return row number or None if row not found"""

    cell: Optional[Cell] = worksheet.find(key, in_column=1, case_sensitive=True)
    if not cell:
        return None

    worksheet.update(
        get_cells_range(cell.row, 1, len(row_data), 1),
        [row_data],
        value_input_option=ValueInputOption.user_entered
    )
    return cell.row


def remove_row_by_key(worksheet: Worksheet, key: str) -> Optional[int]:
    """Remove row with specified key in first column. Return row number or None if row not found"""

    cell: Optional[Cell] = worksheet.find(key, in_column=1, case_sensitive=True)
    if not cell:
        return None

    worksheet.delete_row(cell.row)
    return cell.row


def sort_by_column(worksheet: Worksheet, column: int, reverse: bool = False):
    """Sort worksheet by column number"""

    # A1:ZZ99999 used to skip first frozen row
    worksheet.sort((column, 'asc' if not reverse else 'des'), range='A1:ZZ99999')
                                      