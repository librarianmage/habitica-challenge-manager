"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m challenge_manager` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``challenge_manager.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``challenge_manager.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click, re

class HabiticaUUIDParamType(click.ParamType):
  name = "UUID"
  
  def convert(self, value, param, ctx):
    regex = re.compile('[a-zA-Z0-9]{8}-(?:[a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12}')
    try:
      assert regex.fullmatch(value) is not None
      return value
    except AssertionError:
      self.fail('%s is not a valid UUID' % value, param, ctx)

HabiticaUUID = HabiticaUUIDParamType()

@click.group()
@click.option('-u', '--id', 'userID', type=HabiticaUUID, prompt='User ID')
@click.option('-k', '--key', 'apiKey', type=HabiticaUUID, prompt='API Key')
@click.pass_context
def cli(ctx, userID, apiKey):
  ctx.obj = {
    'AUTH': {
      'x-api-user': userID,
      'x-api-key': apiKey
    }
  }

@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def upload(ctx, files):
  click.echo('uploading to user %s' % ctx.obj['AUTH']['x-api-user'])
