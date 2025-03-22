import os
import subprocess
from vinery.dependency_graph import DependencyGraph
from vinery.io import read_file, update_file, echo

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


def list_workspaces(runner: str) -> list[str]:
    output = subprocess.run(
        args=[runner, "workspace", "list"],
        check=True,
        capture_output=True,
    ).stdout.decode().replace("*", "")

    return [line.strip() for line in output.split("\n") if line]


def select_workspace(workspace: str, runner: str) -> int:
    list_of_existing_workspaces = list_workspaces(runner)
    cmd = "new" if workspace not in list_of_existing_workspaces else "select"
    try:
        subprocess.run(
            args=[runner, "workspace", cmd, workspace],
            check=True,
        )
        echo(f"Selected workspace '{workspace}'.", log_level="INFO")
        return 0
    
    except subprocess.CalledProcessError:
        echo(f"Failed to select workspace '{workspace}'.", log_level="ERROR")
        return 1


def tf(
    plan: str,
    runner: str,
    cmd: str,
    path_to_library: str,
    save_output: bool = False,
) -> int:
    cmd = f"{runner} {cmd}"
    echo(f"tf('{plan}', '{cmd}', '{path_to_library}', {save_output})", log_level="DEBUG")
    echo(f"Running command '{cmd}' for plan '{plan}'.", log_level="INFO")
    
    try:
        output = subprocess.run(
            args=cmd,
            cwd=os.path.join(path_to_library, plan),
            check=True,
            capture_output=save_output,
            shell=True,
        )
        if save_output:
            update_file(
                f"{cmd.split(' ')[1]}_{plan.replace('/', '_')}.log",
                [output.stdout.decode()],
                dir='output'
            )
        echo(f"Command '{cmd}' for plan '{plan}' was successful!", log_level="SUCCESS")
        return 0
    
    except subprocess.CalledProcessError:
        echo(f"Command '{cmd}' failed for plan {plan}!", log_level="ERROR")
        return 1


def tf_loop(
    graph_of_plans_to_run: DependencyGraph,
    *args,
    reverse: bool = False,
    **kwargs
) -> DependencyGraph:
    return graph_of_plans_to_run.wsubgraph({
        plan for plan in graph_of_plans_to_run.sorted_list(reverse)
        if tf(plan, *args, **kwargs) == 0
    })


def init(graph_of_plans, path_to_library, runner, upgrade) -> DependencyGraph:
    graph_of_plans_initialized = graph_of_plans.wsubgraph(
        read_file("init_status") if not upgrade else set()
    )
    graph_of_plans_to_initialize = graph_of_plans - graph_of_plans_initialized

    if not graph_of_plans_to_initialize:
        echo("No plans require initialization.", log_level="INFO")
        if not upgrade:
            echo("Did you mean to run -upgrade?", log_level="INFO")
        return graph_of_plans.wsubgraph(graph_of_plans_initialized.nodes)

    graph_of_plans_initialized += tf_loop(
        graph_of_plans_to_initialize,
        runner, f"init{' -upgrade' if upgrade else ''}", path_to_library,
    )

    update_file("init_status", graph_of_plans_initialized.nodes)

    return graph_of_plans_initialized


def with_tf_init(function):
    """
    Decorator that runs 'init' before the function.
    """
    def wrapper(graph_of_plans, path_to_library, runner, upgrade, *args, **kwargs):
        graph_of_plans_initialized = init(graph_of_plans, path_to_library, runner, upgrade=upgrade)
        return function(graph_of_plans_initialized, path_to_library, runner, *args, **kwargs)

    return wrapper


@with_tf_init
def validate(graph_of_plans_initialized, path_to_library, runner, json) -> DependencyGraph:
    return tf_loop(
        graph_of_plans_initialized,
        runner, f"validate{' -json' if json else ''}", path_to_library,
        save_output=json,
    )


@with_tf_init
def plan(graph_of_plans_initialized, path_to_library, runner) -> DependencyGraph:
    return tf_loop(
        graph_of_plans_initialized,
        runner, "plan", path_to_library,
    )


@with_tf_init
def apply(graph_of_plans_initialized, path_to_library, runner, auto_approve) -> DependencyGraph:
    return tf_loop(
        graph_of_plans_initialized,
        runner, f"apply{' -auto-approve' if auto_approve else ''}", path_to_library,
    )


@with_tf_init
def destroy(graph_of_plans_initialized, path_to_library, runner, auto_approve) -> DependencyGraph:
    return tf_loop(
        graph_of_plans_initialized,
        runner, f"destroy{' -auto-approve' if auto_approve else ''}", path_to_library, reverse=True,
    )
