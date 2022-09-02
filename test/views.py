from django.http import HttpResponse
from django.shortcuts import render
from test.models import Player

def hello(request):
    players = Player.objects.all()
    return render(request,
        'test/hello.html',
        {'players': players})


