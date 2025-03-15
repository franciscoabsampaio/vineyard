from vineyard.io import DIRECTORIES, setup_directories, set_log_level, setup_library, echo
import os


def setup(log_level: str, path_to_library: str):
    """
    Set up the vineyard CLI.
    """
    if all([os.path.isdir(dir) for dir in DIRECTORIES.values()]):
        echo(f"Working directories already exist.", log_level="DEBUG")
    else:
        setup_directories()
        echo("Working directories created successfully.", log_level="INFO")

    set_log_level(log_level)

    if os.path.isdir(f"{path_to_library}/default"):
        echo(f"Library already exists at {path_to_library}.", log_level="DEBUG")
    else:
        setup_library(path_to_library)
        echo(f"Library plans copied to {path_to_library}.", log_level="INFO")

    echo(f"--log-level: {log_level}", log_level="DEBUG")
    echo(f"--path-to-library: {path_to_library}", log_level="DEBUG")
