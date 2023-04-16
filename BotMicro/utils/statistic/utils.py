from typing import Any


def escape_dict_strings(data: dict[str, Any]) -> dict[str, Any]:
    new_data = {}
    for key in data:
        if isinstance(data[key], str):
            new_data[key] = escape_string(data[key])
        else:
            new_data[key] = data[key]
            
    return data
    

def escape_string(string: str) -> str:
    return f'="{string}"'
    