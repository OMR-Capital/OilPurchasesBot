from typing import Any


def escape_dict_strings(data: dict[str, Any]) -> dict[str, Any]:
    return {key: escape_string(value) for key, value in data.items() if isinstance(value, str)}
    

def escape_string(string: str) -> str:
    return f'="{string}"'
    