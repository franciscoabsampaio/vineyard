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
    reverse: bool = False,
    *args,
    **kwargs
) -> DependencyGraph:
    return graph_of_plans_to_run.subgraph({
        plan for plan in graph_of_plans_to_run.sorted_list(reverse)
        if tf(plan, *args, **kwargs) == 0
    })


def init(plan, path_to_library, runner, recursive, upgrade) -> DependencyGraph:
    graph_of_plans = (
        DependencyGraph()
        .from_library(path_to_library)
        .subgraph_from_node(plan).nodes
    ) if recursive else DependencyGraph().add_node(plan)

    graph_of_plans_initialized = graph_of_plans.subgraph(
        read_file("init_status") if not upgrade else set()
    )
    graph_of_plans_to_initialize = graph_of_plans.subtract(graph_of_plans_initialized)

    if not graph_of_plans_to_initialize:
        echo("No plans require initialization. Did you mean to run -upgrade?", log_level="INFO")
        return graph_of_plans.subgraph(graph_of_plans_initialized.nodes)

    graph_of_plans_initialized.add(tf_loop(
        graph_of_plans_to_initialize,
        runner, f"init{' -upgrade' if upgrade else ''}", path_to_library,
    ).nodes)

    update_file("init_status", graph_of_plans_initialized.nodes)

    return graph_of_plans_initialized


def validate(plan, path_to_library, runner, recursive, upgrade, json) -> DependencyGraph:
    graph_of_plans_initialized = init(plan, path_to_library, runner, recursive, upgrade=upgrade)

    graph_of_plans_validated = tf_loop(
        graph_of_plans_initialized,
        runner, f"validate{' -json' if json else ''}", path_to_library,
        save_output=json,
    )

    return graph_of_plans_validated


def plan(plan, path_to_library, runner, recursive, upgrade) -> DependencyGraph:
    graph_of_plans_initialized = init(plan, path_to_library, runner, recursive, upgrade=upgrade)

    graph_of_plans_planned = tf_loop(
        graph_of_plans_initialized,
        runner, "plan", path_to_library,
    )

    return graph_of_plans_planned


def apply(plan, path_to_library, runner, recursive, upgrade) -> DependencyGraph:
    graph_of_plans_initialized = init(plan, path_to_library, runner, recursive, upgrade=upgrade)

    graph_of_plans_applied = tf_loop(
        graph_of_plans_initialized,
        runner, "apply", path_to_library,
    )

    return graph_of_plans_applied


def destroy(plan, path_to_library, runner, recursive, upgrade) -> DependencyGraph:
    graph_of_plans_initialized = init(plan, path_to_library, runner, recursive, upgrade=upgrade)

    graph_of_plans_destroyed = tf_loop(
        graph_of_plans_initialized,
        runner, "destroy", path_to_library, reverse=True,
    )

    return graph_of_plans_destroyed
