from hello_world.models import DeepSeaGame
from django.http import HttpResponse
from django.http import JsonResponse
import random
from django.core import serializers
from django.core.serializers import serialize

def createGameDeepSea(request):
    new_entry = DeepSeaGame()
    new_entry.setup(4)
    new_entry.save()
    return HttpResponse(new_entry.id)

def resetGameDeepSea(request, gameId, numberPlayers):
    game = DeepSeaGame.objects.get(id=gameId)
    if (numberPlayers == 0):
        numberPlayers = game.maxPlayers
    game.setup(numberPlayers)
    game.save()
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)

def gameStateDeepSea(request, gameId):
    game = DeepSeaGame.objects.get(id=gameId)
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)

def checkIdDeepSea(request, gameId):
    data = DeepSeaGame.objects.filter(id=gameId)
    if (len(data) > 0): 
        return HttpResponse("ID GOOD")
    else:
        return HttpResponse("ID BAD")

def changeDirectionDeepSea(request, gameId, playerNumber, isChangingDirection):
    game = DeepSeaGame.objects.get(id=gameId)
    isChangingDirectionBool = False
    if (isChangingDirection == 1):
        isChangingDirectionBool = True
    response = game.changeDirection(playerNumber, isChangingDirectionBool)
    game.save()
    return HttpResponse(response)

def rollDeepSea(request, gameId):
    game = DeepSeaGame.objects.get(id=gameId)
    response = game.roll()
    game.save()
    return HttpResponse(response)

def takeTreasureDeepSea(request, gameId):
    game = DeepSeaGame.objects.get(id=gameId)
    response = game.takeTreasure()
    game.save()
    return HttpResponse(response)

def advanceTurnDeepSea(request, gameId):
    game = DeepSeaGame.objects.get(id=gameId)
    response = game.advanceTurn()
    game.save()
    return HttpResponse(response)

def dropTreasureDeepSea(request, gameId):
    game = DeepSeaGame.objects.get(id=gameId)
    response = game.dropTreasure()
    game.save()
    return HttpResponse(response)

def spoofDiceDeepSea(request, gameId, diceValue):
    diceArray = [0,0]
    if (diceValue == 2):
        diceArray = [1,1]
    elif (diceValue == 3):
        diceArray = [1,2]
    elif (diceValue == 4):
        diceArray = [2,2]
    elif (diceValue == 5):
        diceArray = [2,3]
    elif (diceValue == 6):
        diceArray = [3,3]
    else:
        return HttpResponse("Spoofed dice value not correct.")
    game = DeepSeaGame.objects.get(id=gameId)
    game.setDice(diceArray)
    response = game.roll(withRoll=False)
    game.save()
    return HttpResponse(response)

def resetTestsDeepSea(request):
    testGameIds = [1]
    numberOfPlayers = [4]
    for i in range(len(testGameIds)):
        game = DeepSeaGame.objects.get(id=testGameIds[i])
        response = game.setup(numberOfPlayers[i])
        game.save()
    return HttpResponse("")

def setMaxOxygenDeepSea(request, gameId, maxOxygen):
    game = DeepSeaGame.objects.get(id=gameId)
    response = game.setMaxOxygen(maxOxygen)
    game.save()
    return HttpResponse(response)
    
def setMaxRoundsDeepSea(request, gameId, maxRounds):
    game = DeepSeaGame.objects.get(id=gameId)
    response = game.setMaxRemainingRounds(maxRounds)
    game.save()
    return HttpResponse(response)