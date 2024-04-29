#!/usr/bin/env python3.8

import i3ipc


ENVS = {}
F_KEYS = ["F1", "F2", "F3", "F4"]


class Workspace:
    def __init__(self, env, section, index):
        self.env = env
        self.section = section
        self.index = index

    def __str__(self):
        return f"{self.env}~{self.section}~{self.index}"


def name_to_values(name):
    try:
        print("NAME: ", name)
        env, section, index = name.split("~")
        return (env, section, index)
    except Exception:
        print(f"Could not convert: {name}")
        return ("", "F1", "1")


def values_to_name(env, section, index):
    return "~".join([env, section, str(index)])


def get_last_index(env, section):
    i = 0
    for workspace in i3.get_workspaces():
        try:
            if (
                name_to_values(workspace.name)[1] == section
                and env == name_to_values(workspace.name)[0]
            ):
                i += 1
        except Exception:
            continue
    return i


def rename_workspace(name, env, section, index):
    if section not in F_KEYS:
        section = "F1"
        index = get_last_index(env, section) + 1
    resp = i3.command(
        f"rename workspace {name} to {values_to_name(env, section, index)}"
    )
    print(resp[0])
    if not resp[0].success:
        index = get_last_index(env, section) + 1
        resp = i3.command(
            f"rename workspace {name} to {values_to_name(env, section, index)}"
        )
        if not resp[0].success:
            print(name, "could not be renamed to", values_to_name(env, section, index))
            raise Exception(resp[0]["error"])
        else:
            print(name, "renamed to", values_to_name(env, section, index))
    else:
        print(name, "renamed to", values_to_name(env, section, index))


def refactor_workspaces(self=None, e=None):
    indici = {}
    for workspace in i3.get_workspaces():
        env = workspace.output
        name = workspace.name
        try:
            _, section, _ = name_to_values(name)
        except Exception:
            section = "F1"
        if env in indici:
            if section in indici[env]:
                indici[env][section] += 1
            else:
                indici[env][section] = 1
        else:
            indici[env] = {section: 1}
        rename_workspace(name, "TEMP__" + env, section, indici[env][section])
    for workspace in i3.get_workspaces():
        env, section, index = name_to_values(workspace.name)
        rename_workspace(workspace.name, env[6:], section, index)


def go_to(workspace):
    print("GOTO:", workspace)
    i3.command(f"workspace {workspace}")


def on_binding_run(self=None, e=None):
    if e.binding.command == "nop":
        workspace = i3.get_tree().find_focused().workspace()
        env, section, index = name_to_values(workspace.name)
        env = workspace.parent.parent.name

        # Switch to another section
        if e.binding.symbol in F_KEYS:
            section = e.binding.symbol
            if "shift" in e.binding.mods:
                i3.command(
                    f"move container to workspace {values_to_name(env, section, index)}"
                )

            # TODO Foreach monitor go to a workspace on that section.
            go_to(values_to_name(env, section, index))
            refactor_workspaces()

        # Switch to another workspace
        elif "0" <= e.binding.symbol <= "9":
            index = int(e.binding.symbol)
            if "shift" in e.binding.mods:
                i3.command(
                    f"move container to workspace {values_to_name(env, section, index)}"
                )

            go_to(values_to_name(env, section, index))
            refactor_workspaces()

        # Open rofi in new workspace
        elif e.binding.symbol == "d":
            index = get_last_index(env, section) + 1
            i3.command(f"workspace {values_to_name(env, section, index)}")
            i3.command("""exec ~/.scripts/rofi_launcher.sh""")
            refactor_workspaces()


if __name__ == "__main__":
    i3 = i3ipc.Connection()

    refactor_workspaces()

    i3.on("binding::run", on_binding_run)
    i3.on("workspace::move", refactor_workspaces)
    for method in [
        # "focus",
        "close",
        "move",
    ]:
        i3.on(f"window::{method}", refactor_workspaces)
    try:
        i3.main()
    except KeyboardInterrupt:
        i3.main_quit()
