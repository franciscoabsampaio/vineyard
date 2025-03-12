import os
import subprocess
from vineyard.dependency_graph import DependencyGraph
from vineyard.io import read_file, update_file, echo

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


def tf(
    plan: str,
    runner: str,
    cmd: str,
    path_to_plans: str,
    save_output: bool = False,
) -> int:
    echo(f"tf('{plan}', '{runner}', '{cmd}', '{path_to_plans}', {save_output})", log_level="DEBUG")

    echo(f"Running command '{cmd}' for plan '{plan}'.", log_level="INFO")
    
    try:
        output = subprocess.run(
            args=[runner, cmd],
            cwd=os.path.join(path_to_plans, plan),
            check=True,
            capture_output=save_output,
        )
        if save_output:
            update_file(f"{cmd.split(' ')[0]}_{plan}.log", [output.stdout.decode()], dir='output')

        echo(f"Command '{cmd}' for plan '{plan}' was successful!", log_level="SUCCESS")
        return 0
    except subprocess.CalledProcessError:

        echo(f"Command '{cmd}' failed for plan {plan}!", log_level="ERROR")
        return 1


def tf_loop(
    set_of_plans_to_run: set[str],
    *args,
    **kwargs
) -> set[str]:
    return {
        plan for plan in set_of_plans_to_run
        if tf(plan, *args, **kwargs) == 0
    }


def init(plan, path_to_plans, runner, recursive, upgrade) -> set[str]:
    set_of_plans = set(
        DependencyGraph()
        .from_path_to_plans(path_to_plans)
        .from_dependency_subgraph(plan).nodes
    ) if recursive else {plan}

    set_of_plans_initialized = read_file("init_status") if not upgrade else set()
    set_of_plans_to_initialize = set_of_plans - set_of_plans_initialized

    if not set_of_plans_to_initialize:
        echo("No plans require initialization. Did you mean to run -upgrade?", log_level="INFO")
        return set_of_plans_initialized

    set_of_plans_initialized.update(tf_loop(
        set_of_plans_to_initialize,
        runner, f"init {' -upgrade' if upgrade else ''}", path_to_plans,
    ))

    update_file("init_status", set_of_plans_initialized)

    return set_of_plans_initialized


def validate(plan, path_to_plans, runner, recursive, json) -> set[str]:
    set_of_plans_initialized = init(plan, path_to_plans, runner, recursive, upgrade=True)

    set_of_plans_validated = tf_loop(
        set_of_plans_initialized,
        runner, f"validate{' -json' if json else ''}", path_to_plans,
        save_output=json,
    )

    return set_of_plans_validated


def plan(plan, path_to_plans, runner, recursive, json) -> set[str]:
    set_of_plans_initialized = init(plan, path_to_plans, runner, recursive, upgrade=True)

    set_of_plans_planned = tf_loop(  # lol
        set_of_plans_initialized,
        runner, f"plan{' -json' if json else ''}", path_to_plans,
    )

    return set_of_plans_planned

# tf apply


# tf destroy
