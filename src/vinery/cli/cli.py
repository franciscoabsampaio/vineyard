import click
import subprocess
import vinery
from vinery.cli.options import option_path_to_library, options_tf, option_runner, option_auto_approve
from vinery.cli.options_tf_vars import options_tf_vars
from vinery.dependency_graph import DependencyGraph
from vinery.io import LOG_LEVELS
from vinery.cli.setup import setup
from vinery import tf


@click.group()
@click.option(
    '--log_level', '-l',
    default="INFO",
    envvar="VINE_LOG_LEVEL",
    help=f"""
    Set the global log level for the CLI.
    Can be overridden by setting the VINE_LOG_LEVEL environment variable.
    
    Accepted values: {LOG_LEVELS}
    """,
    show_default=True
)
@option_path_to_library
@click.pass_context
def cli(ctx, log_level: str, path_to_library: str):
    """
    Manage infrastructure plans.
    """
    setup(log_level, path_to_library)


########################
# version
@cli.command(
    help="""
    Get the version of the CLI.
    """
)
def version():
    print(vinery.__version__)


########################
# fmt
@cli.command(
    help="Recursively format all infrastructure plans."
)
@option_runner
@click.pass_context
def fmt(ctx, runner: str):
    subprocess.run(args=[runner, "fmt", "-recursive"], cwd=ctx.obj["path_to_library"])


########################
# init
@cli.command()
@options_tf
@click.pass_context
def init(ctx, plan: str, runner: str, recursive: bool, upgrade: bool):
    """
    Initialize all infrastructure plans.
    """
    tf.init(ctx.obj["graph"], ctx.obj["path_to_library"], runner, upgrade)


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
def validate(ctx, plan: str, runner: str, recursive: bool, upgrade: bool, json: bool):
    """
    Validate plans' syntax and correctness.
    By default, runs 'RUNNER init -upgrade' prior to execution.
    Plans that fail to 'init' are not validated.
    """
    tf.validate(ctx.obj["graph"], ctx.obj["path_to_library"], runner, upgrade, json)


########################
# plan
@cli.command()
@options_tf
@options_tf_vars
@click.pass_context
def plan(ctx, plan: str, runner: str, recursive: bool, upgrade: bool):
    """
    Execute a dry run of all infrastructure plans,
    showing what changes would be made.
    """
    tf.plan(ctx.obj["graph"], ctx.obj["path_to_library"], runner, upgrade)


########################
# apply
@cli.command()
@options_tf
@option_auto_approve
@options_tf_vars
@click.pass_context
def apply(ctx, plan: str, runner: str, recursive: bool, upgrade: bool, auto_approve: bool):
    """
    Apply the plans, building the infrastructure and applying any latent changes.
    """
    tf.apply(ctx.obj["graph"], ctx.obj["path_to_library"], runner, upgrade, auto_approve)


########################
# destroy
@cli.command()
@options_tf
@option_auto_approve
@click.pass_context
def destroy(ctx, plan: str, runner: str, recursive: bool, upgrade: bool, auto_approve: bool):
    """
    Destroy all infrastructure described in the associated set of plans.
    """
    tf.destroy(ctx.obj["graph"], ctx.obj["path_to_library"], runner, upgrade, auto_approve)
