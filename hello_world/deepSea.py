from django.db import models
from django.core import serializers
from django_mysql.models import ListCharField
from django.db.models import CharField
import copy
import random
import math

class DeepSeaGame(models.Model):
    playersInGame = models.JSONField(
        default=dict
    )
    currentTurn = models.IntegerField(default=1)
    savedTreasure = models.JSONField(
        default=dict
    )
    heldTreasure = models.JSONField(
        default=dict
    )
    dice = models.JSONField(
        default=dict
    )
    message = models.JSONField(
        default=dict
    )
    points = models.JSONField(
        default=dict
    )
    board = models.JSONField(
        default = dict
    )
    isUp = models.JSONField(
        default = dict
    )
    treasureBoard = models.JSONField(
        default = dict
    )
    oxygenCounter = models.IntegerField(default=25)
    remainingRounds = models.IntegerField(default=3)
    doRemove = models.BooleanField(default=False)
    maxPlayers = models.IntegerField(default=4)
    doShuffle = models.BooleanField(default=True)
    maxRemainingRounds = models.IntegerField(default=3)
    buttonPhase = models.IntegerField(default=0)
    maxOxygen = models.IntegerField(default=25)

    def setup(self, numberOfPlayers):
        print("numberOfPlayers", numberOfPlayers)
        self.maxPlayers = numberOfPlayers
        newPlayers = []
        newSavedTreasures = []
        newHeldTreasures = []
        newPoints = []
        newIsUp = []
        # for (i = 1 i <= self.maxPlayers i++) { 
        for i in range(1, self.maxPlayers + 1):
            newPlayers.append(i)
            newSavedTreasures.append([])
            newHeldTreasures.append([])
            newPoints.append(0)
            newIsUp.append(False)
        self.playersInGame = newPlayers
        self.currentTurn = 1
        self.savedTreasure = newSavedTreasures
        self.heldTreasure = newHeldTreasures
        self.dice = ["none", "none"]
        self.message = ["blank message", "blank message", "blank message", "blank message", "blank message", "blank message"]
        self.points = newPoints
        self.board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.isUp = newIsUp
        self.treasureBoard = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4]
        self.oxygenCounter = self.maxOxygen
        self.remainingRounds: self.maxRemainingRounds
        self.buttonPhase = 0
        self.doRemove = False
        # self.doShuffle = self.doShuffle
        # self.maxRemainingRounds = self.maxRemainingRounds
        # self.maxOxygen = self.maxOxygen

    def changeDirection(self, playerNumber, isChangingDirection):
        response = ""
        if (isChangingDirection):
            self.updateMessage("Player " + str(self.currentTurn) + " turns around!")
            self.isUp[self.currentTurn - 1] = True
        else:
            self.updateMessage("Player " + str(self.currentTurn) + " continues on!")
        self.buttonPhase = 1
        return response
    
    def setDice(self, diceArray):
        self.dice = diceArray
        print("New dice are", self.dice)
    
    def roll(self, withRoll = True, withAdvance = False):
        response = ""
        if (withRoll):
            self.dice = [
                random.choice([1,2,3]),
                random.choice([1,2,3]),
            ]
        else:
            print(self.dice)
        self.buttonPhase = 2
        self.updateMessage("Player " + str(self.currentTurn) + " rolls " + str(self.dice[0] + self.dice[1]) + ".")
        self.resolveRoll()
        if (withAdvance):
            self.advanceTurn()
        return response
    
    def resolveRoll(self):
        self.movePlayerForDice()

    def movePlayerForDice(self):
        movementValue = max(self.getRollValue() - self.getCurrentTreasureNumberForPlayer(self.currentTurn),0)
        playerIndex = -1
        try:
            playerIndex = self.board.index(self.currentTurn)
        except ValueError:
            pass
        indexToMoveTo = 0
        if (playerIndex == -1):
            indexToMoveTo = -1
            print("Initial move.")
        else:
            self.board[playerIndex] = 0
            print("Not initial move.")
            indexToMoveTo = playerIndex
        remainingMoves = movementValue
        incrementor = 1
        if (self.isUp[self.currentTurn - 1]):
            incrementor = -1
            print("negative incrementor")
            print("remaining moves(outside) " + str(remainingMoves))
        print("indexToMoveTo", indexToMoveTo)
        print("incrementor", incrementor)
        while (remainingMoves > 0):
            indexToMoveTo = self.nextFreeSpace(indexToMoveTo + incrementor)
            remainingMoves = remainingMoves - 1
            print("Remaining moves" + str(remainingMoves))
        if (indexToMoveTo >= 0):
            self.board[indexToMoveTo] = self.currentTurn
        else:
            self.doRemove = True
            print("Players " + str(self.playersInGame))
            for i in range(len(self.heldTreasure)):
                self.savedTreasure[self.currentTurn - 1].append(self.heldTreasure[self.currentTurn - 1][i])
            self.heldTreasure[self.currentTurn - 1] = []
    
    def getRollValue(self):
        return self.dice[0] + self.dice[1]

    def getCurrentTreasureNumberForPlayer(self, playerNumber):
        return len(self.heldTreasure[playerNumber - 1])

    def advanceTurn(self):
        response = ""
        self.buttonPhase = 0
        nextClosestPlayer = 0
        currentIndex = -1
        try:
            currentIndex = self.playersInGame.index(self.currentTurn)
        except ValueError:
            pass
        if (currentIndex == -1):
            potentialPlayers = []
            # for (var i = 1 i < self.totalNumberOfPlayers i++) {
            for i in range(1, self.totalNumberOfPlayers):
                player = i + self.currentTurn 
                if (player <= self.totalNumberOfPlayers):
                    potentialPlayers.append(player)
                else:
                    potentialPlayers.append(player % self.totalNumberOfPlayers)
            nextClosestPlayer = self.playersInGame[0]
            for i in range(0, len(potentialPlayers)):
                if (self.playersInGame.index(potentialPlayers[i]) != -1):
                    print("Next player is " + str(potentialPlayers[i]))
                    nextClosestPlayer = potentialPlayers[i]
                    break
        else:
            nextClosestPlayer = self.playersInGame[(currentIndex + 1) % len(self.playersInGame)] 
        if (self.doRemove):
            self.doRemove = False
            # self.playersInGame.splice(self.playersInGame.index(self.currentTurn), 1)
            del self.playersInGame[self.currentTurn]
        print("Next closest player" + str(nextClosestPlayer))
        self.currentTurn = nextClosestPlayer
        self.startTurnProcedures()
        return response

    def startTurnProcedures(self):
        self.subtractOxygen()
        self.resetRoll()
        if (self.oxygenCounter <= 0):
            self.remainingRounds -= 1
            if (self.remainingRounds == 0):
                self.buttonPhase = -1
                self.determineWinner()
            else:
                self.createNewRound()

    def createNewRound(self):
        # Drop held treasures
        self.updateMessage("IMPLEMENT TREASURE DROP")
        self.printTreasureStatus()

        self.playersInGame = []
        print("Max players " + str(self.maxPlayers))
        # for (i = 0 i < self.maxPlayers i++) {
        for i in range(0, self.maxPlayers):
            self.playersInGame.append(i + 1)

        # Reset saved treasures
        # for (i = 0 i < len(self.playersInGame) i++) {
        for i in range(0, len(self.playersInGame)):
            self.heldTreasure[i] = []

        # for (i = len(self.treasureBoard) - 1 i >= 0 i--) {
        for i in range(len(self.treasureBoard) - 1, -1, -1):
            if (self.treasureBoard[i] == "x"):
                self.treasureBoard.splice(i, 1)
        self.board = []
        # for (i = 0 i < len(self.treasureBoard) i++) {
        for i in range(0, len(self.treasureBoard)):
            self.board.append(0)

        self.oxygenCounter = self.maxOxygen
        self.currentTurn = 1
        self.dice = ["none", "none"]
        self.isUp = [False, False, False, False]

    def printTreasureStatus(self):
        # for (i = 0 i < len(self.savedTreasure) i++) {
        for i in range(0, len(self.savedTreasure)):
            self.updateMessage("Player " + str(i + 1) + " treaure: " + str(self.savedTreasure[i]))

    def determineWinner(self):
        singlePoints = [0,0,1,1,2,2,3,3]
        doublePoints = [4,4,5,5,6,6,7,7]
        triplePoints = [8,8,9,9,10,10,11,11]
        quadPoints = [12,12,13,13,14,14,15,15]
        points = []
        # for (i = 0 i < self.maxPlayers i++) {
        for i in range(0, self.maxPlayers):
            points.append(0)
        # for (i = 0 i < self.maxPlayers i++) {
        for i in range(0, self.maxPlayers):
            treasures = self.savedTreasure[i]
            # for (j = 0 j < len(treasures) j++) {
            for j in range(0, len(treasures)):
                if (treasures[j] == 1):
                    points[i] = points[i] + singlePoints.splice(Math.floor(Math.random() * len(singlePoints)), 1)
                else:
                    print("Not equal to 1. Is self right?")
        maxPlayerNumber = -1
        maxPointValue = -1
        # for (i = 0 i < len(points) i++) {
        for i in range(0, len(points)):
            if (points[i] > maxPointValue):
                maxPlayerNumber = i
                maxPointValue = points[i]

        self.updateMessage("Player " + str(maxPlayerNumber + 1) + " wins with " + str(maxPointValue) + " points!")
        # IMPLEMENT TIE

    def subtractOxygen(self):
        treasureNumber = self.getCurrentTreasureNumberForPlayer(self.currentTurn)
        self.updateMessage(str(treasureNumber) + " oxygen is subtracted.")
        self.oxygenCounter -= treasureNumber

    def resetRoll(self):
        self.dice = ["none", "none"]

    def nextFreeSpace(self, targetIndex):
        returnIndex = 0
        incrementor = 1
        if (self.isUp[self.currentTurn - 1]):
            incrementor = -1
        if (True):
            # for (i = targetIndex i >= -1 i = i + incrementor) {
            # BUG for reverse iteration?
            i = targetIndex
            while (i >= 0):
            # for i in range(targetIndex, -1, incrementor):
                # // Bounce back
                testValue = i
                if (i >= len(self.board)):
                    testValue = (len(self.board) - 1) - (i - len(self.board))
                print("Testing index " + str(testValue))
                if (self.board[testValue] == 0):
                    returnIndex = testValue
                    break
                if (testValue == -1):
                    returnIndex = -1
                    break
                i = i + incrementor
        return returnIndex

    def spaceHasTreasure(self):
        try:
            playerIndex = self.board.index(self.currentTurn)
        except ValueError:
            playerIndex = -1
        if (playerIndex == -1):
            return False
        return self.treasureBoard[playerIndex] != "x"

    def playerIsHoldingTreasure(self):
        return (len(self.heldTreasure[self.currentTurn - 1]) > 0)

    def takeTreasure(self):
        response = ""
        playerIndex = self.board.index(self.currentTurn)
        self.heldTreasure[self.currentTurn - 1].append(self.treasureBoard[playerIndex])
        self.updateMessage("Player " + str(self.currentTurn) + " takes a treasure with " + str(self.treasureBoard[playerIndex]) + " pips.")
        self.treasureBoard[playerIndex] = "x"
        self.advanceTurn()
        return response

    def dropTreasure(self):
        response = ""
        playerIndex = self.board.index(self.currentTurn)
        self.advanceTurn()
        response = "IMPLEMENT DROP TREASURE"
        return response

    def updateMessage(self, newMessage):
        print(newMessage)
        messageCopy = copy.copy(self.message)
        for i in range(len(messageCopy) - 1):
            messageCopy[i] = messageCopy[i+1]
        messageCopy[len(messageCopy) - 1] = newMessage
        self.message = messageCopy