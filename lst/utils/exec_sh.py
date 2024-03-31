import threading
import subprocess
import sys


def exec_sh(command: str, print_output: bool = False) -> None:
    if print_output:
        stdout = sys.stdout
        stderr = sys.stderr
    else:
        stdout = subprocess.DEVNULL
        stderr = subprocess.DEVNULL

    threading.Thread(
        target=lambda: subprocess.run(
            command.split(" "), text=True, stdout=stdout, stderr=stderr
        )
    ).start()
