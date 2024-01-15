#!/usr/bin/env python3

import i3ipc
import sys
import os
import logging
from fontawesome import icons


logging.basicConfig(filename="/tmp/poly.log", level=logging.DEBUG)

HIGHEST = 10000
HIGH = 1000
MEDIUM = 100
LOW = 10
LOWEST = 1


ICON_MAP = [
    # Social
    {
        "names": ["discord"],
        "icon": "",
        "weight": HIGHEST,
    },
    {
        "names": ["Slack"],
        "icon": "",
        "weight": HIGH,
    },
    {
        "names": ["Signal"],
        "icon": icons["comment"],
        "weight": HIGH,
    },
    {
        "names": ["Teams", "teams-for-linux", "teams_for_linux"],
        "icon": icons["users"],
        "weight": HIGH,
    },
    # Browsers
    {
        "names": ["google_chrome", "google-chrome", "chromium", "Chromium"],
        "icon": icons["chrome"],
        "weight": HIGH,
    },
    {
        "names": ["firefox", "Firefox-esr"],
        "icon": icons["firefox"],
        "weight": HIGH,
    },
    # Code
    {
        "names": ["github"],
        "icon": icons["github"],
        "weight": HIGH,
    },
    {
        "names": ["atom", "vim", "vscode"],
        "icon": icons["code"],
        "weight": HIGH,
    },
    {
        "names": ["code"],
        "icon": icons["code"],
        "weight": MEDIUM + 1,
    },
    {
        "names": ["DBeaver"],
        "icon": icons["database"],
        "weight": MEDIUM,
    },
    {
        "names": ["gnome-control-center", "gnome-tweaks", "Gnome-tweaks"],
        "icon": icons["cog"],
        "weight": MEDIUM,
    },
    {
        "names": ["URxvt", "Gnome-terminal", "jetbrains-studio", "st"],
        "icon": icons["terminal"],
        "weight": LOWEST,
    },
    {
        "names": ["test"],
        "icon": icons["flask"],
        "weight": LOW,
    },
    {
        "names": ["run-"],
        "icon": icons["microchip"],
        "weight": LOW,
    },
    # Images
    {
        "names": ["Pinta", "Gimp"],
        "icon": icons["magic"],
        "weight": HIGH,
    },
    {
        "names": ["feh", "nomacs", "Image Lounge"],
        "icon": icons["images"],
        "weight": HIGH,
    },
    # Office
    {
        "names": ["libreoffice-calc"],
        "icon": icons["table"],
        "weight": HIGH,
    },
    {
        "names": ["libreoffice-writer"],
        "icon": icons["align-left"],
        "weight": HIGH,
    },
    {
        "names": ["libreoffice-impress"],
        "icon": icons["file-powerpoint"],
        "weight": HIGH,
    },
    {
        "names": ["libreoffice"],
        "icon": icons["file"],
        "weight": MEDIUM,
    },
    {
        "names": ["Evince"],
        "icon": icons["file-pdf"],
        "weight": MEDIUM,
    },
    # Utils
    {
        "names": ["Bluetooth"],
        "icon": icons["bluetooth-b"],
        "weight": MEDIUM,
    },
    {
        "names": ["Nautilus", "org.gnome.Nautilus", "Thunar"],
        "icon": icons["folder"],
        "weight": MEDIUM,
    },
    # Other
    {
        "names": ["Thunderbird"],
        "icon": icons["envelope-open"],
        "weight": MEDIUM,
    },
    {
        "names": ["stack"],
        "icon": icons["sync-alt"],
        "weight": MEDIUM,
    },
    {
        "names": ["remmina"],
        "icon": icons["laptop"],
        "weight": MEDIUM,
    },
    {
        "names": ["virt-manager"],
        "icon": icons["server"],
        "weight": MEDIUM,
    },
    {
        "names": ["obs"],
        "icon": icons["video"],
        "weight": HIGH,
    },
]

F_KEYS = ["F1", "F2", "F3", "F4"]
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
TEXT_COLOR = WHITE


def name_to_values(name):
    try:
        env, section, index = name.split("~")
        return (env, section, index)
    except Exception:
        print(f"Could not convert: {name}")
        raise Exception


def get_index(ws):
    return int(name_to_values(ws.name)[2])


def get_leaves(ws):
    try:
        return next(
            (w for w in i3.get_tree().workspaces() if w.name == ws.name)
        ).leaves()
    except StopIteration:
        return []


def prepare_str_compare(string):
    return string and string.upper().replace("-", "_").replace(".", "_")


def icontains(string, lst):
    """Check if a string is in the list, case insensitive"""
    return string and prepare_str_compare(string) in map(prepare_str_compare, lst)


def any_item_icontains(string, lst):
    """Check if a string is in the list, case insensitive"""
    return string and any(
        prepare_str_compare(name) in prepare_str_compare(string) for name in lst
    )


def get_icons(ws):
    leaves = get_leaves(ws)
    if not leaves:
        return ["+"]

    icon_maps = []
    for c in leaves:
        matching_icons = []
        for icon_map in ICON_MAP:
            if icontains(c.window_class, icon_map["names"]):
                matching_icons.append(icon_map)
            if icontains(c.window_title, icon_map["names"]):
                matching_icons.append(icon_map)
            if any_item_icontains(c.window_title, icon_map["names"]):
                matching_icons.append(icon_map)
        if matching_icons:
            icon_maps.append(max(matching_icons, key=lambda x: x["weight"]))

    if not icon_maps:
        return [str(get_index(ws))]

    return [
        icon_map["icon"] for icon_map in sorted(icon_maps, key=lambda x: -x["weight"])
    ]


def color_to_bg(color):
    return "%{{B{}}}".format(color)


def color_to_fg(color):
    return "%{{F{}}}".format(color)


def set_command_on_click(command, text):
    return "%{{A1:{}:}}{}%{{A}}".format(command, text)


def get_index_color(ws):
    return COLORS[(get_index(ws) - 1) % len(COLORS)]


def get_text_color(ws):
    if not ws:
        return TEXT_COLOR
    if ws.urgent:
        return RED
    if ws.focused:
        return BLACK
    else:
        return TEXT_COLOR


def get_bg_color(ws):
    if not ws:
        return COLORS[0]
    if ws.urgent:
        return WHITE
    if ws.focused:
        return WHITE
    else:
        return get_index_color(ws)


def set_border(prev_ws, ws):
    current_bg = get_bg_color(ws)
    current_text = get_text_color(ws)

    prev_bg = get_bg_color(prev_ws)
    return "".join(
        [
            color_to_bg(current_bg) + color_to_fg(prev_bg),
            "",
            color_to_bg(current_bg) + color_to_fg(current_text),
        ]
    )


def get_workspace_text(ws):
    return set_command_on_click(
        "i3-msg workspace {}".format(ws.name),
        PADDING.join(
            [
                "",  # Extra padding
                *get_icons(ws),
                "",  # Extra padding
            ]
        ),
    )


def reset_colors():
    return "%{B-}%{F-}"


def print_bar(self=None, e=None):
    bar = {section: "" for section in F_KEYS}
    # Sort workspaces based on [-1]
    sorted_ws = i3.get_workspaces()
    sorted_ws.sort(key=lambda ws: int(ws.name[-1]))

    prev_wss = {section: None for section in F_KEYS}
    for ws in sorted_ws:
        if ws.output != os.environ.get("MONITOR", "eDP-1"):
            continue
        section = name_to_values(ws.name)[1]
        bar[section] += set_border(prev_wss[section], ws) + get_workspace_text(ws)
        prev_wss[section] = ws

    # Add group styling
    bar = [
        PADDING.join(
            [
                color_to_bg(COLORS[0]),
                section,
                workspaces + reset_colors(),
            ]
        )
        for section, workspaces in bar.items()
    ]

    print((PADDING * 2).join(bar))
    sys.stdout.flush()


if __name__ == "__main__":
    i3 = i3ipc.Connection()
    for method in [
        "focus",
        "init",
        "empty",
        "urgent",
        "reload",
        "rename",
        "restored",
        "move",
    ]:
        i3.on(f"workspace::{method}", print_bar)

    for method in ["focus", "close", "move"]:
        i3.on(f"window::{method}", print_bar)

    try:
        print_bar()
        i3.main()
    except KeyboardInterrupt:
        i3.main_quit()
