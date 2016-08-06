""" Provides an inversion of control for a Click CLI. """
import click

from app.commands import registry as subcommands


def handle_options(**options):
    for sc in subcommands:
        options_subset = {p.name: options[p.name] for p in sc.params}
        sc.callback(**options_subset)


params = [param for sc in subcommands for param in sc.params]
cli = click.CommandCollection(sources=subcommands, params=params, callback=handle_options)
