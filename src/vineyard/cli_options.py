import click
from typing import Literal
from vineyard.cli_arguments import argument_plan
from vineyard.io import echo


def option_env(function: callable):
    return click.option(
        '--env', '-e', '-env',
        help='Environment name.',
        required=True
    )(function)


def option_path_to_library(function: callable):
    return click.option(
        '--path-to-library', '-p', '-path-to-library',
        help='Path to the directory with all infrastructure plans.',
        default='./library',
        show_default=True,
    )(function)


def option_runner(function: callable):
    """
    Automatically checks if the runner is installed.
    """
    from vineyard.tf import load_runners

    def callback(ctx, param, value: Literal["tofu", "terraform"]):
        runners_available = load_runners()
        if value not in runners_available:
            echo(f"Runner '{value}' is not installed.", log_level="ERROR")
        return value

    return click.option(
        '--runner', '-r', '-runner',
        help='Select the preferred runner for managing infrastructure.',
        default='tofu',
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


def options_tf(function: callable):
    function = option_recursive(function)
    function = option_runner(function)
    function = option_path_to_library(function)
    function = argument_plan(function)

    return function
