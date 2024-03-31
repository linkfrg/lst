import subprocess


def check_output(command: str):
    result = subprocess.check_output(command.split(" "), text=True)
    return result
