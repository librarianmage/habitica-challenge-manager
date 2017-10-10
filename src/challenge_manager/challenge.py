import requests
from challenge_manager.constants import API_BASE, TASK_TYPES
import click


class apiError(Exception):
    def __init__(self, code, name, description, extra=None):
        self.code = code
        self.name = name
        self.description = description
        self.extra = extra


class Challenge():
    '''A Habitica Challenge'''
    def __init__(self, meta, AUTH):
        self.AUTH = AUTH
        meta['group'] = meta['group'].upper()
        challengeRequest = requests.post('{0}/challenges'.format(API_BASE), headers=self.AUTH, data=meta)
        data = challengeRequest.json()

        if data['success'] and challengeRequest.status_code == 201:
            self.id = data['data']['id']
            self.challenge = data['data']
        else:
            raise apiError(challengeRequest.status_code, data['error'], data['message'], meta['group'])

    def _updateSelf(self):
        challengeGet = requests.get('{0}/challenges/{1}'.format(API_BASE, self.id), headers=self.AUTH)
        data = challengeGet.json()

        if data['success'] and challengeGet.status_code == 200:
            self.challenge = data['data']
        else:
            raise apiError(challengeGet.status_code, data['error'], data['message'])

    def setTasksOfType(self, type, tasks):
        self._updateSelf()

        if len(self.challenge['tasksOrder'][type]) > len(tasks):
            for task in self.challenge['tasksOrder'][type][0:len(self.challenge['tasksOrder'][type]) - len(tasks)]:
                deletedTask = requests.delete('{0}/tasks/{1}'.format(API_BASE, task._id), headers=self.AUTH)

                if deletedTask.json()['success'] and deletedTask.status_code == 200:
                    pass
                else:
                    raise apiError(deletedTask.status_code, deletedTask.json()['error'], deletedTask.json()['message'])
        elif len(self.challenge['tasksOrder'][type]) < len(tasks):
            for taskNum in range(len(tasks) - len(self.challenge['tasksOrder'][type])):
                createdTask = requests.post('{0}/tasks/challenge/{1}'.format(API_BASE, self.id), headers=self.AUTH, data={
                    'text': 'Placeholder Task #{0}'.format(taskNum),
                    'type': TASK_TYPES.inv[type]
                })

                if createdTask.json()['success'] and createdTask.status_code == 201:
                    pass
                else:
                    raise apiError(createdTask.status_code, createdTask.json()['error'], createdTask.json()['message'])

        self._updateSelf()

        for taskIndex in range(len(tasks)):
            if 'date' in tasks[taskIndex]:
                tasks[taskIndex]['date'] = tasks[taskIndex]['date'].isoformat()
            elif 'startDate' in tasks[taskIndex]:
                tasks[taskIndex]['startDate'] = tasks[taskIndex]['startDate'].isoformat()

            click.echo('adding task: {0}'.format(tasks[taskIndex]['text']))
            updatedTask = requests.put(
                          '{0}/tasks/{1}'.format(API_BASE, self.challenge['tasksOrder'][type][len(tasks) - 1 - taskIndex]),
                          headers=self.AUTH, data=tasks[taskIndex])

            if updatedTask.json()['success'] and updatedTask.status_code == 200:
                pass
            else:
                raise apiError(updatedTask.status_code, updatedTask.json()['error'], updatedTask.json()['message'])
