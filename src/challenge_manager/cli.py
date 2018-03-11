"""
Module that contains the command line app.
"""
import click, requests, json
from strictyaml import load, YAMLValidationError
from ruamel.yaml import YAML

from challenge_manager.challenge import Challenge
from challenge_manager.challengeSchema import challengeSchema, challengeSchemaList
from challenge_manager.constants import URL, API_BASE


@click.group()
@click.option('-u', '--id', 'userID', type=click.UUID, prompt='User ID')
@click.option('-k', '--key', 'apiKey', type=click.UUID, prompt='API Key', hide_input=True)
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
    challengesToUpload = []

    for file in files:
        with open(file) as yamlData:
            data = yamlData.read()
            try:
                challengeYaml = load(data, challengeSchema)
                challengeData = challengeYaml.data
                challengeData['challenge']['group'] = challengeData['challenge']['group'].lower() if challengeData['challenge']['group'] != '00000000-0000-4000-a000-000000000000' else '00000000-0000-4000-A000-000000000000'
                challengesToUpload.append(challengeData)
            except YAMLValidationError:
                challengesYaml = load(data, challengeSchemaList)
                challengesData = challengesYaml.data
                for i in range(len(challengesData)):
                    challengesData[i]['challenge']['group'] = challengesData[i]['challenge']['group'].lower() if challengesData[i]['challenge']['group'] != '00000000-0000-4000-a000-000000000000' else '00000000-0000-4000-A000-000000000000'
                challengesToUpload.extend(challengesData)

    for challengeData in challengesToUpload:
        challenge = Challenge(challengeData['challenge'], ctx.obj['AUTH'], challengeData['tasks'])


@cli.command()
@click.argument('id', type=click.UUID)
@click.pass_context
def download(ctx, id):
    challengeRequest = requests.get('{0}/challenges/{1}'.format(API_BASE, id), headers=ctx.obj['AUTH'])
    data = challengeRequest.json()

    if data['success'] and challengeRequest.status_code == 200:
         click.echo(json.dumps(data['data']))
    else:
        raise apiError(challengeGet.status_code, data['error'], data['message'])