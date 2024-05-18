import subprocess
from typing import NoReturn
import click

from src.app.opener import get_random_open_cmd


@click.command()
def pronapp() -> NoReturn:
    while True:
        click.confirm(text="Press anything to open the next sauce", show_default=False)
        cmd = get_random_open_cmd()
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    pronapp()
