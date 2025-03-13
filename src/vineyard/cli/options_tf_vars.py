import click
import os


TF_VARS = {
    'region': 'Cloud region where the infrastructure will be deployed.',
}
OPTIONS_TF_VARS = {}


for name, description in TF_VARS.items():
    def _option_tf_var(function: callable):
        def callback(ctx, param, value):
            os.environ[f"TF_VAR_{name.upper()}"] = value
            return value
        
        return click.option(
            f'--{name}', f'-{name[0]}', f'-{name}',
            help=description,
            callback=callback,
            envvar=f"TF_VAR_{name.upper()}",
            required=True
        )(function)
    
    OPTIONS_TF_VARS[name] = _option_tf_var


def option_workspace(function: callable):
    def callback(ctx, param, value):
        os.environ["TF_VAR_workspace"] = value
        manage_workspace()
        return value

    return click.option(
        '--workspace', '-w', '-workspace',
        default='default',
        callback=callback,
        envvar="TF_VAR_workspace",
        help="The current workspace against which all plans are evaluated/executed.",
        required=True,
        show_default=True,
    )(function)


def options_tf_vars(function: callable):
    for option in OPTIONS_TF_VARS:
        function = option(function)

    function = option_workspace(function)
    return function
