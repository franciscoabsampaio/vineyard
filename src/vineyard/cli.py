import click
import os
import subprocess
from vineyard.cli_options import options_tf, option_runner
from vineyard.io import LOG_LEVELS
from vineyard import tf


@click.group()
@click.option(
    '--log_level', '-l',
    default="INFO",
    show_default=True,
    envvar="VINE_LOG_LEVEL",
    help=f"""
    Set the global log level for the CLI.
    Can be overridden by setting the VINE_LOG_LEVEL environment variable.
    
    Accepted values: {LOG_LEVELS}
    """
)
def cli(log_level: str):
    """
    Manage infrastructure plans.
    """
    if log_level not in LOG_LEVELS:
        raise ValueError(f"Invalid log level: {log_level}. Accepted values: {LOG_LEVELS}")
    os.environ["VINE_LOG_LEVEL"] = os.getenv("VINE_LOG_LEVEL", log_level)


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
def init(plan: str, path_to_plans: str, runner: str, recursive: bool, upgrade: bool):
    """
    Initialize all infrastructure plans.
    """
    tf.init(plan, path_to_plans, runner, recursive, upgrade)


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
def validate(plan: str, path_to_plans: str, runner: str, recursive: bool, json: bool):
    """
    Validate plans' syntax and correctness.
    By default, runs 'RUNNER init -upgrade' prior to execution.
    Plans that fail to 'init' are not validated.
    """
    tf.validate(plan, path_to_plans, runner, recursive, json)


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
def plan(plan: str, path_to_plans: str, runner: str, recursive: bool, upgrade: bool):
    """
    ???
    """
    tf.plan(plan, path_to_plans, runner, recursive, upgrade)
