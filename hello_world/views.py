from django.http import HttpResponse
import datetime
from django.http import JsonResponse
import random
from django.core import serializers
from django.core.serializers import serialize

from hello_world.models import RPSGame
from hello_world.models import LoveLetterGame
from hello_world.models import ShogunGame

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
    new_entry.deal(4)
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

def createGameShogun(request):
    new_entry = ShogunGame()
    new_entry.setup(4)
    new_entry.save()
    # new_entry.save()
    # new_entry = serialize('json', [new_entry, ])
    # print(new_entry)
    # print(new_entry.hands)
    # jsonObject = new_entry.jsonForm()
    return HttpResponse(new_entry.id)
    # new_entry.save()

def resetGameShogun(request, gameId):
    game = ShogunGame.objects.get(id=gameId)
    game.setup(4)
    game.save()
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)

def gameStateShogun(request, gameId):
    game = ShogunGame.objects.get(id=gameId)
    game = serializers.serialize("json", [game,])
    return HttpResponse(game)

def rollShogun(request, gameId, playerNumber):
    game = ShogunGame.objects.get(id=gameId)
    response = game.roll(playerNumber)
    game.save()
    return HttpResponse(response)

def checkIdShogun(request, gameId):
    data = ShogunGame.objects.filter(id=gameId)
    if (len(data) > 0): 
        return HttpResponse("ID GOOD")
    else:
        return HttpResponse("ID BAD")

def toggleSaveShogun(request, gameId, saveIndex):
    game = ShogunGame.objects.get(id=gameId)
    response = game.toggleSave(saveIndex)
    game.save()
    return HttpResponse(response)

def resolveRollShogun(request, gameId):
    game = ShogunGame.objects.get(id=gameId)
    response = game.resolveRoll()
    game.save()
    return HttpResponse(response)

def buyShogun(request, gameId, buyNumber):
    game = ShogunGame.objects.get(id=gameId)
    response = game.buy(buyNumber)
    game.save()
    return HttpResponse(response)

def doneYieldingShogun(request, gameId):
    game = ShogunGame.objects.get(id=gameId)
    response = game.doneYielding()
    game.save()
    return HttpResponse(response)

def setMaxHealthShogun(request, gameId, maxHealth):
    game = ShogunGame.objects.get(id=gameId)
    response = game.setMaxHealth(maxHealth)
    game.save()
    return HttpResponse(response)

def setMaxVictoryShogun(request, gameId, maxVictory):
    game = ShogunGame.objects.get(id=gameId)
    response = game.setMaxVictoryPoints(maxVictory)
    game.save()
    return HttpResponse(response)

def yieldEdoShogun(request, gameId, edoString):
    game = ShogunGame.objects.get(id=gameId)
    response = game.yieldEdo(edoString)
    game.save()
    return HttpResponse(response)
    
def clearBuyShogun(request, gameId):
    game = ShogunGame.objects.get(id=gameId)
    response = game.clearBuy()
    game.save()
    return HttpResponse(response)