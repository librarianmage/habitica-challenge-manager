"""
Module that contains the command line app.
"""
import click
from strictyaml import load

from challenge_manager.challenge import Challenge
from challenge_manager.challengeSchema import challengeSchema


@click.group()
@click.option('-u', '--id', 'userID', type=click.UUID, prompt='User ID')
@click.option('-k', '--key', 'apiKey', type=click.UUID, prompt='API Key')
@click.pass_context
def cli(ctx, userID, apiKey):
    ctx.obj = {
        'AUTH': {
            'x-api-user': str(userID),
            'x-api-key': str(apiKey)
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
    challengeData['challenge']['group'] = str(challengeData['challenge']['group'])

    # create challenge
    click.echo('creating challenge...')
    challenge = Challenge(challengeData['challenge'], ctx.obj['AUTH'])
    click.echo('done')

    # create tasks
    for taskType, tasks in challengeData['tasks'].items():
        click.echo('adding {0}...'.format(taskType))
        challenge.setTasksOfType(taskType, tasks)
        click.echo('done')
