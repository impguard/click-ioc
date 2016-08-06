import click

from app.commands.registry import register


@click.group()
@click.option('--opt1', is_flag=True)
def cli(opt1):
    print('opt1 is {}'.format(opt1))


@cli.command()
def hello():
    print('I say hello there!')


register(cli)
