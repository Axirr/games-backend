from django.http import HttpResponse
import datetime
from django.http import JsonResponse
import random
from hello_world.models import RPSGame
from hello_world.models import LoveLetterGame
from django.core import serializers
from django.core.serializers import serialize

def returnGameState(request, gameId):
    # data = serializers.serialize("json", RPSGame.objects.all())
    data = RPSGame.objects.filter(id=gameId)
    print(data[0])
    # returnData = serializers.serialize('json', data)
    data = serializers.serialize("json", RPSGame.objects.filter(id=gameId))
    return HttpResponse(data)

def setLeft(request, gameId, handCode):
    data = RPSGame.objects.filter(id=gameId)
    data = data[0]
    if (handCode == 1):
        data.setLeftHand("Rock")
    elif (handCode == 2):
        data.setLeftHand("Paper")
    elif (handCode == 3):
        data.setLeftHand("Scissors")
    print(data)
    data.save()
    return HttpResponse("")

def setRight(request, gameId, handCode):
    # VALIDATE GAME ID
    data = RPSGame.objects.filter(id=gameId)
    data = data[0]
    if (handCode == 1):
        data.setRightHand("Rock")
    elif (handCode == 2):
        data.setRightHand("Paper")
    elif (handCode == 3):
        data.setRightHand("Scissors")
    print(data)
    data.save()
    return HttpResponse("")

def evaluate(request, gameId):
    data = RPSGame.objects.filter(id=gameId)
    data = data[0]
    data.evaluateWin()
    data.save()
    return HttpResponse(data.win)

def reset(request, gameId):
    data = RPSGame.objects.filter(id=gameId)
    data = data[0]
    data.resetGame()
    data.save()
    return HttpResponse("")

def checkId(request, gameId):
    data = RPSGame.objects.filter(id=gameId)
    if (len(data) > 0): 
        return HttpResponse("ID GOOD")
    else:
        return HttpResponse("ID BAD")

def createGame(request):
    new_entry = RPSGame(leftHand="None", rightHand="None", win="None")
    new_entry.save()
    return HttpResponse(new_entry.id)

def index(request):
    return HttpResponse("")

def createLoveLetterGame(request):
    new_entry = LoveLetterGame()
    new_entry.save()
    # new_entry.save()
    # new_entry = serialize('json', [new_entry, ])
    # print(new_entry)
    # print(new_entry.hands)
    # jsonObject = new_entry.jsonForm()
    return HttpResponse("")
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

def dealLoveLetter(request, gameId, numberOfPlayers):
    data = LoveLetterGame.objects.get(id=gameId)
    data.deal(numberOfPlayers)
    print(data)
    data.save()
    data = serializers.serialize("json", [data,])
    return HttpResponse(data)

def playCardLoveLetter(request, gameId, card, playerNumber, target, guardGuess):
    game = LoveLetterGame.objects.get(id=gameId)
    game.playCard(card, playerNumber, target, guardGuess)
    # print(game)
    game.save()
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)

def checkIdLoveLetter(request, gameId):
    data = LoveLetterGame.objects.filter(id=gameId)
    if (len(data) > 0): 
        return HttpResponse("ID GOOD")
    else:
        return HttpResponse("ID BAD")

def resetGameLoveLetter(request, gameId):
    game = LoveLetterGame.objects.get(id=gameId)
    game.resetGame()
    game.save()
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)