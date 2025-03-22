import click
from typing import Literal
from vinery.cli.arguments import argument_plan
from vinery.dependency_graph import DependencyGraph
from vinery.io import echo
import sys


def option_path_to_library(function: callable):    
    def callback(ctx, param, value):
        ctx.ensure_object(dict)
        ctx.obj["path_to_library"] = value
        ctx.obj["graph"] = DependencyGraph().from_library(value)
        return value

    return click.option(
        '--path-to-library', '-p', '-path-to-library',
        callback=callback,
        default='./library',
        envvar='VINERY_PATH_TO_LIBRARY',
        help='Path to the directory with all infrastructure plans.',
        required=True,
        show_default=True,
    )(function)


def option_auto_approve(function: callable):
    return click.option(
        '--auto-approve', '-a', '-auto-approve',
        default=False,
        is_flag=True,
        help="Pass -auto-approve flag to 'RUNNER apply/destroy'."
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
            sys.exit(1)
        
        ctx.ensure_object(dict)
        ctx.obj['runner'] = value
        return value

    return click.option(
        '--runner', '-r', '-runner',
        help='Select the preferred runner for managing infrastructure.',
        default='terraform',
        envvar='VINERY_RUNNER',
        show_default=True,
        callback=callback
    )(function)


def option_recursive(function: callable):
    def callback(ctx, param, value):
        if not value:
            ctx.ensure_object(dict)
            ctx.obj["graph"] = DependencyGraph().from_node(ctx.params.get('plan'))
        return value
    
    return click.option(
        '--recursive', '-rr', '-recursive',
        callback=callback,
        default=True,
        help='Apply the command recursively.',
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
