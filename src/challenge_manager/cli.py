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
import click, re, requests
from strictyaml import load, Map, MapPattern, Int, Float, Str, Regex, Enum, Bool, Seq, Optional, Datetime, YAMLValidationError
from datetime import datetime

UUID_REGEX = '[a-zA-Z0-9]{8}-(?:[a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12}'
API_BASE = 'https://habitica.com/api/v3/'

task_schema = {
  "text": Str(),
  Optional("alias"): Str(),
  Optional("attribute"): Enum(["str", "int", "per", "con"]),
  Optional("notes"): Str(),
  Optional("priority"): Float()
}

todo_schema = task_schema.copy()
todo_schema.update({
  Optional("date"): Datetime()
})

daily_schema = task_schema.copy()
daily_schema.update({
  Optional("frequency"): Enum(["daily", "weekly", "montly", "yearly"]),
  Optional("repeat"): MapPattern(Str(), Bool()),
  Optional("everyX"): Int(),
  Optional("startDate"): Datetime()
})

habit_schema = task_schema.copy()
habit_schema.update({
  Optional("up"): Bool(),
  Optional("down"): Bool()
})

reward_schema = task_schema.copy()
reward_schema.update({
  Optional("value"): Float()
})

challenge_schema = Map({
  "challenge": Map({
    "group": Regex(UUID_REGEX),
    "name": Str(),
    "shortName": Str(),
    Optional("summary"): Str(),
    Optional("description"): Str(),
    Optional("prize"): Int()
  }),
  Optional("tasks"): Map({
    Optional("habit"): Seq(Map(habit_schema)),
    Optional("daily"): Seq(Map(daily_schema)),
    Optional("todo"): Seq(Map(todo_schema)),
    Optional("reward"): Seq(Map(reward_schema))
  })
})

class HabiticaUUIDParamType(click.ParamType):
  name = "UUID"
  
  def convert(self, value, param, ctx):
    regex = re.compile(UUID_REGEX)
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
  with open(files[0]) as yamlData:
    data = yamlData.read()
  challengeYaml = load(data, challenge_schema)
  challengeData = challengeYaml.data
  
  # create challenge 
  challengeInfo = challengeData['challenge']
  createdChallenge = requests.post(API_BASE + 'challenges', headers=ctx.obj['AUTH'], data=challengeInfo)
  challenge = createdChallenge.json()
  
  # create tasks
  for taskType, tasks in challengeData['tasks'].items():
    for task in tasks:
      click.echo('%(taskType)s: %(task)s' % {
        'taskType': taskType,
        'task': task['text']
      })