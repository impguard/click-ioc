import click


ROOT_PARAMS=[
    click.Option('--debug/--no-debug')
    click.Option('--verbose', is_flag=True)]

def root_params(debug, verbose):
    if debug:
        print('I am debugging!')
    if verbose:
        print(''


@click.group()
@click.argument('text')
def echo(text):
    print(text)


