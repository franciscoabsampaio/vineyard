import click
import subprocess
from vineyard.dependency_graph import DependencyGraph
from vineyard.cli_options import options_tf, option_runner
from vineyard import tf


@click.group()
def cli():
    """
    Manage infrastructure plans.
    """
    pass


########################
# fmt
@cli.command(
    help="Recursively format all infrastructure plans."
)
@option_runner
def fmt(runner: str):
    subprocess.run(args=[runner, "fmt", "-recursive"])


########################
# init
@cli.command()
@options_tf
@click.option(
    '--upgrade', '-u', '-upgrade',
    default=False,
    is_flag=True,
    help="Pass -upgrade flag to 'RUNNER init'."
)
@click.pass_context
def init(ctx, plan: str, path_to_plans: str, runner: str, recursive: bool, upgrade: bool):
    """
    Initialize all infrastructure plans.
    """
    plans = ctx.obj['plans']

    tf.init(plan, path_to_plans, plans, runner, recursive, upgrade)


########################
# validate
@cli.command()
@options_tf
@click.option(
    '--json', '-j', '-json',
    default=False,
    is_flag=True,
    help="""
    Pass -json flag to 'RUNNER plan'.
    Additionally, saves JSON output to a file.
    """
)
@click.pass_context
def validate(ctx, plan: str, path_to_plans: str, runner: str, recursive: bool, json: bool):
    """
    Validate plans' syntax and correctness.
    By default, runs 'RUNNER init -upgrade' prior to execution.
    Plans that fail to 'init' are not validated.
    """

    plans = ctx.obj['plans']

    tf.validate(plan, path_to_plans, plans, runner, recursive, json)


########################
# plan
@cli.command()
@options_tf
@click.option(
    '--upgrade', '-u', '-upgrade',
    default=False,
    is_flag=True,
    help="Pass -upgrade flag to 'RUNNER init'."
)
@click.pass_context
def plan(ctx, plan: str, path_to_plans: str, runner: str, recursive: bool, upgrade: bool):
    """
    ???
    """
    
    plans = ctx.obj['plans']

    tf.init(plan, path_to_plans, plans, runner, recursive, upgrade)
