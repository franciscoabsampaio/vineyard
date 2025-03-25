from vinery.io import DIRECTORIES, setup_directories, set_log_level, setup_library, echo
import os


def setup(ctx, log_level: str, path_to_library: str, directories: str = DIRECTORIES) -> None:
    """
    Set up the vinery CLI.
    """
    try:
        set_log_level(log_level)
    except ValueError as e:
        echo(str(e), log_level="ERROR")
        ctx.exit(1)

    if all([os.path.isdir(dir) for dir in directories.values()]):
        echo(f"Working directories already exist.", log_level="DEBUG")
    else:
        setup_directories(directories=directories)
        echo("Working directories created successfully.", log_level="INFO")

    if os.path.isdir(f"{path_to_library}/default"):
        echo(f"Library already exists at {path_to_library}.", log_level="DEBUG")
    else:
        try:
            setup_library(path_to_library)
        except FileNotFoundError as e:
            echo(str(e), log_level="ERROR")
            ctx.exit(1)
        echo(f"Library plans copied to {path_to_library}.", log_level="INFO")

    echo(f"--log-level: {log_level}", log_level="DEBUG")
    echo(f"--path-to-library: {path_to_library}", log_level="DEBUG")
