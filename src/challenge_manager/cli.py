"""
Module that contains the command line app.
"""
import click
import requests
from strictyaml import load
from challenge_manager.challengeSchema import challengeSchema

UUID_REGEX = '[a-zA-Z0-9]{8}-(?:[a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12}'
API_BASE = 'https://habitica.com/api/v3/'


@click.group()
@click.option('-u', '--id', 'userID', type=click.UUID, prompt='User ID')
@click.option('-k', '--key', 'apiKey', type=click.UUID, prompt='API Key')
@click.pass_context
def cli(ctx, userID, apiKey):
    ctx.obj = {
        'AUTH': {
            'x-api-user': str(userID),
            'x-api-key': str(urn)
        }
    }


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def upload(ctx, files):
    with open(files[0]) as yamlData:
        data = yamlData.read()
    challengeYaml = load(data, challengeSchema)
    challengeData = challengeYaml.data

    # create challenge
    challengeInfo = challengeData['challenge']
    createdChallenge = requests.post(API_BASE + 'challenges', headers=ctx.obj['AUTH'], data=challengeInfo)
    challenge = createdChallenge.json()
    click.echo(str(challenge))

    # create tasks
    for taskType, tasks in challengeData['tasks'].items():
        for task in tasks:
            click.echo('%(taskType)s: %(task)s' % {
                'taskType': taskType,
                'task': task['text']
            })
