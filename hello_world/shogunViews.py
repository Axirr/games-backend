from hello_world.models import ShogunGame
from django.http import HttpResponse
from django.http import JsonResponse
import random
from django.core import serializers
from django.core.serializers import serialize

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

def resetGameShogun(request, gameId, numberPlayers):
    game = ShogunGame.objects.get(id=gameId)
    if (numberPlayers == 0):
        numberPlayers = game.maxPlayers
    game.setup(numberPlayers)
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

def resetTestsShogun(request):
    testGameIds = [1, 2, 3, 4, 5, 6, 7, 8]
    numberOfPlayers = [4, 4, 4, 4, 4, 4, 4, 4]
    decksForGames = [
                [
                {'name': 'Omnivore', 'cost': 4, 'type': 'keep', 'ability': "Can score [1][2][3] for 2 points now. Can still use in other combos."},
                {'name': 'Regeneration', 'cost': 4, 'type': 'keep', 'ability': "When you heal, heal one extra damage."},
                {'name': 'Rooting For The Underdog', 'cost': 3, 'type': 'keep', 'ability': "At the end of a turn where you have the fewest points, gain a point."},
            ],[
                {'name': 'National Guard', 'cost': 3, 'type': 'discard', 'ability': "+2[Star] and take 2 damage."},
                {'name': 'Nova Breath', 'cost': 7, 'type': 'keep', 'ability': "Your attacks damage all other players."},
                {'name': 'Nuclear Power Plant', 'cost': 6, 'type': 'discard', 'ability': "+2[Star] and heal 3 damage."},
            ],[
                {'name': 'Friend of Children', 'cost':	3, 'type': 'keep', 'ability':	'When you gain energy, gain an additional energy.'},
                {'name': 'Acid Attack', 'cost':	6, 'type': 'keep', 'ability':	"Deal one extra damage (even when you don't attack)"},
                {'name': 'Alien Metabolism', 'cost':	3, 'type': 'keep', 'ability':	'Buying cards costs you 1 less energy'},
                {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
                {'name': 'Commuter Train', 'cost': 4, 'type': 'discard', 'ability': '+ 2[Star]'},
                {'name': 'Corner Store', 'cost': 3, 'type': 'discard', 'ability': '+ 1[Star]'}
            ],[
                {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
                {'name': 'Commuter Train', 'cost': 4, 'type': 'discard', 'ability': '+ 2[Star]'},
                {'name': 'Corner Store', 'cost': 3, 'type': 'discard', 'ability': '+ 1[Star]'}
            ],[
                {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
                {'name': 'Commuter Train', 'cost': 4, 'type': 'discard', 'ability': '+ 2[Star]'},
                {'name': 'Corner Store', 'cost': 3, 'type': 'discard', 'ability': '+ 1[Star]'},
                {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
                {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
                {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
            ],[
                {'name': 'Evacuation Orders', 'cost': 7, 'type': 'discard', 'ability': 'All other monsters lose 5[Star]'},
                {'name': 'Fire Blast', 'cost': 3, 'type': 'discard', 'ability': 'Deal 2 damage to all other monsters'},
                {'name': 'Giant Brain', 'cost': 5, 'type': 'keep', 'ability': 'Get an extra reroll each turn.'},
            ],[
                {'name': 'Complete Destruction', 'cost': 3, 'type': 'keep', 'ability': 'If you roll [1][2][3][Heart][Attack][Energy] gain 9[Star] in addition to the regular results.'},
                {'name': 'Energy Hoarder', 'cost': 3, 'type': 'keep', 'ability': 'You gain 1[Star] for every 6[Energy] you have at the end of your turn.'},
                {'name': 'Even Bigger', 'cost': 4, 'type': 'keep', 'ability': 'Your maximum [Heart] is increased by 2. Gain 2[Heart] when you get this card.'},
            ],[
                {'name': 'Energy Hoarder', 'cost': 3, 'type': 'keep', 'ability': 'You gain 1[Star] for every 6[Energy] you have at the end of your turn.'},
                {'name': 'Gas Refinery', 'cost': 6, 'type': 'discard', 'ability': "Gain 2[Star] and deal 3 damage to all other monsters."},
                {'name': 'High Altitude Bombing', 'cost': 4, 'type': 'discard', 'ability': "All monsters (including you) take 3 damage."},
            ],
    ]
    for i in range(len(testGameIds)):
        game = ShogunGame.objects.get(id=testGameIds[i])
        response = game.setup(numberOfPlayers[i], decksForGames[i], False)
        game.save()
    return HttpResponse("")

def setDiceShogun(request, gameId, diceCode):
    game = ShogunGame.objects.get(id=gameId)
    response = game.setDice(diceCode)
    game.save()
    return HttpResponse(response)