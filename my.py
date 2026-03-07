file = open("config.txt", "r")
content = [line.strip() for line in file.readlines()]
d_config = dict()
for c in content:
    k, v = c.split("=")
    d_config[k] = v
# === VALIDATION CHECKS ===
# width height entry and exit:
try:
    m_width = int(d_config["WIDTH"])
    m_height = int(d_config["HEIGHT"])
    if m_width < 0 or m_height < 0:
        raise ValueError("")
except ValueError:
    raise ValueError("Configuration must be a valid value.")
try:
    x_entry, y_entry = map(int, d_config["ENTRY"].split(","))
    x_exit, y_exit = map(int, d_config["EXIT"].split(","))
except ValueError:
    raise ValueError("Your x,y entry/exit are wrong! fix that")
#    ------------------  han fin zayd ljadid -----------------
if not (0 <= x_entry < m_width) or not (0 <= y_entry < m_height):
    raise ValueError("The entry is out of bounds!")
if not (0 <= x_exit < m_width) or not (0 <= y_exit < m_height):
    raise ValueError("The exit is out of bounds!")
elif (x_entry, y_entry) == (x_exit, y_exit):
    raise ValueError(
        "x and y entry cannot be the same as x_exit and y_exit. therefore change them!"
    )
