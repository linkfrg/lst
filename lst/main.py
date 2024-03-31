import argparse
import os
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
gi.require_version("GdkPixbuf", "2.0")
gi.require_version("DbusmenuGtk3", "0.4")
gi.require_version('NM', '1.0')
gi.require_version("Gst", "1.0")
from lst.app import app, APP_INTERFACE_NAME  # noqa: E402
from gi.repository import Gio, GLib  # noqa: E402
from lst.client import LstClient  # noqa: E402


def parse_arguments():
    parser = argparse.ArgumentParser(description="Linkfrg's PyGTK Shell", prog="lst")
    parser.add_argument(
        "--config",
        "-c",
        default="~/.config/lst/config.py",
        help="Path to the configuration file (default: ~/.config/lst/config.py)",
    )
    parser.add_argument(
        "--open",
        metavar="WINDOW",
        help="Open a window",
    )
    parser.add_argument(
        "--close",
        metavar="WINDOW",
        help="Close a window",
    )
    parser.add_argument(
        "--toggle",
        metavar="WINDOW",
        help="Toggle a window",
    )
    parser.add_argument(
        "--list-windows",
        action="store_true",
        help="List all windows",
    )
    parser.add_argument(
        "--run-python",
        metavar="CODE",
        help="Execute inline python code",
    )
    parser.add_argument(
        "--run-file",
        metavar="FILE",
        help="Execute python file",
    )
    parser.add_argument(
        "--inspector",
        action="store_true",
        help="Open Inspector",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Reload LST",
    )
    parser.add_argument(
        "--quit",
        action="store_true",
        help="Quit LST",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    result = bus.call_sync(
        "org.freedesktop.DBus",
        "/org/freedesktop/DBus",
        "org.freedesktop.DBus",
        "NameHasOwner",
        GLib.Variant("(s)", (APP_INTERFACE_NAME,)),
        GLib.VariantType("(b)"),
        Gio.DBusCallFlags.NONE,
        -1,
        None,
    ).unpack()[0]

    if not result:
        run_server(args.config)
    else:
        client = LstClient()
        if args.open:
            client.OpenWindow(args.open)

        elif args.close:
            client.CloseWindow(args.close)

        elif args.toggle:
            client.ToggleWindow(args.toggle)

        elif args.list_windows:
            client.ListWindows()

        elif args.run_python:
            client.RunPython(args.run_python)

        elif args.run_file:
            client.RunFile(args.run_file)

        elif args.inspector:
            client.Inspector()

        elif args.reload:
            client.Reload()

        elif args.quit:
            client.Quit()

        elif args.version:
            print("lst 1.0")

        else:
            print("lst is already running")
            exit(1)


def run_server(config):
    config_path = os.path.expanduser(config)

    config_dir = os.path.dirname(config_path)
    config_filename = os.path.splitext(os.path.basename(config_path))[0]

    app.setup(config_dir, config_filename)

    try:
        app.run(None)
    except KeyboardInterrupt:
        app.quit()


if __name__ == "__main__":
    main()
