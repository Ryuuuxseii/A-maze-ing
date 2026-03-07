import mazegen


def config_parser():
    """
    this function takes the data from the config.txt
    file and checks its validity.
    """

    # fetching the data from config.txt:

    d_config = {}
    try:
        with open("config.txt", 'r') as file:
            content = [line.strip() for line in file if line != '\n']
    except FileNotFoundError:
        raise FileNotFoundError('"config.txt" doesnt exist!')

    # content is a list of stripped lines:

    for c in content:
        if c[0] != "#":     # --- the if is to ignore comments in .txt
            k, v = c.split("=")
            d_config[k] = v
    print(d_config)

    # ========= VALIDATION CHECKS =========

    keys = ["HEIGHT", "ENTRY", "EXIT", "WIDTH", "PERFECT", "OUTPUT_FILE"]
    try:
        for key in keys:
            d_config[key]
    except KeyError:
        raise KeyError(f"MANDATORY KEY DOES NOT EXIST GNG : {key}")

    # width and height :

    try:
        m_width = int(d_config["WIDTH"])
        m_height = int(d_config["HEIGHT"])
        if m_width < 0 or m_height < 0:
            raise ValueError("HEIGHT and WIDTH can't be negative >:()")
    except ValueError:
        raise ValueError("Configuration must be a valid value!!")

    # entry and exit:

    try:
        x_entry, y_entry = map(int, d_config["ENTRY"].split(","))
        x_exit, y_exit = map(int, d_config["EXIT"].split(","))
    except ValueError:
        raise ValueError("ENTRY/EXIT are absurd!")

    # perfect maze:

    if (d_config["PERFECT"].title() != "True" and
            d_config["PERFECT"].title() != "False"):
        raise ValueError("PERFECT should be a boolean value (TRUE/FALSE!)")

    # Coordinates validation fr professionally checked this time:

    if not (0 <= x_entry < m_width) or not (0 <= y_entry < m_height):
        raise ValueError("The entry is out of bounds!")
    if not (0 <= x_exit < m_width) or not (0 <= y_exit < m_height):
        raise ValueError("The exit is out of bounds!")
    elif (x_entry, y_entry) == (x_exit, y_exit):
        raise ValueError("x and y entry cannot be the same as x_exit and "
                         "y_exit. Change them!")


def main():
    """
    Main function of the program.
    """
    try:
        config_parser()
    except (ValueError, FileNotFoundError, KeyError) as e:
        print("Error: ", e)


main()
