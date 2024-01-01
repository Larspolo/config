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
        "weight": HIGH,
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
        "names": ["google_chrome", "Google-chrome", "chromium", "Chromium"],
        "icon": icons["chrome"],
        "weight": HIGH,
    },
    {
        "names": ["Firefox", "firefox", "Firefox-esr"],
        "icon": icons["firefox"],
        "weight": HIGH,
    },
    # Code
    {
        "names": ["Atom", "vim", "code", "vscode", "Code"],
        "icon": icons["code"],
        "weight": HIGHEST,
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
        "names": ["libreoffice-writer"],
        "icon": icons["file-word"],
        "weight": HIGH,
    },
    {
        "names": ["libreoffice-calc"],
        "icon": icons["file-excel"],
        "weight": HIGH,
    },
    {
        "names": ["libreoffice-writer"],
        "icon": icons["file-word"],
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
]

F_KEYS = ["F1", "F2", "F3", "F4"]
PADDING = "  "
COLORS = [
    "#5e8d87",
    "#85678f",
    "#de935f",
    "#8c9440",
]
TEXT_COLOR = "#FFF"

backgrounds_colors = {
    "F1": "#5e8d87",
    "F2": "#85678f",
    "F3": "#de935f",
    "F4": "#8c9440",
}


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


def icontains(string, lst):
    """Check if a string is in the list, case insensitive"""
    return string and string.upper() in map(str.upper, lst)


def any_item_icontains(string, lst):
    """Check if a string is in the list, case insensitive"""
    return string and any(name.upper() in string.upper() for name in lst)


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


def set_bg_color(color):
    return "%{{B{}}}".format(color)


def set_fg_color(color):
    return "%{{F{}}}".format(color)


def set_command_on_click(command, text):
    return "%{{A1:{}:}}{}%{{A}}".format(command, text)


def set_text_color(ws):
    if ws.focused:
        return set_fg_color("#323234")
    elif ws.urgent:
        return set_fg_color("#990000")
    else:
        return set_fg_color(TEXT_COLOR)


def set_border(ws):
    i = get_index(ws)
    current = (i - 1) % len(COLORS)
    # On the first workspace, we don't want a border
    if i == 1:
        return set_bg_color(COLORS[current]) + set_text_color(ws)

    prev = (i - 2) % len(COLORS)
    return "".join(
        [
            set_bg_color(COLORS[current]) + set_fg_color(COLORS[prev]),
            "",
            set_bg_color(COLORS[current]) + set_text_color(ws),
        ]
    )


def get_workspace_text(ws):
    return set_command_on_click(
        "i3-msg workspace {}".format(ws.name),
        PADDING.join(
            [
                set_border(ws),
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

    for ws in sorted_ws:
        if ws.output != os.environ.get("MONITOR", "eDP-1"):
            continue

        bar[name_to_values(ws.name)[1]] += get_workspace_text(ws)

    # Add group styling
    bar = [
        PADDING.join(
            [
                set_bg_color(COLORS[0]),
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
