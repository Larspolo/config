#!/usr/bin/env python3

import i3ipc
import sys
import os
import logging


logging.basicConfig(filename="/tmp/poly.log", level=logging.DEBUG)

ICON_MAP = [
    {"names": ["discord"], "icon": "", "weight": 5},
    {
        "names": ["gnome-control-center", "gnome-tweaks", "Gnome-tweaks"],
        "icon": "",
        "weight": 5,
    },
    {
        "names": ["URxvt", "Gnome-terminal", "jetbrains-studio", "st"],
        "icon": "",
        "weight": 1,
    },
    {
        "names": ["google_chrome", "Google-chrome", "chromium", "Chromium"],
        "icon": "",
        "weight": 3,
    },
    {"names": ["Firefox", "firefox"], "icon": "", "weight": 3},
    {"names": ["Atom", "vim", "code", "vscode", "Code"], "icon": "", "weight": 10},
    {"names": ["Evince"], "icon": "", "weight": 2},
    {"names": ["Pinta", "Gimp"], "icon": "", "weight": 3},
    {"names": ["DBeaver"], "icon": "", "weight": 3},
    {"names": ["Slack"], "icon": "", "weight": 3},
    {"names": ["Thunderbird"], "icon": "", "weight": 3},
    {"names": ["nomacs", "Image Lounge"], "icon": "", "weight": 3},
    {"names": ["virt-manager", "Virt-manager"], "icon": "", "weight": 3},
    {"names": ["STACK", "Stack", "stack"], "icon": "", "weight": 3},
    {"names": ["Signal"], "icon": "", "weight": 3},
    {"names": ["Remmina", "remmina"], "icon": "RDP", "weight": 3},
    {"names": ["Bluetooth"], "icon": "", "weight": 3},
    {
        "names": ["Teams", "teams-for-linux", "teams_for_linux"],
        "icon": "",
        "weight": 3,
    },
    {"names": ["Nautilus", "org.gnome.Nautilus", "Thunar"], "icon": "", "weight": 3},
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


def get_icons(ws):
    leaves = get_leaves(ws)
    if not leaves:
        return ["+"]

    icon_maps = [
        icon_map
        for c in leaves
        for icon_map in ICON_MAP
        if (
            c.window_class in icon_map["names"]
            or c.window_title in icon_map["names"]
            or (c.window_title and icon_map.get("names", [])[0] in c.window_title)
        )
    ]

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
