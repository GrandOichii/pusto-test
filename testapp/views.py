from django.core import serializers
from django.http import HttpResponse
import json
from django.shortcuts import render

from .models import TodoTask

# Create your views here.

def all(context) -> HttpResponse:
    values = TodoTask.objects.all()
    data = serializers.serialize('json', values)
    return HttpResponse(data)