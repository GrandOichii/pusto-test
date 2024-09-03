# Решение второй задачи

import csv
import datetime
import random
import io
from django.db import models
from django.core.paginator import Paginator

class Player(models.Model):
    player_id = models.CharField(max_length=100)

    def complete_level(self, level: 'PlayerLevel', score: int):
        if level.player != self:
            raise Exception(f'tried to complete someone elses PlayerLevel {level} (player_id = {self.pk})')
        if level.is_completed:
            raise Exception(f'tried to complete already completed {level}')

        # complete level
        level.is_completed = True
        level.completed = datetime.date.today()
        level.score = score
        level.save()
        
        # receive Level prize
        self.receive_level_prize(level)

    def receive_level_prize(self, level: 'Level'):
        '''Receiving level prize (if any are left)'''
        prizes = LevelPrize.objects.filter(level_id=level.pk, received_by=None)
        prize_count = len(prizes)
        if prize_count == 0:
            # no prize for player :(
            return
        prize = prizes[random.randrange(0, prize_count)]
        prize.received = datetime.date.today()
        prize.received_by = self
        prize.save()
    
    
class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    
    
class Prize(models.Model):
    title = models.CharField(max_length=200) # adding max_length
    
    
class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(null=True, blank=True) # ? should null=True
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def dump_csv() -> str:
        '''Dump PlayerLevel data into .csv format'''
        rows = PlayerLevel.objects.all().order_by('pk')
        paginator = Paginator(rows, 10)
        out = io.StringIO()
        writer = csv.writer(out, lineterminator='\n')
        writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])
        for page_i in paginator.page_range:
            page = paginator.page(page_i)
            for row in page:
                prizes = LevelPrize.objects.filter(received_by=row.player, level=row.level)
                prize_title = prizes[0].prize.title if len(prizes) > 0 else ''
                writer.writerow([row.player.player_id, row.level.title, row.is_completed, prize_title])
        return out.getvalue()


    
class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField(null=True, blank=True) # ? should null=True?
    received_by = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
     
