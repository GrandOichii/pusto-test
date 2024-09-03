from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from task1.models import Player

# Create your views here.
def login(context, id: int) -> HttpResponse:
    try:
        player = Player.objects.get(id=id)
        player.on_login()
        data = serializers.serialize('json', [player])
        return HttpResponse(data)
    except Player.DoesNotExist:
        return HttpResponseNotFound(f'player with id {id} not found')