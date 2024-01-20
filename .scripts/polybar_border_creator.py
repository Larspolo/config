import sys

RIGHT_TO_LEFT = ""
LEFT_TO_RIGHT = ""
PADDING = "  "
BLACK = "#11101d"
BLUE = "#216cce"
GREEN = "#007E33"
RED = "#CC0000"
ORANGE = "#FF8800"
YELLOW = "#E8A723"
MAGENTA = "#E64769"
PURPLE = "#473e62"
WHITE = "#FFFFFF"
COLORS = [
    BLUE,
    GREEN,
    RED,
    ORANGE,
    YELLOW,
    MAGENTA,
    PURPLE,
]
COLOR_MAP = {
    "BLUE": {
        "name": "BLUE",
        "hex": BLUE,
        "polybar": "${c.blue}",
    },
    "GREEN": {
        "name": "GREEN",
        "hex": GREEN,
        "polybar": "${c.green}",
    },
    "RED": {
        "name": "RED",
        "hex": RED,
        "polybar": "${c.red}",
    },
    "ORANGE": {
        "name": "ORANGE",
        "hex": ORANGE,
        "polybar": "${c.orange}",
    },
    "YELLOW": {
        "name": "YELLOW",
        "hex": YELLOW,
        "polybar": "${c.yellow}",
    },
    "MAGENTA": {
        "name": "MAGENTA",
        "hex": MAGENTA,
        "polybar": "${c.magenta}",
    },
    "PURPLE": {
        "name": "PURPLE",
        "hex": PURPLE,
        "polybar": "${c.purple}",
    },
    "BLACK": {
        "name": "BLACK",
        "hex": BLACK,
        "polybar": "${c.black}",
    },
    "WHITE": {
        "name": "WHITE",
        "hex": WHITE,
        "polybar": "${c.white}",
    },
}
SEPARATOR_MAP = {
    "LTR": {
        "name": "LTR",
        "polybar": LEFT_TO_RIGHT,
        "terminal": "▶",
    },
    "RTL": {
        "name": "RTL",
        "polybar": RIGHT_TO_LEFT,
        "terminal": "◀",
    },
}
RESET = "\033[0m"

current_direction = sys.argv[1].upper()
current_from_color = COLOR_MAP[sys.argv[2].upper()]
current_to_color = COLOR_MAP[sys.argv[3].upper()]
text_color = COLOR_MAP[sys.argv[4].upper()] if len(sys.argv) > 4 else WHITE


def color_to_bg(color):
    return "%{{B{}}}".format(color)


def color_to_fg(color):
    return "%{{F{}}}".format(color)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def get_rgb_color_escape(r, g, b, background=False):
    return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


def get_hex_color_escape(hex_color, background=False):
    return get_rgb_color_escape(*hex_to_rgb(hex_color), background=background)


def print_overview():
    print("Available colors:")
    for color in COLOR_MAP.values():
        print(
            get_hex_color_escape(color["hex"], background=True)
            + get_hex_color_escape(WHITE)
            + color["name"]
            + RESET
        )
    print("Available directions:")
    print(f"LTR: {LEFT_TO_RIGHT}")
    print(f"RTL: {RIGHT_TO_LEFT}")

    print("Current settings:")
    if current_direction == LEFT_TO_RIGHT:
        left_color = current_from_color
        right_color = current_to_color
    else:
        left_color = current_from_color
        right_color = current_to_color

    separator_bg_color = left_color if current_direction == "RTL" else right_color
    separator_fg_color = right_color if current_direction == "RTL" else left_color
    print(
        get_hex_color_escape(left_color["hex"], background=True)
        + get_hex_color_escape(WHITE)
        + left_color["name"]
        + RESET
        + get_hex_color_escape(separator_fg_color["hex"])
        + SEPARATOR_MAP[current_direction]["terminal"]
        + get_hex_color_escape(right_color["hex"], background=True)
        + get_hex_color_escape(WHITE)
        + right_color["name"]
        + RESET
    )
    print("For polybar:")
    print(
        # color_to_bg(left_color["hex"])
        # + color_to_fg(WHITE)
        # + left_color["name"]
        # +
        color_to_bg(separator_bg_color["hex"])
        + color_to_fg(separator_fg_color["hex"])
        + "  "
        + SEPARATOR_MAP[current_direction]["polybar"]
        + color_to_bg(right_color["hex"])
        + "  "
        + color_to_fg(WHITE)
        # + right_color["name"]
    )


def print_help():
    print("Usage:")
    print(f"python {sys.argv[0]} <direction> <from_color> <to_color> <text_color>")
    print("Example:")
    print(f"python {sys.argv[0]} LTR BLUE GREEN")
    print_overview()


print_help()
