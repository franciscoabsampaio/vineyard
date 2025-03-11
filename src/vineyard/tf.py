import click
import os
import subprocess
from vineyard.dependency_graph import DependencyGraph
from vineyard.io import read_temp_file, update_temp_file, echo

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


def tf(runner: str, cmd: str, path_to_plans: str, plan: str):
    echo(f"Running command {cmd} for plan {plan}.", log_level="INFO")
    subprocess.run(args=[runner, cmd], cwd=os.path.join(path_to_plans, plan))


def init(plan, path_to_plans, plans, runner, recursive, upgrade):
    set_of_plans = set(plans.nodes) if recursive else {plan}

    plans_already_initialized = read_temp_file("init_status") if not upgrade else set()
    plans_to_initialize = set_of_plans - plans_already_initialized

    for plan in plans_to_initialize:
        tf(runner, "init", path_to_plans, plan)

    update_temp_file("init_status", plans_to_initialize)


# tf plan


# tf apply


# tf destroy
