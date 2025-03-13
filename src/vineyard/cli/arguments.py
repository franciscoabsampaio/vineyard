import click


def argument_plan(function: callable):
    help_text = """
    PLAN: apply command to the PLAN dependency tree, including PLAN.
    """

    if function.__doc__:
        function.__doc__ += help_text
    else:
        function.__doc__ = help_text
    
    def callback(ctx, param, value):
        return value.strip("/")
    
    return click.argument('plan', callback=callback)(function)
