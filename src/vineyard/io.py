import click
from datetime import datetime
from pathlib import Path
import os
from typing import Literal


DIRECTORY_TEMP = '/tmp/vineyard'
DIRECTORY_OUTPUT = f'{Path().resolve()}/outputs'


Path(DIRECTORY_TEMP).mkdir(parents=True, exist_ok=True)
Path(DIRECTORY_OUTPUT).mkdir(parents=True, exist_ok=True)


def read_temp_file(filename: str, dir: str = DIRECTORY_TEMP) -> set[str]:
    try:
        with open(os.path.join(dir, filename), "r") as f:
            return set(f.readlines())
    except FileNotFoundError:
        echo(f"File {filename} not found in {dir}.", log_level="WARNING")
        return set()


def update_temp_file(filename: str, new_lines: list[str], dir: str = DIRECTORY_TEMP) -> set[str]:
    contents = read_temp_file(filename)

    for line in new_lines:
        contents.add(line)
    
    with open(os.path.join(dir, filename), "w") as f:
        f.writelines(contents)


def echo(message: str, log_level: Literal["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"] = "INFO") -> None:
    """Custom logging function with color-coded output."""
    global_log_level = os.getenv("VINEYARD_LOG_LEVEL", 1)

    if ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"].index(log_level) < global_log_level:
        return  # Suppress messages below the global log level

    message = f"{datetime.now().time().isoformat(timespec='seconds')} vineyard: [{log_level}] {message}"

    match log_level:
        case "DEBUG":
            click.secho(message)
        case "INFO":
            click.secho(message, fg="blue", bold=True)
        case "SUCCESS":
            click.secho(message, fg="green", bold=True)
        case "WARNING":
            click.secho(message, fg="yellow")
        case "ERROR":
            click.secho(message, fg="red", bold=True, err=True)
