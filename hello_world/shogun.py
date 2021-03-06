from django.db import models
from django.core import serializers
from django_mysql.models import ListCharField
from django.db.models import CharField
import copy
import random
import math

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
    isGameOver = models.BooleanField(default=False)

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

    def setup(self, numberPlayers, deck=None, isShuffle=True):
        newDice = ["none", "none", "none", "none", "none", "none"]
        newSaved = ["0", "0", "0", "0", "0", "0"]
        newHands = []
        newPlayers = []
        if (deck):
            newDeck = deck
        else:
            newDeck = self.cards
        if (isShuffle):
            print("Shuffling")
            random.shuffle(newDeck)
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
        self.deck = newDeck
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
        self.isGameOver = False
    
    def getSavedNormal(self):
        return list(map(self.lambdaSaved, self.notDirectUseSaved))
    
    def getPlayersInGameNormal(self):
        return list(map(int, self.notDirectUsePlayersInGame))
    
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
    
    # BUG was implemented twice, not sure which is the right one
    # def pointsForRoll(self):
    #     pointsToAdd = 0
    #     count = self.count(self.dice, '1')
    #     if (self.hasCard(self.currentTurn, "Gourmet")):
    #         if (count >= 3): pointsToAdd += count 
    #     else:
    #         if (count >= 3): pointsToAdd += count - 2
    #     count = self.count(self.dice, '2')
    #     if (count >= 3): pointsToAdd += count - 1
    #     count = self.count(self.dice, '3')
    #     if (count >= 3): pointsToAdd += count 
    #     if (self.hasCard(self.currentTurn, "Omnivore")):
    #         onesCount = self.count(self.dice, '1')
    #         twosCount = self.count(self.dice, '2')
    #         threesCount = self.count(self.dice, '3')
    #         if (onesCount >= 1 and twosCount >= 1 and threesCount >= 1):
    #             self.updateMessage("Omnivore effect activated.")
    #             pointsToAdd += 2
    #     return pointsToAdd

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
    
    def count(self, myArray, item):
        count = 0
        for i in range(len(myArray)):
            if (myArray[i] == item):
                count += 1
        return count

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
                print("IMPLEMENT yield for double Edo")
            # FIX IMPLEMENT for both and yield
        if (self.hasCard(self.currentTurn, "Complete Destruction")):
            diceFaces = ['claw','heart','energy', '1','2','3']
            diceCounts = list(map(lambda face : self.count(self.dice, face), diceFaces))
            if (self.count(diceCounts, 1) == 6):
                self.updateMessage("Player " + str(self.currentTurn) + " earns 9 points for COMPLETE DESTRUCTION!")
                self.addPoints(self.currentTurn, 9)
        self.canBuy = True
        if (self.canYield):
            self.buttonPhase = 1
        else:
            self.buttonPhase = 2
        return response
    
    def setDice(self, diceCode):
        response = ""
        diceArray = []
        if (diceCode == "333"):
            diceArray = ["3","3","3","1","2","2"]
        elif (diceCode == "oneClaw"):
            diceArray = ["claw","3","3","1","2","2"]
        elif (diceCode == "nothing"):
            diceArray = ["1","1","2","2","3","3"]
        elif (diceCode == "sixClaw"):
            diceArray = ["claw","claw","claw","claw","claw","claw"]
        elif (diceCode == "oneHeart"):
            diceArray = ["heart","1","1","2","2","3"]
        elif (diceCode == "sixEnergy"):
            diceArray = ["energy","energy","energy","energy","energy","energy"]
        elif (diceCode == "completeDestruction"):
            diceArray = ["energy","claw","heart","1","2","3"]
        elif (diceCode == "threeEnergyThreePoints"):
            diceArray = ["energy","energy","energy","3","3","3"]
        elif (diceCode == "twoEnergy"):
            diceArray = ["energy","energy","1","1","3","3"]
        elif (diceCode == "fiveEnergyOneClaw"):
            diceArray = ["energy","energy","energy","energy","energy","claw"]
        elif (diceCode == "twoClaw"):
            diceArray = ["claw","claw","1","1","2","2"]
        else:
            response = "DICE CODE NOT FOUND, DICE NOT SET SERVER"
            return response
        self.dice = diceArray
        return response

    def changeEnergy(self, player, energyToAdd):
        if (self.hasCard(player, "Friend of Children") and energyToAdd > 0):
            energyToAdd += 1
        if (energyToAdd != 0):
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
        return returnValue

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
    
    def eliminatePlayer(self, player):
        try:
            playerIndex = self.getPlayersInGameNormal().index(player)
        except ValueError:
            playerIndex = -1
        del self.notDirectUsePlayersInGame[playerIndex]
        if (self.inEdo(player)):
            self.removeFromEdo(player)
        self.updateMessage("Player " + str(player) + " is eliminated!")
        if (len(self.getPlayersInGameNormal()) == 1):
            self.winProcedures(self.getPlayersInGameNormal()[0])

    def inEdo(self, playerNumber):
        if (len(self.getPlayersInGameNormal()) <= 4):
            if (playerNumber != self.edo): return False
        else:
            if (playerNumber != self.edo and playerNumber != self.bayEdo): return False
        return True

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
                    self.winProcedures(playerToCheck)
                break
    
    def winProcedures(self, winPlayer):
        self.updateMessage("Player " + str(winPlayer) + " wins!")
        self.isGameOver = True
        self.buttonPhase = -1

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
                    playersToDamage.append(self.getPlayersInGameNormal()[i])
        else:
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.inEdo(self.getPlayersInGameNormal()[i]) == damageBool):
                    playersToDamage.append(self.getPlayersInGameNormal()[i])
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
            self.updateMessage("Player " + str(self.getPlayersInGameNormal()[0]) + " wins!")
    
    def buy(self, cardNumber):
        response = ""
        if (self.buttonPhase != 2):
            response = "Not buy phase."
            return response
        if (self.canYield):
            response = "Deal with yield before buying."
            return response
        if (self.canBuy):
            ## Cardnumber hard coded to 10 for done buying, poor, FIX CHANGE
            if (cardNumber == 10):
                self.advanceTurn()
                return response
            elif (len(self.deck) - 1 < cardNumber):
                response = "Cannot buy card " + str(cardNumber + 1) + " because it doesn't exist."
                return response
            else:
                boughtCard = self.deck[cardNumber]
                boughtCardModifiedCost = self.getModifiedCost(self.currentTurn, boughtCard['cost'])
                if (boughtCardModifiedCost > self.getEnergyNormal()[self.currentTurn - 1]):
                    response = 'Not enough money to buy.'
                    return response
                else:
                    self.updateMessage("Player " + str(self.currentTurn) + " bought card " + boughtCard['name'] + ".")
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

    def removeFromEdo(self, player):
        if (self.edo == player):
            self.edo = 0
        elif (self.bayEdo == player):
            self.bayEdo = 0

    def clearBuy(self):
        response = ""
        if (self.buttonPhase != 2):
            response = "Not buy phase."
            return response
        if (self.getEnergyNormal()[self.currentTurn - 1] < 2):
            response = "Not enough money to clear."
            return response
        self.addEnergy(self.currentTurn, -2)
        # CHANGED IMPLEMENT FIX 
        del self.deck[0]
        del self.deck[0]
        del self.deck[0]
        self.updateMessage("Buy cards cleared by Player " + str(self.currentTurn) + ".")
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
            self.updateMessage("Player " + str(self.currentTurn) + " earns 3 points from card.")
            self.addPoints(self.currentTurn, 3)
        elif card['name'] == 'Commuter Train':
            self.updateMessage("Player " + str(self.currentTurn) + " earns 2 points from card.")
            self.addPoints(self.currentTurn, 2)
        elif card['name'] == 'Corner Store':
            self.updateMessage("Player " + str(self.currentTurn) + " earns 1 points from card.")
            self.addPoints(self.currentTurn, 1)
        elif card['name'] == 'Evacuation Orders':
            self.updateMessage("All players (other than the active player) lose 5 points.")
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.currentTurn != self.getPlayersInGameNormal()[i]):
                    self.addPoints(self.getPlayersInGameNormal()[i], -5)
        elif card['name'] == 'Fire Blast':
            self.updateMessage("All players (other than the active player) take 2 damage.")
            playersToFireBlast = []
            for i in range(len(self.getPlayersInGameNormal())):
                if (self.currentTurn != self.getPlayersInGameNormal()[i]):
                    playersToFireBlast.append(self.getPlayersInGameNormal()[i])
            for i in range(len(playersToFireBlast) -1, -1, -1):
                self.changeHealth(playersToFireBlast[i], -2)
        elif card['name'] == 'Heal':
            self.changeHealth(self.currentTurn, 2)
        elif card['name'] == 'Gas Refinery':
            self.updateMessage("All players (other than the active player) take 3 damage.")
            for i in range(len(self.getPlayersInGameNormal()) -1, -1, -1):
                if (self.currentTurn != self.getPlayersInGameNormal()[i]):
                    self.changeHealth(self.getPlayersInGameNormal()[i], -3)
            self.addPoints(self.currentTurn, 2)
        elif card['name'] == 'High Altitude Bombing':
            for i in range(len(self.getPlayersInGameNormal()) - 1, -1, -1):
                print("index", i)
                self.changeHealth(self.getPlayersInGameNormal()[i], -3)
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
            print("Card number" + str(cardNumber))
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
                try:
                    newIndex = self.getPlayersInGameNormal().index(potentialPlayers[i])
                except ValueError:
                    newIndex = -1
                if (newIndex != -1):
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
            if (self.getEnergyNormal()[self.currentTurn - 1] == 0):
                self.updateMessage("Solar Powered activated.")
                self.addEnergy(self.currentTurn, 1)
        if (self.hasCard(self.currentTurn, "Energy Hoarder") and self.getEnergyNormal()[self.currentTurn - 1] >= 6):
            self.updateMessage("Energy Hoarder activated.")
            energyToAdd = math.floor(self.getEnergyNormal()[self.currentTurn - 1] / 6)
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
                        self.addPoints(self.getPlayersInGameNormal()[i], 1)

    def startTurnProcedures(self):
        if (self.inEdo(self.currentTurn)):
            pointsToEarn = 2
            self.updateMessage("Player " + str(self.currentTurn) + " starts in Edo.")
            if (self.hasCard(self.currentTurn, "Urbavore")):
                self.updateMessage("Urbavore activated. One extra point earned for starting in Edo.")
                pointsToEarn += 1
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
