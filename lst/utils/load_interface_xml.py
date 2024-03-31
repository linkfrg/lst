import os

def load_interface_xml(filename: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dbus_dir = os.path.join(current_dir, '..', 'dbus')
    file_path = os.path.join(dbus_dir, filename)
    with open(file_path, "r") as file:
        xml = file.read()
    return xml