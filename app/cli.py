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


Module = namedtuple('Module', ['name', 'instance'])
ROOT_PARAMS_KEY = 'ROOT_PARAMS'


def full_name(name):
    """ Produces the full name of a package in this directory. """
    return "dockerdb.cli." + name


def get_modules():
    """ Get all the modules in this directory. """
    module_filepaths = glob(join(dirname(__file__), '*.py'))
    module_names = [basename(f)[:-3] for f in module_filepaths
                                     if isfile(f)
                                     if basename(f) != '__init__.py']
    modules = [Module(name, import_module(full_name(name))) for name in module_names]

    return modules


def get_commands_params():
    """Get the various commands and params exposed by other modules in this directory."""
    modules = get_modules()
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
