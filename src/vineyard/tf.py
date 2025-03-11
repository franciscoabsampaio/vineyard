import subprocess
from typing import Literal

SUPPORTED_RUNNERS=["terraform", "tofu"]


class RunnerNotFoundError(Exception):
    pass


def load_runners() -> list[str]:
    runners = [
        runner for runner in SUPPORTED_RUNNERS
        if subprocess.run(
            args=["which", runner],
            capture_output=True
        ).stdout.decode().strip()
    ]

    if not runners:
        raise RunnerNotFoundError("ERROR: No runner is installed.")
    
    return runners


def tf(env: str, runner: Literal["tofu", "terraform"] = "tofu"):
    """
    args:
        runner: By default, the runner is set to tofu.
    """
    runners_available = load_runners()
