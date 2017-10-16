"""
Constants for module
"""

from bidict import frozenbidict

URL = 'https://habitica.com'
API_BASE = URL + '/api/v3'
TASK_TYPES = frozenbidict(habit='habits', daily='dailys', todo='todos', reward='rewards')
