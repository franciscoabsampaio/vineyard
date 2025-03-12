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


def tf(runner: str, cmd: str, path_to_plans: str, plan: str) -> int:
    echo(f"Running command {cmd} for plan {plan}.", log_level="INFO")
    
    try:
        subprocess.run(args=[runner, cmd], cwd=os.path.join(path_to_plans, plan), check=True)
        return 0
    except subprocess.CalledProcessError:
        return 1


def init(plan, path_to_plans, plans, runner, recursive, upgrade) -> set[str]:
    set_of_plans = set(plans.nodes) if recursive else {plan}

    plans_initialized = read_temp_file("init_status") if not upgrade else set()
    plans_to_initialize = set_of_plans - plans_initialized

    for plan in plans_to_initialize:
        if tf(runner, "init", path_to_plans, plan) == 0:
            plans_initialized.add(plan)
        else:
            echo(f"Failed to initialize plan {plan}.", log_level="ERROR")

    update_temp_file("init_status", plans_initialized)

    return plans_initialized


def validate(plan, path_to_plans, plans, runner, recursive, json) -> set[str]:
    set_of_plans_initialized = init(plan, path_to_plans, plans, runner, recursive, upgrade=True)


# tf apply


# tf destroy
