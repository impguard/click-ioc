import click

from app.commands.registry import register


@click.group()
@click.option('--opt2', nargs=2, type=int)
def cli(opt2):
    print('You passed {} to opt2'.format(opt2))


@cli.command()
@click.option('--english', is_flag=True)
def adios(english):
    if english:
        print('Bye!')
    else:
        print('Adios!')


register(cli)
