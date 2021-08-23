from django.http import HttpResponse
import datetime
from django.http import JsonResponse
import random
from hello_world.models import RPSGame
from django.core import serializers

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