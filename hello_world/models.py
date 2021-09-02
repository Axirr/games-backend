from django.db import models
from django.core import serializers
from django_mysql.models import ListCharField
from django.db.models import CharField
import copy
import random

class ShogunGame(models.Model):
    dice = ListCharField(
        base_field=CharField(max_length=20),
        size=6,
        max_length=(6 * 21),
        default=["none", "none", "none", "none", "none", "none"]
    )
    notDirectUseSaved = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6*11),
        default=['0','0','0','0','0','0']
    )
    notDirectUsePlayersInGame = ListCharField(
        base_field=models.CharField(max_length=1),
        size=6,
        max_length=(6*2),
        default=['1','2','3','4']
    )
    currentTurn = models.IntegerField(default=1)
    hands = models.JSONField(
        default=dict
    )
    deck = models.JSONField(
        default=dict
    )
    message = ListCharField(
        base_field=CharField(max_length=100),
        size=6,
        max_length=(6 * 101),
        default=["blank message", "blank message", "blank message", "blank message", "blank message", "blank message"]
    )
    doShuffle = models.BooleanField(default=True)
    notDirectUsePoints = ListCharField(
        base_field=models.CharField(max_length=1),
        size=6,
        max_length=(6*2),
        default=['0','0','0','0']
    )
    notDirectUseHealth = ListCharField(
        base_field=models.CharField(max_length=2),
        size=6,
        max_length=(6*3),
        default=['0','0','0','0']
    )
    notDirectUseEnergy = ListCharField(
        base_field=models.CharField(max_length=2),
        size=6,
        max_length=(6*3),
        default=['0','0','0','0']
    )
    edo = models.IntegerField(default=0)
    bayEdo = models.IntegerField(default=0)
    remainingRolls = models.IntegerField(default=3)
    winPoints = models.IntegerField(default=20)
    maxHealth = models.IntegerField(default=10)
    startEnergy = models.IntegerField(default=0)
    withSpoof = models.BooleanField(default=False)
    canBuy = models.BooleanField(default=False)
    canYield = models.BooleanField(default=False)
    buttonPhase = models.IntegerField(default=0)
    maxPlayers = models.IntegerField(default=4)

    # CHANGE FOR PRODUCTION
    startingEnergy = 0
    startingHealth = 10
    playToPoints = 20

    # startingEnergy = 5
    # startingHealth = 5
    # playToPoints = 5
    # END CHANGE FOR PRODUCTION

    cards = [
        {'name': 'Friend of Children', 'cost':	3, 'type': 'keep', 'ability':	'when you gain energy, gain an additional energy.'},
        {'name': 'Acid Attack', 'cost':	6, 'type': 'keep', 'ability':	"Deal one extra damage (even when you don't attack)"},
        {'name': 'Alien Metabolism', 'cost':	3, 'type': 'keep', 'ability':	'Buying cards costs you 1 less energy'},
        {'name': 'Apartment Building', 'cost': 5, 'type': 'discard', 'ability': '+ 3[Star]'},
        {'name': 'Commuter Train', 'cost': 4, 'type': 'discard', 'ability': '+ 2[Star]'},
        {'name': 'Corner Store', 'cost': 3, 'type': 'discard', 'ability': '+ 1[Star]'},
        {'name': 'Complete Destruction', 'cost': 3, 'type': 'keep', 'ability': 'If you roll [1][2][3][Heart][Attack][Energy] gain 9[Star] in addition to the regular results.'},
        {'name': 'Energy Hoarder', 'cost': 3, 'type': 'keep', 'ability': 'You gain 1[Star] for every 6[Energy] you have at the end of your turn.'},
        {'name': 'Even Bigger', 'cost': 4, 'type': 'keep', 'ability': 'Your maximum [Heart] is increased by 2. Gain 2[Heart] when you get self card.'},
        {'name': 'Evacuation Orders', 'cost': 7, 'type': 'discard', 'ability': 'All other monsters lose 5[Star]'},
        {'name': 'Fire Blast', 'cost': 3, 'type': 'discard', 'ability': 'Deal 2 damage to all other monsters'},
        {'name': 'Giant Brain', 'cost': 5, 'type': 'keep', 'ability': 'Get an extra reroll each turn.'},
        {'name': 'Heal', 'cost': 3, 'type': 'discard', 'ability': 'Heal 2 health.'},
        {'name': 'Herbivore', 'cost': 5, 'type': 'keep', 'ability': "Gain 1 point on your turn if you don't attack anyone."},
        {'name': 'Gas Refinery', 'cost': 6, 'type': 'discard', 'ability': "Gain 2[Star] and deal 3 damage to all other monsters."},
        {'name': 'Gourmet', 'cost': 4, 'type': 'keep', 'ability': "When scoring [1][1][1], score 3"},
        {'name': 'High Altitude Bombing', 'cost': 4, 'type': 'discard', 'ability': "All monsters (including you) take 3 damage."},
        {'name': 'Jet Fighters', 'cost': 5, 'type': 'discard', 'ability': "+5[Star] and take 4 damage."},
        {'name': 'National Guard', 'cost': 3, 'type': 'discard', 'ability': "+2[Star] and take 2 damage."},
        {'name': 'Nova Breath', 'cost': 7, 'type': 'keep', 'ability': "Your attacks damage all other players."},
        {'name': 'Nuclear Power Plant', 'cost': 6, 'type': 'discard', 'ability': "+2[Star] and heal 3 damage."},
        {'name': 'Omnivore', 'cost': 4, 'type': 'keep', 'ability': "Can score [1][2][3] for 2 points once per turn. Can still use dice in other combos."},
        {'name': 'Regeneration', 'cost': 4, 'type': 'keep', 'ability': "When you heal, heal one extra damage."},
        {'name': 'Rooting For The Underdog', 'cost': 3, 'type': 'keep', 'ability': "At the end of a turn where you have the fewest points, gain a point."},
        {'name': 'Skyscraper', 'cost': 6, 'type': 'discard', 'ability': "Gain 4[Star]."},
        {'name': 'Spiked Tail', 'cost': 5, 'type': 'keep', 'ability': "When you attack, do 1 additional damage."},
        {'name': 'Solar Powered', 'cost': 2, 'type': 'keep', 'ability': "At the end your turn, if you have 0 energy, gain 1 energy."},
        {'name': 'Tanks', 'cost': 4, 'type': 'discard', 'ability': "+4 Points and take 3 damage."},
        {'name': 'Urbavore', 'cost': 4, 'type': 'keep', 'ability': "Gain 1 extra point when starting a turn in Edo. Deal 1 extra damage when dealing damage from Tokyo."},
        {'name': "We're Only Making It Stronger", 'cost': 3, 'type': 'keep', 'ability': "When you lost 2 health, gain 1 energy."},
        {'name': "Amusement Park", 'cost': 6, 'type': 'discard', 'ability': "+4 Points"},
        {'name': "Army", 'cost': 2, 'type': 'discard', 'ability': "+1 point and take a damage for every card you have."},
        {'name': "Cannibalistic", 'cost': 5, 'type': 'keep', 'ability': "When you deal damage, gain 1 point."},
        {'name': "Reflective Hide", 'cost': 6, 'type': 'keep', 'ability': "If you suffer damage, the monster that dealt it suffers 1 damage."},
        {'name': "Throw A Tanker", 'cost': 4, 'type': 'keep', 'ability': "On a turn you deal 3 or more damage, gain 2 points."},
    ]

    def setup(self, numberPlayers):
        # self.canBuy = False
        # self.canYield = False
        # self.buttonPhase = 0
        newDice = ["none", "none", "none", "none", "none", "none"]
        newSaved = ["0", "0", "0", "0", "0", "0"]
        newHands = []
        newPlayers = []
        newDeck = self.deck
        if (self.doShuffle):
            print("Shuffling")
            print("IMPLEMENT SHUFFLE NOT WORKING")
            newDeck = random.shuffle(newDeck)
        else:
            print("Not shuffling.")
        newPoints = []
        newHealth = []
        newEnergy = []
        for i in range(numberPlayers):
            newPlayers.append(i + 1)
            newHands.append([])
            newPoints.append(0)
            newHealth.append(self.startingHealth)
            newEnergy.append(self.startingEnergy)
        self.dice = newDice
        self.notDirectUseSaved = newSaved
        self.notDirectUsePlayersInGame = list(map(str, newPlayers))
        self.currentTurn = 1
        self.hands = newHands
        self.deck = self.cards
        self.message = ["none", "none", "none", "none", "none", "none"]
        self.doShuffle = True
        self.notDirectUsePoints = list(map(str, newPoints))
        self.notDirectUseHealth = list(map(str, newHealth))
        self.notDirectUseEnergy = list(map(str, newEnergy))
        self.edo = 0
        self.bayEdo = 0
        self.remainingRolls = 3
        self.winPoints = self.playToPoints
        self.maxHealth = self.startingHealth
        self.startEnergy = self.startingEnergy
        self.withSpoof = False
        self.canBuy = False
        self.canYield = False
        self.buttonPhase = 0
        self.maxPlayers = numberPlayers
    
    def getSavedNormal(self):
        return list(map(self.lambdaSaved, self.notDirectUseSaved))
    
    def getPlayersInGameNormal(self):
        return list(map(int, self.notDirectUsePlayersInGame))
    
    # def setPlayersInGameNormal(self, index):
    
    def getEnergyNormal(self):
        return list(map(int, self.notDirectUseEnergy))

    def getHealthNormal(self):
        return list(map(int, self.notDirectUseHealth))
    
    def addEnergy(self, playerNumber, energyToAdd):
        self.notDirectUseEnergy[playerNumber - 1] = str(int(self.notDirectUseEnergy[playerNumber - 1]) + energyToAdd)

    def addHealth(self, playerNumber, healthToAdd):
        self.notDirectUseHealth[playerNumber - 1] = str(int(self.notDirectUseHealth[playerNumber - 1]) + healthToAdd)
    
    def setHealth(self, playerNumber, newHealth):
        self.notDirectUseHealth[playerNumber - 1] = str(newHealth)
    
    def getPointsNormal(self):
        return list(map(int, self.notDirectUsePoints))

    def setPoints(self, playerNumber, newPoints):
        self.notDirectUsePoints[playerNumber - 1] = str(newPoints)
    
    def lambdaSaved(self, savedBool):
        if (savedBool == "0"):
            return False
        else:
            return True
    
    def updateMessage(self, newMessage):
        print(newMessage)
        messageCopy = copy.copy(self.message)
        for i in range(len(messageCopy) - 1):
            messageCopy[i] = messageCopy[i+1]
        messageCopy[len(messageCopy) - 1] = newMessage
        self.message = messageCopy

    def roll(self, playerNumber):
        response = ""
        if (playerNumber != self.currentTurn):
            response = "Not your turn"
            return response
        if (self.buttonPhase != 0):
            response = "Not correct phase for that action."
            return response
        if (self.remainingRolls <= 0):
            response = "No rolls left!"
            return response
        numberOfDice = 6
        newDice = []
        for i in range(numberOfDice):
            if (not self.getSavedNormal()[i]):
                newDice.append(self.getRollResult())
            else:
                newDice.append(self.dice[i])
        print(newDice)
        self.dice = newDice
        self.remainingRolls -= 1
        return response

    def getRollResult(self):
        numberOfDice = 6
        rollNumber = random.choice([0,1,2,3,4,5])
        return(self.getNameForRollNumber(rollNumber))

    def getNameForRollNumber(self, rollNumber):
        rollName = "default"
        if (rollNumber == 0):
            rollName = "claw"
        elif (rollNumber == 1):
                rollName = "energy"
        elif (rollNumber == 2):
            rollName = "heart"
        elif (rollNumber == 3):
            rollName = "1"
        elif (rollNumber == 4):
            rollName = "2"
        elif (rollNumber == 5):
            rollName = "3"
        else:
            print("ERROR, UNIDENTIFIED ROLL")
        return rollName

    def toggleSave(self, diceIndexNumber):
        response = ""
        if (self.buttonPhase != 0):
            response = "Not the rolling phase right now."
            return response
        if (self.dice[diceIndexNumber] == "none"):
            response = "Cannot save an unrolled dice."
            return response
        if (self.notDirectUseSaved[diceIndexNumber] == "0"):
            self.notDirectUseSaved[diceIndexNumber] = "1"
        else:
            self.notDirectUseSaved[diceIndexNumber] = "0"
        print(self.notDirectUseSaved)
        print(diceIndexNumber)
        return response
    
    def pointsForRoll(self):
        pointsToAdd = 0
        count = self.count(self.dice, '1')
        if (self.hasCard(self.currentTurn, "Gourmet")):
            if (count >= 3): pointsToAdd += count 
        else:
            if (count >= 3): pointsToAdd += count - 2
        count = self.count(self.dice, '2')
        if (count >= 3): pointsToAdd += count - 1
        count = self.count(self.dice, '3')
        if (count >= 3): pointsToAdd += count 
        if (self.hasCard(self.currentTurn, "Omnivore")):
            onesCount = self.count(self.dice, '1')
            twosCount = self.count(self.dice, '2')
            threesCount = self.count(self.dice, '3')
            if (onesCount >= 1 and twosCount >= 1 and threesCount >= 1):
                self.updateMessage("Omnivore effect activated.")
                pointsToAdd += 2
        return pointsToAdd
    
    def count(self, myArray, item):
        count = 0
        for i in range(len(myArray)):
            if (myArray[i] == item):
                count += 1
        return count

    def pointsForRoll(self):
        pointsToAdd = 0
        count = self.count(self.dice, '1')
        if (self.hasCard(self.currentTurn, "Gourmet")):
            if (count >= 3):
                pointsToAdd += count 
        else:
            if (count >= 3):
                pointsToAdd += count - 2
        count = self.count(self.dice, '2')
        if (count >= 3):
            pointsToAdd += count - 1
        count = self.count(self.dice, '3')
        if (count >= 3):
            pointsToAdd += count 
        if (self.hasCard(self.currentTurn, "Omnivore")):
            onesCount = self.count(self.dice, '1')
            twosCount = self.count(self.dice, '2')
            threesCount = self.count(self.dice, '3')
            if (onesCount >= 1 and twosCount >= 1 and threesCount >= 1):
                self.updateMessage("Omnivore effect activated.")
                pointsToAdd += 2
        return pointsToAdd

    def hasCard(self, player, cardName):
        playerHand = self.hands[player - 1]
        for i in range(len(playerHand)):
            if (playerHand[i]['name'] == cardName):
                return True
        return False

    def resolveRoll(self):
        response = ""
        if (self.buttonPhase != 0):
            response = "Not the rolling phase right now."
            return response
        if (self.dice[0] == "none"):
            response = "Cannot finish turn without rolling."
            return response
        pointsToAdd = 0
        energyToAdd = 0
        healthToAdd = 0
        damage = 0
        pointsToAdd = self.pointsForRoll()
        count = self.count(self.dice, 'energy')
        energyToAdd += count
        count = self.count(self.dice, 'heart')
        if (not self.inEdo(self.currentTurn)):
            healthToAdd = count
        count = self.count(self.dice, 'claw')
        damage += count
        self.changeEnergy(self.currentTurn, energyToAdd)
        self.changeHealth(self.currentTurn, healthToAdd)
        self.addPoints(self.currentTurn, pointsToAdd)
        self.attack(damage)
        self.checkElim()
        if (damage > 0):
            if (len(self.getPlayersInGameNormal()) <= 4):
                if (self.edo == 0):
                    self.enterEdo(self.currentTurn)
                if (not self.onlyCurrentPlayerInEdo()):
                    self.canYield = True
            else:
                self.alertWindow("Implement yield for double edo")
            # Fix for both and yield
        if (self.hasCard(self.currentTurn, "Complete Destruction")):
            diceFaces = ['claw','heart','energy', '1','2','3']
            diceCounts = diceFaces.map(lambda face : self.count(self.dice, face))
            if (self.count(diceCounts, 1) == 6):
                self.updateMessage("Player " + str(self.currentTurn) + " earns 9 points for COMPLETE DESTRUCTION!")
                self.addPoints(self.currentTurn, 9)
        self.canBuy = True
        if (self.canYield):
            self.buttonPhase = 1
        else:
            self.buttonPhase = 2
        return response

    def changeEnergy(self, player, energyToAdd):
        # if (self.hasCard(player, "Friend of Children")):
        # CHANGED TO ACCOUNT FOR NEGATIVE ENERGY
        if (self.hasCard(player, "Friend of Children") and energyToAdd > 0):
            energyToAdd += 1
        self.updateMessage("Player " + str(player) + " earns " + str(energyToAdd) + " energy.")
        self.addEnergy(player, energyToAdd)

    def inEdo(self, playerNumber):
        if (len(self.getPlayersInGameNormal()) <= 4):
            if (playerNumber != self.edo):
                return False
        else:
            if (playerNumber != self.edo and playerNumber != self.bayEdo):
                return False
        return True
    
    def enterEdo(self, player):
        self.edo = player
        self.updateMessage("Player " + str(self.currentTurn) + " goes into Edo.")
        self.addPoints(player, 1)

    def onlyCurrentPlayerInEdo(self):
        returnValue = (self.edo == self.currentTurn or self.edo == 0) and (self.bayEdo == self.currentTurn or self.bayEdo == 0)
        # print("return value" + returnValue)
        # print(self.edo)
        # print(self.bayEdo)
        return returnValue
        # return (self.edo == self.currentTurn || self.edo == 0) and (self.bayEdo == self.currentTurn || self.bayEdo == 0)

    def changeHealth(self, player, healthToAdd):
        healString = " heals for "
        if (healthToAdd < 0):
            healString = " is damaged for "
        if (abs(healthToAdd) > 0):
            self.updateMessage("Player " + str(player) + healString + str(healthToAdd))
        if (self.hasCard(player, "Regeneration") and healthToAdd > 0):
            self.updateMessage("Regeneration effect activated.")
            healthToAdd += 1
        if (self.hasCard(player, "Even Bigger")):
            self.setHealth(player, min(self.getHealthNormal()[player - 1] + healthToAdd, self.maxHealth + 2))
        else:
            self.setHealth(player, min(self.getHealthNormal()[player - 1] + healthToAdd, self.maxHealth))
        if (self.getHealthNormal()[player - 1] <= 0):
            self.eliminatePlayer(player)
        if (self.hasCard(player, "We're Only Making It Stronger") and healthToAdd <= -2):
            self.updateMessage("We're Only Making It Stronger activated.")
            self.changeEnergy(player, 1)

    def addPoints(self, player, newPoints):
        try:
            pointIndex = self.getPlayersInGameNormal().index(player)
        except ValueError:
            pointIndex = -1
        if (pointIndex == -1):
            print("Can't add points to a dead player.")
            return
        originalPoints = self.getPointsNormal()[player - 1]
        newPointValue = max(self.getPointsNormal()[player - 1] + newPoints,0)
        self.setPoints(player, newPointValue)
        if (newPointValue != originalPoints):
            self.updateMessage("Player " + str(player) + " earns " + str(newPoints) + " points.")
        self.checkPointsWin()
    
    def setMaxHealth(self, maxHealth):
        response = ""
        self.maxHealth = maxHealth
        self.updateMessage("Max Health set to " + str(maxHealth))
        self.resetHealthsToMax()
        return response

    def setMaxVictoryPoints(self, points):
        response = ""
        self.updateMessage("Points to win set to " + str(points))
        self.winPoints = points
        return response
    
    def resetHealthsToMax(self):
        for i in range(len(self.notDirectUseHealth)):
            self.setHealth(i + 1, min(self.getHealthNormal()[i], self.maxHealth))

    def checkPointsWin(self):
        for i in range(len(self.getPlayersInGameNormal())):
            playerToCheck = self.getPlayersInGameNormal()[i]
            if (self.getPointsNormal()[playerToCheck - 1] >= self.winPoints):
                if (self.getHealthNormal()[playerToCheck - 1] > 0):
                    self.updateMessage("Player " + str(playerToCheck) + " wins!")
                break

    def getModifiedCost(self, player, originalCost):
        returnCost = originalCost
        if (self.hasCard(player, "Alien Metabolism")):
            returnCost -= 1
        return returnCost

    def attack(self, damage):
        damageBool = True
        attackString = "Edo"
        if (self.hasCard(self.currentTurn, "Acid Attack")): damage += 1
        if (self.hasCard(self.currentTurn, "Spiked Tail") and damage > 0): damage += 1
        if (self.hasCard(self.currentTurn, "Urbavore") and damage > 0): damage += 1
        if (damage >= 3 and self.hasCard(self.currentTurn, "Throw A Tanker")):
            self.updateMessage("Throw A Tanker activated.")
            self.addPoints(self.currentTurn, 2)
        if (self.inEdo(self.currentTurn)):
            damageBool = False
            attackString = "Outside Edo"
        if (damage > 0):
            self.updateMessage("Player " + str(self.currentTurn) + " deals " + str(damage) + " damage to " + str(attackString) + ".")
            if(self.hasCard(self.currentTurn, "Cannibalistic")):
                self.updateMessage("Cannibalistic activated.")
                self.addPoints(self.currentTurn, 1)
        else:
            if (self.hasCard(self.currentTurn, "Herbivore")):
                self.updateMessage("Herbivore activated!")
                self.addPoints(self.currentTurn, 1)
        playersToDamage = []
        if (self.hasCard(self.currentTurn, "Nova Breath")):
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.getPlayersInGameNormal()[i] != self.currentTurn):
                    playersToDamage.append(self.playersInGame[i])
        else:
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.inEdo(self.getPlayersInGameNormal()[i]) == damageBool):
                    playersToDamage.append(self.getPlayersInGameNormal()[i])
        # }
        print("playersToDamage ", playersToDamage)
        for i in range(len(playersToDamage)):
            self.changeHealth(playersToDamage[i], -damage)
            if (self.hasCard(playersToDamage[i], "Reflective Hide") and damage > 1):
                self.updateMessage("Reflective Hide activated.")
                self.changeHealth(self.currentTurn, -1)

    def checkElim(self):
        playersToElim = []
        for i in range(len(self.getPlayersInGameNormal())):
            playerToCheck = self.getPlayersInGameNormal()[i]
            if (self.getHealthNormal()[playerToCheck - 1] <= 0):
                playersToElim.append(playerToCheck)
        for i in range(len(playersToElim)):
            self.eliminatePlayer(playersToElim[i])
        if (len(self.getPlayersInGameNormal()) == 1):
            self.updateMessage("Player " + self.playersInGame[0] + " wins!")
    
    def buy(self, cardNumber):
        response = ""
        if (self.buttonPhase != 2):
            response = "Not buy phase."
            return response
        if (self.canYield):
            response = "Deal with yield before buying."
            return response
        if (len(self.deck) - 1 < cardNumber):
            response = "Cannot buy card " + (cardNumber + 1) + " because it doesn't exist."
            return response
        if (self.canBuy):
            # if (cardNumber == -1):
            if (cardNumber == 10):
                self.advanceTurn()
                return response
            else:
                boughtCard = self.deck[cardNumber]
                boughtCardModifiedCost = self.getModifiedCost(self.currentTurn, boughtCard['cost'])
                if (boughtCardModifiedCost > self.getEnergyNormal()[self.currentTurn - 1]):
                    response = 'Not enough money to buy.'
                    return response
                else:
                    # self.addEnergy(self.currentTurn - 1, -boughtCardModifiedCost)
                    # CHANGED
                    self.addEnergy(self.currentTurn, -boughtCardModifiedCost)
                    del self.deck[cardNumber]
                    if (boughtCard['type'] == 'discard'):
                        self.discardCardEffect(boughtCard)
                    else:
                        self.hands[self.currentTurn - 1].append(boughtCard)
                        self.keepCardImmediateEffect(boughtCard)
        else:
            response = "Cannot buy until you resolve your roll."
        return response

    def clearBuy(self):
        response = ""
        if (self.buttonPhase != 2):
            response = "Not buy phase."
            return response
        if (self.getEnergyNormal()[self.currentTurn - 1] < 2):
            response = "Not enough money to clear."
            return response
        else:
            self.addEnergy(self.currentTurn, -2)
            # CHANGED IMPLEMENT FIX THIS
            del self.deck[0]
            del self.deck[0]
            del self.deck[0]
        return response

    def yieldEdo(self, location):
        response = ""
        if (self.buttonPhase != 1):
            response = "Not yield phase."
            return response
        if(not self.canYield):
            response = "Can't yield, didn't take damage."
            return response
        else:
            if (self.currentTurn != self.edo and self.currentTurn != self.bayEdo):
                if (location == 'edo'):
                    # Possibly can remove inside checks
                    if (self.edo != self.currentTurn):
                        self.updateMessage("Player " + str(self.edo) + " is yielding Edo.")
                        self.enterEdo(self.currentTurn)
                        # self.edo = self.currentTurn
                    else:
                        response = "Can't yield Edo on own turn"
                elif (location == 'bay'):
                    if (self.bayEdo != self.currentTurn):
                        self.updateMessage("Player " + str(self.bayEdo) + " is yielding Edo Bay.")
                        self.enterBayEdo(self.currentTurn)
                    else:
                        response = "Can't yield Edo on own turn"
            else:
                response = "Can't yield Edo on own turn"
        return response

    def discardCardEffect(self, card):
        self.updateMessage(card['name'] + " activated.")
        if card['name'] == 'Apartment Building':
            self.updateMessage("Player " + self.currentTurn + " earns 3 points from card.")
            self.addPoints(self.currentTurn, 3)
        elif card['name'] == 'Commuter Train':
            self.updateMessage("Player " + self.currentTurn + " earns 2 points from card.")
            self.addPoints(self.currentTurn, 2)
        elif card['name'] == 'Corner Store':
            self.updateMessage("Player " + self.currentTurn + " earns 1 points from card.")
            self.addPoints(self.currentTurn, 1)
        elif card['name'] == 'Evacuation Orders':
            self.updateMessage("All players (other than the active player) lose 5 points.")
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.currentTurn != self.playersInGame[i]):
                    self.addPoints(self.playersInGame[i], -5)
        elif card['name'] == 'Fire Blast':
            self.updateMessage("All players (other than the active player) take 2 damage.")
            playersToFireBlast = []
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.currentTurn != self.playersInGame[i]):
                    playersToFireBlast.append(self.playersInGame[i])
                    # self.changeHealth(self.playersInGame[i], -2)
            for i in range(len(playersToFireBlast)):
                self.changeHealth(playersToFireBlast[i], -2)
        elif card['name'] == 'Heal':
            self.changeHealth(self.currentTurn, 2)
        elif card['name'] == 'Gas Refinery':
            self.updateMessage("All players (other than the active player) take 3 damage.")
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.currentTurn != self.playersInGame[i]):
                    self.changeHealth(self.playersInGame[i], -3)
            self.addPoints(self.currentTurn, 2)
        elif card['name'] == 'High Altitude Bombing':
            for i in range(len(self.getPlayersInGameNormal()), -1, -1):
                self.changeHealth(self.playersInGame[i], -3)
        elif card['name'] == "Jet Fighters":
            self.changeHealth(self.currentTurn, -4)
            self.addPoints(self.currentTurn, 5)
        elif card['name'] == "National Guard":
            self.changeHealth(self.currentTurn, -2)
            self.addPoints(self.currentTurn, 2)
        elif card['name'] == "Nuclear Power Plant":
            self.changeHealth(self.currentTurn, 3)
            self.addPoints(self.currentTurn, 2)
        elif card['name'] == "Skyscraper":
            self.addPoints(self.currentTurn, 4)
        elif card['name'] == "Tanks":
            self.changeHealth(self.currentTurn, -3)
            self.addPoints(self.currentTurn, 4)
        elif card['name'] == "Amusement Park":
            self.addPoints(self.currentTurn, 4)
        elif card['name'] == "Army":
            cardNumber = len(self.hands[self.currentTurn - 1])
            print("Card number" + cardNumber)
            self.changeHealth(self.currentTurn, -cardNumber)
            self.addPoints(self.currentTurn, cardNumber)
        else:
            print("ERROR: Unrecognized card.")
        
    def advanceTurn(self):
        try:
            currentIndex = self.getPlayersInGameNormal().index(self.currentTurn)
        except ValueError:
            currentIndex = -1
        if (currentIndex == -1):
            potentialPlayers = []
            for i in range(1, self.totalNumberOfPlayers):
                player = i + self.currentTurn 
                if (player <= self.totalNumberOfPlayers):
                    potentialPlayers.append(player)
                else:
                    potentialPlayers.append(player % self.totalNumberOfPlayers)
            nextClosestPlayer = self.getPlayersInGameNormal()[0]
            for i in range(len(potentialPlayers)):
                if (self.playersInGame.indexOf(potentialPlayers[i]) != -1):
                    nextClosestPlayer = potentialPlayers[i]
                    break
        else:
            nextClosestPlayer = self.getPlayersInGameNormal()[(currentIndex + 1) % len(self.getPlayersInGameNormal())]
        self.endTurnSelfProcedures()
        self.currentTurn = nextClosestPlayer
        self.endTurnAllProcedures()
        self.startTurnProcedures()

    def endTurnSelfProcedures(self):
        if (self.hasCard(self.currentTurn, "Solar Powered")):
            if (self.energy[self.currentTurn - 1] == 0):
                self.updateMessage("Solar Powered activated.")
                self.addEnergy(self.currentTurn, 1)
        if (self.hasCard(self.currentTurn, "Energy Hoarder") and self.getEnergyNormal()[self.currentTurn - 1] >= 6):
            self.updateMessage("Energy Hoarder activated.")
            energyToAdd = floor(self.getEnergyNormal()[self.currentTurn - 1] / 6)
            self.addEnergy(self.currentTurn, energyToAdd)

    def endTurnAllProcedures(self):
        self.rootingForUnderdog()

    def rootingForUnderdog(self):
        for i in range(len(self.getPlayersInGameNormal())):
            if (self.hasCard(self.getPlayersInGameNormal()[i], "Rooting For The Underdog")):
                underdogPoints = self.getPointsNormal()[self.getPlayersInGameNormal()[i] - 1]
                for j in range(len(self.getPlayersInGameNormal())):
                    if (self.getPlayersInGameNormal()[i] != self.getPlayersInGameNormal()[j]):
                        if (self.getPointsNormal()[self.getPlayersInGameNormal()[j] - 1] <= underdogPoints):
                            break
                    if (j == (len(self.getPlayersInGameNormal()) - 1)):
                        self.updateMessage("Underdog activated.")
                        self.addPoints(self.playersInGame[i], 1)

    def startTurnProcedures(self):
        if (self.inEdo(self.currentTurn)):
            pointsToEarn = 2
            if (self.hasCard(self.currentTurn, "Urbavore")):
                pointsToEarn += 1
            self.updateMessage("Player " + str(self.currentTurn) + " gets " + str(pointsToEarn) + " points for starting in Edo.")
            self.addPoints(self.currentTurn, pointsToEarn)
        self.resetRolls()
        self.buttonPhase = 0
        self.canBuy = False
        self.canYield = False

    def resetRolls(self):
        self.remainingRolls = 3
        if (self.hasCard(self.currentTurn, "Giant Brain")):
            self.remainingRolls += 1
        self.resetDiceState()

    def resetDiceState(self):
        self.notDirectUseSaved = ["0","0","0","0","0","0"]
        self.dice = ['none','none','none','none','none','none']

    def doneYielding(self):
        response = ""
        if (self.buttonPhase != 1):
            response = "Not yield phase."
            return response
        self.canYield = False
        self.buttonPhase = 2
        return response

    def keepCardImmediateEffect(self, card):
        if (card['name'] == 'Even Bigger'):
            self.changeHealth(self.currentTurn, 2)

class RPSGame(models.Model):
    leftHand = models.CharField(max_length=30)
    rightHand = models.CharField(max_length=30)
    win = models.CharField(max_length=30)

    def setLeftHand(self, newLeft):
        self.leftHand = newLeft

    def setRightHand(self, newRight):
        self.rightHand = newRight
    
    def __str__(self):
        return "Left Hand: %s Right Hand: %s Win: %s" % (self.leftHand, self.rightHand, self.win)

    def evaluateWin(self):
        validHands = ["Rock", "Paper", "Scissors"]
        if (self.leftHand not in validHands or self.rightHand not in validHands):
            self.win = "Cannot Evaluate"
            return
        if (self.leftHand == self.rightHand):
            self.win = "Tie"
            return
        if (self.leftHand == "Rock"): 
            if (self.rightHand == "Paper"):
                self.win = "Right Hand"
            if (self.rightHand == "Scissors"):
                self.win = "Left Hand"
        if (self.leftHand == "Paper"): 
            if (self.rightHand == "Rock"):
                self.win = "Left Hand"
            if (self.rightHand == "Scissors"):
                self.win = "Right Hand"
        if (self.leftHand == "Scissors"): 
            if (self.rightHand == "Rock"):
                self.win = "Right Hand"
            if (self.rightHand == "Paper"):
                self.win = "Left Hand"

    def resetGame(self):
        self.leftHand = "None"
        self.rightHand = "None"
        self.win = "None"


class LoveLetterGame(models.Model):
    hands = ListCharField(
        base_field=CharField(max_length=20),
        size=6,
        max_length=(6 * 21),
        default=["none", "none", "none", "none"]
    )
    drawCard = CharField(max_length=30, default="none")
    currentTurn = models.IntegerField(default=1)
    deck = ListCharField(
        base_field=CharField(max_length=20),
        size=16,
        max_length=(16 * 21),
        default=["guard", "guard", "guard", "guard", "guard", "priest", "priest", "baron", "baron", "handmaiden",
        "handmaiden", "prince", "prince", "king", "countess", "princess"]
    )
    playersInGame = ListCharField(
        base_field=models.CharField(max_length=5),
        size=6,
        max_length=(6 * 6),
        default=['1','2','3','4']
    )
    isHandMaiden = ListCharField(
        base_field=models.CharField(max_length=1),
        size=5,
        max_length=(5*2),
        default=['0','0','0','0']
    )
    message = ListCharField(
        base_field=CharField(max_length=100),
        size=6,
        max_length=(6 * 101),
        default=["blank message", "blank message", "blank message", "blank message", "blank message", "blank message"]
    )
    setAsideCard = CharField(max_length=30, default="none")
    isDisplayed = ListCharField(
        base_field=models.CharField(max_length=1),
        size=6,
        max_length=(6*2),
        default=['0','0','0','0', '0', '0']
    )
    useDefaultDeck = models.BooleanField(default=True)
    totalNumberOfPlayers = models.IntegerField(default=4)
    playedCards = ListCharField(
        base_field=CharField(max_length=20),
        size=16,
        max_length=(16 * 21),
        default=[]
    )
    # defaultDeck = ["guard", "guard", "guard", "guard", "guard", "priest", "priest", "baron", "baron", "handmaiden",
    # "handmaiden", "prince", "prince", "king", "countess", "princess"]
    
    def __str__(self):
        return "LoveLetterGame: \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s" % (
            str(self.hands),self.drawCard,self.currentTurn, self.deck, self.playersInGame, self.isHandMaiden, self.message, self.setAsideCard,
            self.isDisplayed, self.useDefaultDeck, self.totalNumberOfPlayers, self.playedCards)

    def jsonForm(self):
        data = serializers.serialize('json', [self, ])
        print(data)
        return data

    def advanceTurn(self):
        intPlayersInGame = list(map(int, self.playersInGame))
        try:
            # print("Current turn is ", self.currentTurn)
            # print("Players in game ", intPlayersInGame)
            currentIndex = intPlayersInGame.index(self.currentTurn)
        except ValueError:
            currentIndex = -1
        if (currentIndex == -1):
            print("Player NOT FOUND way")
            potentialPlayers = []
            for i in range(self.totalNumberOfPlayers):
                player = i + int(self.currentTurn)
                if (player <= self.totalNumberOfPlayers):
                    potentialPlayers.append(player)
                else:
                    potentialPlayers.append(player % self.totalNumberOfPlayers)
            nextClosestPlayer = intPlayersInGame[0]
            for i in range(len(potentialPlayers)):
                try:
                    if (intPlayersInGame.index(potentialPlayers[i]) != -1):
                        nextClosestPlayer = potentialPlayers[i]
                        break
                except ValueError:
                    pass
            self.currentTurn = nextClosestPlayer
        else:
            print("Player found way")
            self.currentTurn = intPlayersInGame[(currentIndex + 1) % len(intPlayersInGame)]

    def deal(self, numberPlayers, deckNumber=0):
        newDeck = []
        doShuffle = True
        if (deckNumber == 0):
            newDeck = ["guard", "guard", "guard", "guard", "guard", "priest", "priest", "baron", "baron", "handmaiden",
        "handmaiden", "prince", "prince", "king", "countess", "princess"]
        else:
            doShuffle = False
            newDeck = self.getDeckForDeckNumber(deckNumber)
        if (doShuffle):
            random.shuffle(newDeck)
        deckCopy = copy.copy(newDeck)
        newHands = []
        isHandMaiden = []
        isDisplayed = ['1', '1']
        playersInGame = []
        for i in range(numberPlayers):
            newHands.append(deckCopy.pop())
            isHandMaiden.append('0')
            isDisplayed.append('1')
            playersInGame.append(i + 1)
        drawCard = deckCopy.pop()
        setAsideCard = deckCopy.pop()
        print("Set aside card: " + setAsideCard)
        self.hands = newHands
        self.drawCard = drawCard
        self.currentTurn = 1
        self.deck = deckCopy
        self.playersInGame = playersInGame
        self.isHandMaiden = isHandMaiden
        self.setAsideCard = setAsideCard
        self.isDisplayed = isDisplayed
        self.totalNumberOfPlayers = numberPlayers
        self.playedCards = []
        self.message = ["blank message","blank message","blank message","blank message","blank message","blank message"]

    def playCard(self, card, playerNumber, target, guardGuess):
        response = ""
        if (playerNumber != self.currentTurn): 
            response = "Not your turn. Current turn is Player " + str(self.currentTurn) + "."
            print(response)
            return response
        self.removeSelfHandmaiden()
        if (self.currentTurn < 0 ):
            response = "Game is over. No valid moves unless you reset the game."
            return response
        if (not self.isValidMove(card, target)):
            response = "Not a valid move"
            return response
        try:
            cardIndex = ["king", "prince", "guard", "priest", "baron"].index(card)
        except ValueError:
            cardIndex = -1
        if (not (cardIndex == -1) and self.isOnlyHandmaidenTargets(card)):
            self.updateMessage("Player " + str(self.currentTurn) + " played a " + card + " but had no valid targets.")
            isDrawCardPlayed = (card == self.drawCard)
            self.normalDrawAndAdvance(isDrawCardPlayed)
        else:
            response = self.cardEffect(card, target, guardGuess)
        return response
    
    def getDeckForDeckNumber(self, deckNumber):
        if (deckNumber == 1):
            deck = ["guard", "guard","guard","countess","priest","guard","king", "baron", "king", "princess"] 
        return deck


    def removeSelfHandmaiden(self):
        handmaidenCopy = copy.copy(self.isHandMaiden)
        handmaidenCopy[self.currentTurn - 1] = "0"
        self.isHandMaiden = handmaidenCopy
    
    def isValidMove(self, card, targetNumber):
        # Countess check
        currentHandCard = self.hands[self.currentTurn - 1]
        if (currentHandCard == "countess" or self.drawCard == "countess"):
            if (card != "countess"):
                if ((currentHandCard == "prince") or (currentHandCard == "king") or (self.drawCard == "prince") or (self.drawCard) == "king"):
                    self.alertWindow("Invalid move. Must play the countess")
                    return False
        # Valid target check
        try:
            cardIndex = ['king', 'guard', 'prince', 'baron', 'priest', 'guard'].index(card)
        except ValueError:
            cardIndex = -1
        if (cardIndex != -1):
            if (not self.isValidTarget(card, targetNumber)):
                return False
        return True
    
    def alertWindow(self, message):
        self.updateMessage(message)

    def isValidTarget(self, card, targetNumber):
        myTarget = targetNumber

        # Check still in game
        try:
            intPlayersInGame = list(map(int, self.playersInGame))
            targetIndex = intPlayersInGame.index(myTarget)
        except ValueError:
            targetIndex = -1
        if (targetIndex == -1):
            self.alertWindow("INVALID MOVE. Target not in game.")
            return False


        # Check if handmaiden
        if (self.isOnlyHandmaidenTargets(card)):
            return True
        elif (self.isHandMaiden[myTarget - 1] == "1"):
        # Check not self unless prince
            try:
                secondCardIndex = ['king', 'guard', 'baron', 'priest', 'guard'].index(card)
            except ValueError:
                secondCardIndex = -1
            if (secondCardIndex != -1):
                if (myTarget == self.currentTurn):
                    self.alertWindow("INVALID MOVE. Cannot target self except with prince.")
                    return False
                elif (len(self.playersInGame) > 2):
                    self.alertWindow("INVALID MOVE. Cannot target handmaiden player.")
                    return False
                elif (card == "prince"):
                    self.alertWindow("INVALID MOVE. Cannot target handmaiden player. Remember, Prince can target self.")
                    return False
        return True
    
    
    def isOnlyHandmaidenTargets(self, card):
        # return False
        onlyHandmaidens = False
        if (card == "prince"):
            return onlyHandmaidens
        intPlayersInGame = list(map(int, self.playersInGame))
        for i in range(len(intPlayersInGame)):
            potentialTarget = intPlayersInGame[i]

            # Found valid target
            if (self.isHandMaiden[potentialTarget - 1] == '0' and potentialTarget != self.currentTurn):
                break

            # Reached end of search, no valid target found
            if (i == (len(intPlayersInGame) - 1)):
                onlyHandmaidens = True
        return onlyHandmaidens
    
    def updateMessage(self, newMessage):
        messageCopy = copy.copy(self.message)
        for i in range(len(messageCopy) - 1):
            messageCopy[i] = messageCopy[i+1]
        messageCopy[len(messageCopy) - 1] = newMessage
        self.message = messageCopy
    
    def normalDrawAndAdvance(self, isDrawCardPlayed): 
        if (not isDrawCardPlayed): 
            self.replaceCard(self.currentTurn)
        else:
            self.replaceCard(0)
        self.advanceTurn()
    
    def resetGame(self, deckNumber): 
        self.deal(self.totalNumberOfPlayers, deckNumber)

    def replaceCard(self, playerNumber):
        self.checkIfGameOver()
        if (len(self.deck) == 0):
            drawnCard = "none"
        else:
            drawnCard = self.deck.pop()
        if (playerNumber == 0):
            self.drawCard = drawnCard
        else:
            copyHands = copy.copy(self.hands)
            copyHands[playerNumber - 1] = self.drawCard
            self.hands = copyHands
            self.drawCard = drawnCard

    def checkIfGameOver(self):
        # splitDeck = self.deck.split(',')
        # print("Length of deck", len(splitDeck))
        if (len(self.deck) == 0):
            self.evaluateShowdownWin()
            return
    
    def evaluateShowdownWin(self):
        self.updateMessage("SHOWDOWN! Players compare card values and highest wins.")
        # self.showAllCards()
        maxPlayer = 0
        maxValue = 0
        isTie = False
        intPlayersInGame = list(map(int, self.playersInGame))
        for i in range(len(intPlayersInGame)):
            currentPlayer = intPlayersInGame[i]
            cardValue = self.getCardValue(self.hands[currentPlayer - 1])
            if (cardValue > maxValue):
                maxPlayer = currentPlayer
                maxValue = cardValue
                isTie = False
            elif (cardValue == maxValue):
                isTie = True
        self.currentTurn = -1
        if (not isTie):
            self.winProcedures(maxPlayer)
        else:
            self.winProcedures(-1)

    def getCardValue(self, card):
        if (card == "princess"):
            return 8
        elif (card == "countess"):
            return 7
        elif (card == "king"):
            return 6
        elif (card == "prince"):
            return 5
        elif (card == "handmaiden"):
            return 4
        elif (card == "baron"):
            return 3
        elif (card == "priest"):
            return 2
        elif (card == "guard"):
            return 1
        else:
            print("ERROR, unidentified card found")
            print(card)
            return 0
    
    def winProcedures(self, player):
        if (player < 0):
            self.updateMessage("Tie!")
        else:
            self.updateMessage("Player " + str(player) + " wins!")
        self.currentTurn = -1
    
    
    def cardEffect(self, card, myTarget, guess):
        response = ""
        self.playedCards.append(card)
        try:
            targetCardIndex = ["guard","priest","baron", "prince", "king"].index(card) 
        except ValueError:
            targetCardIndex = -1
        try:
            handMaidenCardIndex = ["handmaiden"].index(card)
        except ValueError:
            handMaidenCardIndex = -1
        if (targetCardIndex != -1): 
            self.updateMessage("Player " + str(self.currentTurn) + " played a " + card + " targeting Player " + str(myTarget) + ".")
        elif (handMaidenCardIndex != -1):
            self.updateMessage("Player " + str(self.currentTurn) + " played a " + card + ".")
        else:
            self.updateMessage("Player " + str(self.currentTurn) + " played a " + card + " with no direct effect.")
        isDrawCardPlayed = (card == self.drawCard)
        if (isDrawCardPlayed):
            notPlayedCard = self.hands[self.currentTurn - 1]
        else:
            notPlayedCard = self.drawCard
        if (card == 'princess'):
            self.eliminatePlayer(self.currentTurn)
            self.replaceCard(0)
            self.advanceTurn()
        elif (card == 'countess'):
            self.normalDrawAndAdvance(isDrawCardPlayed)
        elif (card == 'king'):
            self.updateMessage("Player " + str(self.currentTurn) + " trades hand with Player " + str(myTarget) + ".")
            handsCopy = copy.copy(self.hands)
            playerOriginalHand = handsCopy[myTarget - 1]
            handsCopy[myTarget - 1] = notPlayedCard
            handsCopy[self.currentTurn - 1] = playerOriginalHand
            self.hands = handsCopy
            if (not isDrawCardPlayed):
                self.replaceCard(0)
                self.advanceTurn()
            else:
                self.replaceCard(0)
                self.advanceTurn()
        elif (card == 'prince'):
            self.updateMessage("Player " + str(myTarget) + " discards their hand.")
            self.updateMessage("Player " + str(myTarget) + " hand card was a " + self.hands[myTarget - 1] + ".")
            deckCopy = copy.copy(self.deck)
            handsCopy = copy.copy(self.hands)
            discardedCard = handsCopy[myTarget - 1]
            if (myTarget == self.currentTurn):
                if (discardedCard == "prince"):
                    discardedCard = self.drawCard
            if (len(deckCopy) >= 1):
                handsCopy[myTarget - 1] = deckCopy.pop()
            else:
                handsCopy[myTarget - 1] = self.setAsideCard
            self.hands = handsCopy
            if (myTarget == self.currentTurn):
                self.replaceCard(0)
                self.advanceTurn()
            else:
                self.replaceCard(self.currentTurn)
                self.advanceTurn()
            if (discardedCard == "princess"):
                self.eliminatePlayer(myTarget)
                self.advanceTurn()
        elif (card == 'handmaiden'):
            self.updateMessage("Player " + str(self.currentTurn) + " is immune until their next turn.")
            handmaidenCopy = copy.copy(self.isHandMaiden)
            handmaidenCopy[self.currentTurn - 1] = '1'
            self.isHandMaiden = handmaidenCopy
            self.normalDrawAndAdvance(isDrawCardPlayed)
        elif (card == 'baron'):
            if (isDrawCardPlayed):
                playerValue = self.getCardValue(self.hands[self.currentTurn - 1])
            else:
                playerValue = self.getCardValue(self.drawCard)
            targetValue = self.getCardValue(self.hands[myTarget - 1])
            playerToEliminate = 0
            message = "Player " + str(myTarget) + " and Player " + str(self.currentTurn) + " tie in baron comparison."
            if (playerValue > targetValue):
                playerToEliminate = myTarget
                message = "Player " + str(self.currentTurn) + " wins against Player " + str(myTarget) + " in baron comparison."
            elif (targetValue > playerValue):
                playerToEliminate = self.currentTurn
                message = "Player " + str(self.currentTurn) + " loses against Player " + str(myTarget) + " in baron comparison."
            self.updateMessage(message)
            if (playerToEliminate != 0):
                self.eliminatePlayer(playerToEliminate)
            if (not isDrawCardPlayed):
                self.replaceCard(self.currentTurn)
            else:
                self.replaceCard(0)
            self.advanceTurn()
        elif (card == 'priest'):
            self.updateMessage("Player " + str(self.currentTurn) + " looks at the hand of Player " + str(myTarget) + ".")
            response = "Player " + str(myTarget) + " has a " + self.hands[myTarget - 1]
            self.normalDrawAndAdvance(isDrawCardPlayed)
        elif (card == 'guard'):
            self.updateMessage("Player " + str(self.currentTurn) + " guessed " + guess + ".")
            actualHand = self.hands[myTarget - 1]
            playerToEliminate = 0
            message = "Guess was wrong."
            if (guess == actualHand):
                message = "Guess was right!"
                playerToEliminate = myTarget
            self.updateMessage(message)
            if (playerToEliminate != 0):
                self.eliminatePlayer(playerToEliminate)
                self.normalDrawAndAdvance(isDrawCardPlayed)
            else:
                self.normalDrawAndAdvance(isDrawCardPlayed)
        else:
            print("CARD NOT FOUND!")
        return response
    
    def eliminatePlayer(self, playerNumber):
        intPlayersInGame = list(map(int, self.playersInGame))
        print("intPlayersInGame ",intPlayersInGame)
        try:
            index = intPlayersInGame.index(playerNumber)
        except ValueError:
            index = -1
        del intPlayersInGame[index]
        # copyPlayers.splice(index, 1)
        print(list(map(str, intPlayersInGame)))
        self.playersInGame = list(map(str, intPlayersInGame))
        self.updateMessage("Player " + str(playerNumber) + " was eliminated.")
        self.updateMessage("Player " + str(playerNumber) + " discarded a " + self.hands[playerNumber - 1] + ".")
        self.playedCards.append(self.hands[playerNumber - 1])
        if (len(intPlayersInGame) == 1):
            self.winProcedures(intPlayersInGame[0])