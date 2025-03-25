import click
from vinery.io import echo


def argument_plan(function: callable):
    help_text = """
    PLAN: apply command to the PLAN dependency tree, including PLAN.
    Can take multiple plans as arguments.
    """

    if function.__doc__:
        function.__doc__ += help_text
    else:
        function.__doc__ = help_text
    
    def callback(ctx, param, value):
        if value == ():
            echo("At least ONE plan is required.", log_level="ERROR")
            ctx.exit(1)
        
        echo(f"Plans provided: {value}", log_level="DEBUG")
        ctx.ensure_object(dict)
        ctx.obj['plan'] = value

        return [plan.strip("/") for plan in value]
    
    return click.argument(
        'plan',
        callback=callback,
        nargs=-1  # Variadic argument
    )(function)
