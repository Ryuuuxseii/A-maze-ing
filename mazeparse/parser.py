from typing import Union, Any

Coords = tuple[int, int]


def config_parser(filename: str) -> dict[str, Any]:
    """
    Parses 'config.txt' and returns a dictionary of settings.
    """

    d_config: dict[str, str] = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    d_config[k.strip()] = v.strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f'The config file named "{filename}" does not exist!'
            )

    # ========= VALIDATION =========

    mandatory_keys = [
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "WIDTH",
        "PERFECT",
        "OUTPUT_FILE"
    ]

    for key in mandatory_keys:
        if key not in d_config:
            raise KeyError(f"MANDATORY KEY DOES NOT EXIST: {key}")

    # perfect maze validation
    perfect_val = d_config["PERFECT"].title()

    if perfect_val != "True" and perfect_val != "False":
        raise ValueError("PERFECT should be TRUE or FALSE")

    perfect_bool = perfect_val == "True"

    # convert ENTRY and EXIT into exact tuple[int, int]
    entry_parts = d_config["ENTRY"].split(",")
    exit_parts = d_config["EXIT"].split(",")

    if len(entry_parts) != 2 or len(exit_parts) != 2:
        raise ValueError("ENTRY and EXIT must be in format x,y")

    entry_tuple: Coords = (int(entry_parts[0]), int(entry_parts[1]))
    exit_tuple: Coords = (int(exit_parts[0]), int(exit_parts[1]))

    # create settings dictionary
    s = {
        "WIDTH": int(d_config["WIDTH"]),
        "HEIGHT": int(d_config["HEIGHT"]),
        "PERFECT": perfect_bool,
        "ENTRY": entry_tuple,
        "EXIT": exit_tuple,
        "OUTPUT_FILE": d_config["OUTPUT_FILE"]
    }

    # 42 limitation
    if (s["HEIGHT"] < 8 or s["WIDTH"] < 12):
        raise ValueError(
            "The maze dimensions are too small to fit the '42' pattern."
            )

    if "SEED" in d_config:
        s["SEED"] = d_config["SEED"]

    return s
