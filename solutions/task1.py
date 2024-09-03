# Решение первой задачи

import datetime
import time
from django.db import models

POINTS_PER_LOGIN = 10

class Player(models.Model):
    '''Player model'''
    first_login_time = models.DateTimeField(null=True, default=None, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'player {self.pk}'

    def _set_login_time(self):
        '''Set the first login time of the player, if not yet set'''
        if self.first_login_time is None:
            self.first_login_time = datetime.datetime.now()
            self.save()

    def _add_login_points(self):
        '''Add points for logging in'''
        self.points += POINTS_PER_LOGIN
        self.save()

    login_events = [
        _set_login_time,
        _add_login_points,
    ]
    '''List of actions to be performed after player login'''

    def on_login(self):
        '''Perform on-login actions'''
        for event in self.login_events:
            event(self)

    def add_boost(self, boost_type):
        '''Add a boost of a certain type to the player'''
        boost = Boost()
        boost.b_type = boost_type
        boost.player = self
        boost.save()

    def on_completed_level(self):
        '''Perform actions after completing a level'''
        self.add_boost('lvl_complete')

class Boost(models.Model):
    '''Player boost model'''
    b_type = models.CharField(max_length=20, default='')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'boost \"{self.b_type}" {self.pk}'