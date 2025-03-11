import click
import subprocess
from vineyard.dependency_graph import DependencyGraph
from vineyard.cli_options import options_tf, option_runner
from vineyard import tf


@click.group()
def cli():
    pass


@cli.command(
    help="Recursively format all infrastructure plans."
)
@option_runner
def fmt(runner: str):
    subprocess.run(args=[runner, "fmt", "-recursive"])


@cli.command(
    help="Initialize the infrastructure plans."
)
@options_tf
@click.option(
    '--upgrade', '-u', '-upgrade',
    default=False,
    is_flag=True,
    help="Pass -upgrade flag to 'RUNNER init'."
)
@click.pass_context
def init(ctx, plan: str, path_to_plans: str, runner: str, recursive: bool, upgrade: bool):
    plans = ctx.obj['plans']

    tf.init(plan, path_to_plans, plans, runner, recursive, upgrade)
