#!/usr/bin/python3

"""
    Python script that, using this REST API, for a given employee ID,
    returns information about his/her TODO list progress.
"""

import requests
from sys import argv


if __name__ == "__main__":
    user_id = argv[1]
    url = 'https://jsonplaceholder.typicode.com/'
    user = requests.get(url + 'users/{}'.format(user_id)).json()
    todo = requests.get(url + 'todos', params={'userId': user_id}).json()
    completed_tasks = [task for task in todo if task.get('completed') is True]

    print('Employee {} is done with tasks({}/{}):'.format(
        user.get('name'), len(completed_tasks), len(todo)))

    for task in completed_tasks:
        print('\t {}'.format(task.get('title')))
