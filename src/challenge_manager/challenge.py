import click
import requests

from challenge_manager.constants import API_BASE
from challenge_manager.constants import TASK_TYPES
from challenge_manager.constants import URL


class apiError(Exception):
    def __init__(self, url, code, name, description, extra=None):
        self.url = url
        self.code = code
        self.name = name
        self.description = description
        self.extra = extra


class Challenge():
    '''A Habitica Challenge'''
    def __init__(self, meta, AUTH, taskList=None):
        self.headers = AUTH
        challengeRequest = requests.post('{0}/challenges'.format(API_BASE), headers=self.headers, json=meta)
        data = challengeRequest.json()

        if data['success'] and challengeRequest.status_code == 201:
            self.id = data['data']['id']
            self.challenge = data['data']
            self.name = data['data']['name']
            click.echo('{0}: {1}/challenges/{2}'.format(self.name, URL, self.id))
        else:
            raise apiError(challengeRequest.status_code, data['error'], data['message'], meta['group'])

        if taskList is not None:
            for taskType, tasks in taskList.items():
                for task in tasks:
                    task.update({'type': TASK_TYPES.inv[taskType]})
                click.echo('adding {0}'.format(taskType))
                self.addTasks(tasks)

    def _updateSelf(self):
        challengeGet = requests.get('{0}/challenges/{1}'.format(API_BASE, self.id), headers=self.headers)
        data = challengeGet.json()

        if data['success'] and challengeGet.status_code == 200:
            self.challenge = data['data']
        else:
            raise apiError(challengeGet.status_code, data['error'], data['message'])

    def setTasksOfType(self, type, tasks):
        self._updateSelf()

        self.addTasks(tasks)

        self._updateSelf()

        for taskIndex, task in enumerate(tasks):

            click.echo('adding {0}: {1}'.format(TASK_TYPES.inv[type], task['text']))
            updatedTask = requests.put(
                          '{0}/tasks/{1}'.format(API_BASE, self.challenge['tasksOrder'][type][taskIndex]),
                          headers=self.headers, json=task)

            if updatedTask.json()['success'] and updatedTask.status_code == 200:
                pass
            else:
                raise apiError(updatedTask.status_code, updatedTask.json()['error'], updatedTask.json()['message'], task)

    def addTasks(self, tasks):
        self._updateSelf()
        addedTasks = requests.post('{0}/tasks/challenge/{1}'.format(API_BASE, self.id),
                                  headers=self.headers,
                                  json=tasks)
        if addedTasks.json()['success'] and addedTasks.status_code == 201:
            pass
        else:
            raise apiError('{0}/tasks/challenge/{1}'.format(API_BASE, self.id), addedTasks.status_code, addedTasks.json()['error'], addedTasks.json()['message'], tasks)
            