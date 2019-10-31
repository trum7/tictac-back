from django.http import HttpResponse, JsonResponse
from random import randint
from json import loads
from .models import Game, Round


def new(request, session):
    games = Game.objects.filter(session=session)
    if games.count() != 0:
        return HttpResponse(status=409)
    g = Game(session=session, gamer=1)
    g.save()
    while Game.objects.filter(session=session)[0].gamer == 1:
        pass

    r = Round.objects.filter(game=session)[0]

    round = {'id': r.game, 'invited': r.invited, 'turn': r.turn}

    return JsonResponse(round)


def games(request):
    games = {}
    for g in Game.objects.filter(gamer=1):
        games[g.session] = g.gamer
    return JsonResponse(games)


def join(request, session):
    games = Game.objects.filter(session=session)
    if request.method != 'POST' or games.count() == 0:
        return HttpResponse(status=404)
    elif games[0].gamer == 2:
        return HttpResponse(status=409)
    try:
        json = loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    round = {'id': session, 'invited': json['idGamer']}
    if randint(1, 1000) % 2 == 0:
        turn = round['id']
    else:
        turn = round['invited']
    round['turn'] = turn
    g = games[0]
    r = Round(game=round['id'], invited=round['invited'], turn=round['turn'])
    g.gamer = 2
    r.save()
    g.save()
    return JsonResponse(round)


def wait(request, session):
    rounds = Round.objects.filter(game=session)
    if rounds.count() == 0:
        return HttpResponse(status=404)
    r = rounds[0]
    while r.turn == Round.objects.filter(game=session)[0].turn:
        pass
    r = Round.objects.filter(game=session)[0]
    round = {'id': r.game, 'invited': r.invited, 'turn': r.turn, 'move': r.move}
    return JsonResponse(round)


def play(request, session):
    if request.method != 'POST':
        return HttpResponse(status=404)

    games = Game.objects.filter(session=session)
    rounds = Round.objects.filter(game=session)

    if games.count() == 0:
        return HttpResponse(status=404)
    elif games[0].gamer != 2 or rounds.count() == 0:
        return HttpResponse(status=409)

    try:
        json = loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)
        return HttpResponse(status=400)

    r = rounds[0]
    if r.turn == json['idGamer']:
        r.move = json['move']
        r.turn = json['idOpponent']
        r.save()
    else:
        return HttpResponse(status=401)

    return HttpResponse(status=200)


def delete(request, session):
    games = Game.objects.filter(session=session)
    rounds = Round.objects.filter(game=session)
    if rounds.count() != 0:
        r = rounds[0]
        r.delete()
    if games.count():
        g = games[0]
        g.delete()

    return HttpResponse(status=200)
