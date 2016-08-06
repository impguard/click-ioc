"""Provides an inversion of control for a Click CLI.

Discovers other commands and parameters and creates a wrapper cli click group
that will wrap everything found in this way.

This implementation inspects each python module in this directory (besides this
one and __init__.py). Each python module that has a function of the same name
will be added to the wrapper command and each module with a ROOT_PARAMS list of
Click options will be added as global root parameters.

Dynamically discovers these commands and params and loads them at runtime.
"""
import click
from importlib import import_module
from glob import glob
from os.path import dirname, basename, join, isfile
from collections import namedtuple


def get_modules():
    """ Get all the modules in this directory.

    Excludes __init__.py and cli.py when searching for modules. Returns a list
    of Module tuples that store the module instance and the module name.
    """
    Module = namedtuple('Module', ['name', 'instance'])
    exclude_files = {'__init__.py', 'cli.py'}
    full_path = lambda name: "app." + name

    filepaths = glob(join(dirname(__file__), '*.py'))

    modules = []
    for path in filepaths:
        if not isfile(f) or basename(f) in exclude_files:
            continue

        filename = basename(f)[:-3]
        instance = import_module(full_path(filename))
        modules.append(Module(filename, module))

    return modules


def get_commands_params(modules):
    """ Given a list of modules, get the Click commands and params. """
    ROOT_PARAMS_KEY = 'ROOT_PARAMS'

    params = []
    commands = {}
    for module in modules:
        if hasattr(module.instance, ROOT_PARAMS_KEY):
            params += getattr(module.instance, ROOT_PARAMS_KEY)

        if hasattr(module.instance, module.name):
            command = getattr(module.instance, module.name)
            commands[command.name] = command

    return commands, params


commands, params = get_commands_params()
cli = click.Group(commands=commands, params=params)
