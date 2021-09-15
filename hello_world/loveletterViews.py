from hello_world.models import LoveLetterGame
from django.http import HttpResponse
from django.http import JsonResponse
import random
from django.core import serializers
from django.core.serializers import serialize

def createLoveLetterGame(request, numberOfPlayers=4):
    new_entry = LoveLetterGame()
    new_entry.deal(numberOfPlayers)
    new_entry.save()
    # new_entry.save()
    # new_entry = serialize('json', [new_entry, ])
    # print(new_entry)
    # print(new_entry.hands)
    # jsonObject = new_entry.jsonForm()
    return HttpResponse(new_entry.id)
    # new_entry.save()

def loveLetterReturnGameState(request, gameId):
    # data = serializers.serialize("json", RPSGame.objects.all())
    data = LoveLetterGame.objects.filter(id=gameId)
    # print(data[0])
    # returnData = serializers.serialize('json', data)
    data = serializers.serialize("json", data)
    return HttpResponse(data)

def advanceTurnLoveLetter(request, gameId):
    data = LoveLetterGame.objects.get(id=gameId)
    data.advanceTurn()
    data.save()
    data = serializers.serialize("json", [data,])
    return HttpResponse(data)

def dealLoveLetter(request, gameId, numberOfPlayers, deckNumber):
    data = LoveLetterGame.objects.get(id=gameId)
    data.deal(numberOfPlayers, deckNumber)
    print(data)
    data.save()
    data = serializers.serialize("json", [data,])
    return HttpResponse(data)

def playCardLoveLetter(request, gameId, card, playerNumber, target, guardGuess):
    game = LoveLetterGame.objects.get(id=gameId)
    response = game.playCard(card, playerNumber, target, guardGuess)
    # print(game)
    game.save()
    # game = serializers.serialize("json", [game,])
    return HttpResponse(response)

def checkIdLoveLetter(request, gameId):
    data = LoveLetterGame.objects.filter(id=gameId)
    if (len(data) > 0): 
        return HttpResponse("ID GOOD")
    else:
        return HttpResponse("ID BAD")

def resetGameLoveLetter(request, gameId, deckNumber):
    game = LoveLetterGame.objects.get(id=gameId)
    game.resetGame(deckNumber)
    game.save()
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)


def resetTestsLoveLetter(request):
    testGameIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    numberOfPlayers = [4, 4, 4, 4, 4, 4, 4, 3, 4]
    decksForGames = [
            ["guard", "guard","guard","countess","priest","guard","king", "baron", "king", "princess"],
            ["guard", "guard","guard","countess","priest","guard","king", "baron", "priest", "handmaiden"],
            ["guard", "guard","guard","countess","priest","baron","king", "baron", "princess", "prince"],
            ["guard", "guard","guard","countess","priest","princess","king", "baron", "guard", "prince"],
            ["guard", "guard","guard","countess","priest","prince","king", "baron", "guard", "handmaiden"],
            ["princess","prince","king", "baron", "guard", "handmaiden"],
            ["guard", "guard","guard","countess","priest","king","king", "baron", "guard", "countess"],
            ["guard", "guard","guard","countess","priest","prince","prince", "baron", "guard", "countess"],
            ["guard", "guard","guard","countess","priest","baron","prince", "baron", "guard", "baron"],
    ]
    for i in range(len(testGameIds)):
        game = LoveLetterGame.objects.get(id=testGameIds[i])
        response = game.deal(numberOfPlayers[i], decksForGames[i], False)
        game.save()
    return HttpResponse("")