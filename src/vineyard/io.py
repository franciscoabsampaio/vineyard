import click
from datetime import datetime
from pathlib import Path
import os


DIRECTORIES = {
    'tmp': '/tmp/vineyard',
    'output': f'{Path().resolve()}/outputs'
}
for dir in DIRECTORIES.values():
    Path(dir).mkdir(parents=True, exist_ok=True)

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "SUCCESS", "ERROR"]


def read_file(filename: str, dir: str = 'tmp') -> set[str]:
    try:
        with open(os.path.join(DIRECTORIES[dir], filename), "r") as f:
            return set(f.readlines())
    except FileNotFoundError:
        echo(f"File {filename} not found in {DIRECTORIES[dir]}.", log_level="WARNING")
        return set()


def update_file(filename: str, new_lines: list[str], dir: str = 'tmp') -> set[str]:
    contents = read_file(filename)

    for line in new_lines:
        contents.add(line)
    
    with open(os.path.join(DIRECTORIES[dir], filename), "w") as f:
        f.writelines(contents)


def echo(message: str, log_level: str = "INFO") -> None:
    """
    Custom logging function with color-coded output.
    """
    if LOG_LEVELS.index(log_level) < LOG_LEVELS.index(os.getenv("VINE_LOG_LEVEL", 1)):
        return  # Suppress messages below the global log level

    message = f"{datetime.now().time().isoformat(timespec='seconds')} vineyard: [{log_level}] {message}"

    match log_level:
        case "DEBUG":
            click.secho(message)
        case "INFO":
            click.secho(message, fg="blue", bold=True)
        case "WARNING":
            click.secho(message, fg="yellow")
        case "SUCCESS":
            click.secho(message, fg="green", bold=True)
        case "ERROR":
            click.secho(message, fg="red", bold=True, err=True)
