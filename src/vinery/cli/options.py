import click
from typing import Literal
from vinery.cli.arguments import argument_plan
from vinery.io import echo


def option_auto_approve(function: callable):
    return click.option(
        '--auto-approve', '-a', '-auto-approve',
        default=False,
        is_flag=True,
        help="Pass -auto-approve flag to 'RUNNER apply/destroy'."
    )(function)


def option_path_to_library(function: callable):    
    return click.option(
        '--path-to-library', '-p', '-path-to-library',
        help='Path to the directory with all infrastructure plans.',
        default='./library',
        envvar='VINERY_PATH_TO_LIBRARY',
        required=True,
        show_default=True,
    )(function)


def option_runner(function: callable):
    """
    Automatically checks if the runner is installed.
    """
    from vinery.tf import load_runners

    def callback(ctx, param, value: Literal["terraform", "tofu"]):
        runners_available = load_runners()
        if value not in runners_available:
            echo(f"Runner '{value}' is not installed.", log_level="ERROR")
        
        ctx.ensure_object(dict)
        ctx.obj['runner'] = value
        return value

    return click.option(
        '--runner', '-r', '-runner',
        help='Select the preferred runner for managing infrastructure.',
        default='terraform',
        show_default=True,
        callback=callback
    )(function)


def option_recursive(function: callable):
    return click.option(
        '--recursive', '-rr', '-recursive',
        help='Apply the command recursively.',
        default=True,
        show_default=True,
        required=True
    )(function)


def option_upgrade(function: callable):
    return click.option(
        '--upgrade', '-u', '-upgrade',
        default=False,
        is_flag=True,
        help="Pass -upgrade flag to 'RUNNER init'."
    )(function)


def options_tf(function: callable):
    function = option_upgrade(function)
    function = option_recursive(function)
    function = option_runner(function)
    function = argument_plan(function)

    return function
