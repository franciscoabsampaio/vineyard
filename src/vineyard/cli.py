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
def init(plan: str, path_to_library: str, runner: str, recursive: bool, upgrade: bool):
    """
    Initialize all infrastructure plans.
    """
    tf.init(plan, path_to_library, runner, recursive, upgrade)


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
def validate(plan: str, path_to_library: str, runner: str, recursive: bool, upgrade: bool, json: bool):
    """
    Validate plans' syntax and correctness.
    By default, runs 'RUNNER init -upgrade' prior to execution.
    Plans that fail to 'init' are not validated.
    """
    tf.validate(plan, path_to_library, runner, recursive, upgrade, json)


########################
# plan
@cli.command()
@options_tf
def plan(plan: str, path_to_library: str, runner: str, recursive: bool, upgrade: bool):
    """
    Execute a dry run of all infrastructure plans,
    showing what changes would be made.
    """
    tf.plan(plan, path_to_library, runner, recursive, upgrade)


########################
# apply
@cli.command()
@options_tf
def apply(plan: str, path_to_library: str, runner: str, recursive: bool, upgrade: bool):
    """
    Apply the plans, building the infrastructure and applying any latent changes.
    """
    tf.apply(plan, path_to_library, runner, recursive, upgrade)


########################
# destroy
@cli.command()
@options_tf
def destroy(plan: str, path_to_library: str, runner: str, recursive: bool, upgrade: bool):
    """
    Destroy all infrastructure described in the associated set of plans.
    """
    tf.destroy(plan, path_to_library, runner, recursive, upgrade)
