"""
Constants for module
"""

from bidict import frozenbidict

API_BASE = 'https://habitica.com/api/v3'
TASK_TYPES = frozenbidict(habit='habits', daily='dailys', todo='todos', reward='rewards')
