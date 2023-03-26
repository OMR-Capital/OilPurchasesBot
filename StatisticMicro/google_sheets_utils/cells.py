def get_column_letter(column: int) -> str:
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if column <= 26:
        return letters[column - 1]
    else:
        return letters[column // 26 - 1] + letters[column % 26 - 1]


def get_cells_range(first_row: int, first_column: int, width: int, height: int) -> str:
    return f'{get_column_letter(first_column)}{first_row}:{get_column_letter(first_column + width - 1)}{first_row + height - 1}'
