import click
from tf import tf, RunnerNotFoundError
from vineyard.dependency_graph import DependencyGraph


@click.command()
@click.option(
    '--plan', '-p',
    help='Infrastructure plan name.',
    # required=True
)
@click.option(
    '--env',
    help='Environment name.',
    # required=True
)
@click.option(
    '--path-to-plans',
    help='Path to the directory with all infrastructure plans.',
    default='./tf-plans', show_default=True
)
def cli(plan: str, env: str, path_to_plans: str):
    """
    args:
        env: Environment name.
    """
    # Build dependency graph
    dependency_graph = DependencyGraph().from_path_to_plans(path_to_plans)

    try:
        tf(env)
    except RunnerNotFoundError as e:
        click.echo(e, err=True)
