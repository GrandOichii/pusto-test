from django.contrib import admin

from task2.models import Level, LevelPrize, Player, PlayerLevel, Prize

# Register your models here.
admin.site.register(Player)
admin.site.register(Level)
admin.site.register(Prize)
admin.site.register(PlayerLevel)
admin.site.register(LevelPrize)