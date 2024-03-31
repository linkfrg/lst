import json

def write_json(path: str, data: dict) -> None:
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def read_json(path: str, empty: dict) -> None:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception:
        write_json(path, empty)
        return empty