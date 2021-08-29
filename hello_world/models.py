from django.db import models
from django.core import serializers
from django_mysql.models import ListCharField
from django.db.models import CharField
import copy
import random

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
        base_field=CharField(max_length=40),
        size=6,
        max_length=(6 * 41),
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
            print("Current turn is ", self.currentTurn)
            print("Players in game ", intPlayersInGame)
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

    def deal(self, numberPlayers):
        newDeck = []
        if (True):
            newDeck = ["guard", "guard", "guard", "guard", "guard", "priest", "priest", "baron", "baron", "handmaiden",
        "handmaiden", "prince", "prince", "king", "countess", "princess"]
        else:
            print("IMPLEMENT DECK SEEDING")
        doShuffle = True
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

    def playCard(self, card, playerNumber, target, guardGuess):
        if (playerNumber != self.currentTurn): 
            print("NOT CURRENT PLAYER")
            return
        self.removeSelfHandmaiden()
        if (self.currentTurn <= 0 ):
            print("GAME IS OVER")
            return
        if (not self.isValidMove(card, target)):
            print("Not a valid move")
            return
        try:
            cardIndex = ["king", "prince", "guard", "priest", "baron"].index(card)
        except ValueError:
            cardIndex = -1
        if (not (cardIndex == -1) and self.isOnlyHandmaidenTargets()):
            self.updateMessage("Player " + self.currentTurn + " played a " + card + " but had no valid targets.")
            isDrawCardPlayed = (card == self.drawCard)
            self.normalDrawAndAdvance(isDrawCardPlayed)
        else:
            self.applyCardEffect(card, target)

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
                    # this.alertWindow("Invalid move. Must play the countess")
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

    def isValidTarget(self, card, targetNumber):
        myTarget = targetNumber

        # Check still in game
        try:
            targetIndex = self.playersInGame.index(myTarget)
        except ValueError:
            targetIndex = -1
        if (targetIndex == -1):
            this.alertWindow("INVALID MOVE. Target not in game.")
            return False


        # Check if handmaiden
        if (self.isOnlyHandmaidenTargets()):
            return True
        elif (this.localState.isHandMaiden[myTarget - 1]):
        # Check not self unless prince
            try:
                secondCardIndex = ['king', 'guard', 'baron', 'priest', 'guard'].index(card)
            except ValueError:
                secondCardIndex = -1
            if (secondCardIndex != -1):
                if (myTarget == this.localState.currentTurn):
                    # this.alertWindow("INVALID MOVE. Cannot target self except with prince.")
                    return False
            elif (this.localState.playersInGame.length > 2):
                # this.alertWindow("INVALID MOVE. Cannot target handmaiden player.")
                return False
            elif (card == "prince"):
                # this.alertWindow("INVALID MOVE. Cannot target handmaiden player. Remember, Prince can target self.")
                return False
        return True
    
    
    def isOnlyHandmaidenTargets(self):
        print("IMPLEMENT IS ONLY HANDMAIDEN TARGET")
        return False
    
    def updateMessage(self, newMessage):
        messageCopy = copy.copy(self.message)
        for i in range(len(messageCopy) - 1):
            messageCopy[i] = messageCopy[i+1]
        messageCopy[len(messageCopy) - 1] = newMessage
        self.message = messageCopy
    
    def getTargetPlayerNumber(self):
        print("IMPLEMENT GET TARGET PLAYER NUMBER")
    
    def normalDrawAndAdvance(self, isDrawCardPlayed): 
        if (not isDrawCardPlayed): 
            self.replaceCard(self.currentTurn)
        else:
            self.replaceCard(0)
        self.advanceTurn()
    
    def resetGame(self): 
        self.deal(self.totalNumberOfPlayers)

    def replaceCard(self, playerNumber):
        if (len(self.deck) == 0):
            drawnCard = "none"
        else:
            drawnCard = self.deck.pop()
        if (playerNumber == 0):
            self.drawCard = drawnCard
            self.checkIfGameOver()
        else:
            copyHands = copy.copy(self.hands)
            copyHands[playerNumber - 1] = self.drawCard
            self.hands = copyHands
            self.drawCard = drawnCard
            self.checkIfGameOver()

    def checkIfGameOver(self):
        if (self.deck.length == 0):
            self.evaluateShowdownWin()
            return
    
    def evaluateShowdownWin(self):
        self.updateMessage("SHOWDOWN! Players compare card values, highest wins.")
        # self.showAllCards()
        maxPlayer = 0
        maxValue = 0
        isTie = False
        for i in range(len(self.playersInGame)):
            currentPlayer = self.playersInGame[i]
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
            self.updateMessage("Tie!")
            # console.log("BUG: Implement tie solution.")

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
    
    def winProcedures(self, winningPlayer):
        print("IMPLEMENT WIN PROCEDURES")

    
    def applyCardEffect(self, card, myTarget):
        # myTarget = self.getTargetPlayerNumber()
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
            this.updateMessage("Player " + str(self.currentTurn) + " played a " + card + " with no direct effect.")
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
            print("IMPLEMENT CARD!")
            pass
        elif (card == 'king'):
            print("IMPLEMENT CARD!")
            pass
        elif (card == 'prince'):
            print("IMPLEMENT CARD!")
            pass
        elif (card == 'handmaiden'):
            self.updateMessage("Player " + str(self.currentTurn) + " is immune until their next turn.")
            handmaidenCopy = copy.copy(self.isHandMaiden)
            handmaidenCopy[self.currentTurn - 1] = '1'
            self.isHandMaiden = handmaidenCopy
            self.normalDrawAndAdvance(isDrawCardPlayed)
        elif (card == 'baron'):
            print("IMPLEMENT CARD!")
            pass
        elif (card == 'priest'):
            print("IMPLEMENT CARD!")
            pass
        elif (card == 'guard'):
            print("IMPLEMENT CARD!")
            pass
        else:
            print("CARD NOT FOUND!")
        # switch(card) {
        #     case 'princess':
        #     case 'countess':
        #         this.normalDrawAndAdvance(isDrawCardPlayed)
        #         break;
        #     case 'king':
        #         this.updateMessage("Player " + this.localState.currentTurn + " trades hand with Player " + myTarget + ".")
        #         var handsCopy = [...this.localState.hands]
        #         var playerOriginalHand = handsCopy[myTarget - 1]
        #         handsCopy[myTarget - 1] = notPlayedCard
        #         handsCopy[this.localState.currentTurn - 1] = playerOriginalHand
        #         this.localState['hands'] = handsCopy
        #         if (!isDrawCardPlayed) {
        #             this.replaceCard(0)
        #             this.advanceTurn()
        #         } else {
        #             this.replaceCard(0)
        #             this.advanceTurn()
        #         }
        #         break;
        #     case 'prince':
        #         this.updateMessage("Player " + myTarget + " discards their hand.")
        #         this.updateMessage("Player " + myTarget + " hand card was a " + this.localState.hands[myTarget - 1] + ".")
        #         var deckCopy = [...this.localState.deck]
        #         var handsCopy = [...this.localState.hands]
        #         var discardedCard = handsCopy[myTarget - 1]
        #         if (myTarget === this.localState.currentTurn) {
        #             if (discardedCard === "prince") {
        #                 var discardedCard = this.localState.drawCard
        #             }
        #         }
        #         if (deckCopy.length >= 1) {
        #             handsCopy[myTarget - 1] = deckCopy.pop()
        #         } else {
        #             handsCopy[myTarget - 1] = this.localState.setAsideCard
        #         }
        #         this.localState['hands'] = handsCopy
        #         if (myTarget === this.localState.currentTurn) {
        #             this.replaceCard(0)
        #             this.advanceTurn()
        #         } else {
        #             this.replaceCard(this.localState.currentTurn)
        #             this.advanceTurn()
        #         }
        #         if (discardedCard === "princess") {
        #             this.eliminatePlayer(myTarget)
        #             this.advanceTurn()
        #         } 
        #         break;
        #     case 'handmaiden':
        #         this.updateMessage("Player " + this.localState.currentTurn + " is immune until their next turn.")
        #         var handmaidenCopy = this.localState.isHandMaiden
        #         handmaidenCopy[this.localState.currentTurn - 1] = true
        #         this.localState['isHandMaiden'] = handmaidenCopy
        #         this.normalDrawAndAdvance(isDrawCardPlayed)
        #         break;
        #     case 'baron':
        #         if (isDrawCardPlayed) {
        #             var playerValue = this.getCardValue(this.localState.hands[this.localState.currentTurn - 1])
        #         } else {
        #             var playerValue = this.getCardValue(this.localState.drawCard)
        #         }
        #         var targetValue = this.getCardValue(this.localState.hands[myTarget - 1])
        #         var playerToEliminate = 0
        #         var message = "Player " + myTarget + " and Player " + this.localState.currentTurn + " tie in baron comparison."
        #         if (playerValue > targetValue) {
        #             playerToEliminate = myTarget
        #             var message = "Player " + this.localState.currentTurn + " wins against Player " + myTarget + " in baron comparison."
        #         } else if (targetValue > playerValue) {
        #             playerToEliminate = this.localState.currentTurn
        #             var message = "Player " + this.localState.currentTurn + " loses against Player " + myTarget + " in baron comparison."
        #         }
        #         this.updateMessage(message)
        #         if (playerToEliminate !== 0) {
        #             this.eliminatePlayer(playerToEliminate)
        #         }
        #         if (!isDrawCardPlayed) {
        #             this.replaceCard(this.localState.currentTurn)
        #         } else {
        #             this.replaceCard(0)
        #         }
        #             this.advanceTurn()
        #         break;
        #     case 'priest':
        #         this.updateMessage("Player " + this.localState.currentTurn + " looks at the hand of Player " + myTarget + ".")
        #         this.alertWindow("Player " + myTarget + " has a " + this.localState.hands[myTarget - 1])
        #         this.normalDrawAndAdvance(isDrawCardPlayed)
        #         break;
        #     case 'guard':
        #         var guess = this.getGuardGuess()
        #         this.updateMessage("Player " + this.localState.currentTurn + " guessed " + guess + ".")
        #         var actualHand = this.localState.hands[myTarget - 1]
        #         var playerToEliminate = 0
        #         var message = "Guess was wrong."
        #         if (guess === actualHand) {
        #             message = "Guess was right!"
        #             playerToEliminate = myTarget
        #         } 
        #         this.updateMessage(message)
        #         if (playerToEliminate !== 0) {
        #             this.eliminatePlayer(playerToEliminate)
        #             this.normalDrawAndAdvance(isDrawCardPlayed)
        #         } else {
        #             this.normalDrawAndAdvance(isDrawCardPlayed)
        #         } 
        #         break;
        #     default:
        #         console.log("ERROR, unidentified card found")
        #         console.log(card)
        # }
        # this.rerenderState()
    # }

    # isOnlyHandmaidenTargets(card) {
    #     var onlyHandmaidens = false
    #     if (card === "prince") {
    #         return onlyHandmaidens
    #     }
    #     for (var i = 0; i < this.localState.playersInGame.length; i++) {
    #         var potentialTarget = this.localState.playersInGame[i]

    #         // found valid target
    #         if (this.localState.isHandMaiden[potentialTarget - 1] === false && potentialTarget !== this.localState.currentTurn) {
    #             break;
    #         }

    #         // Reached end of search, no valid target found
    #         if (i === (this.localState.playersInGame.length - 1)) {
    #             onlyHandmaidens = true;
    #         }
    #     }
    #     return onlyHandmaidens
    # }

    # isElimCardEffect(card) {
    #     var myTarget = this.getTargetPlayerNumber()
    #     this.localState.playedCards.push(card)
    #     if (["guard","priest","baron", "prince", "king"].indexOf(card) !== -1) {
    #         this.updateMessage("Player " + this.localState.currentTurn + " played a " + card + " targeting Player " + myTarget + ".")
    #     } else if (["handmaiden"].indexOf(card) !== -1){
    #         this.updateMessage("Player " + this.localState.currentTurn + " played a " + card + ".")
    #     } else {
    #         this.updateMessage("Player " + this.localState.currentTurn + " played a " + card + " with no direct effect.")
    #     }
    #     var isDrawCardPlayed = (card === this.localState.drawCard)
    #     if (isDrawCardPlayed) {
    #         var notPlayedCard = this.localState.hands[this.localState.currentTurn - 1]
    #     } else {
    #         var notPlayedCard = this.localState.drawCard
    #     }
    #     switch(card) {
    #         case 'princess':
    #             this.eliminatePlayer(this.localState.currentTurn)
    #             this.replaceCard(0)
    #             this.advanceTurn()
    #             break;
    #         case 'countess':
    #             this.normalDrawAndAdvance(isDrawCardPlayed)
    #             break;
    #         case 'king':
    #             this.updateMessage("Player " + this.localState.currentTurn + " trades hand with Player " + myTarget + ".")
    #             var handsCopy = [...this.localState.hands]
    #             var playerOriginalHand = handsCopy[myTarget - 1]
    #             handsCopy[myTarget - 1] = notPlayedCard
    #             handsCopy[this.localState.currentTurn - 1] = playerOriginalHand
    #             this.localState['hands'] = handsCopy
    #             if (!isDrawCardPlayed) {
    #                 this.replaceCard(0)
    #                 this.advanceTurn()
    #             } else {
    #                 this.replaceCard(0)
    #                 this.advanceTurn()
    #             }
    #             break;
    #         case 'prince':
    #             this.updateMessage("Player " + myTarget + " discards their hand.")
    #             this.updateMessage("Player " + myTarget + " hand card was a " + this.localState.hands[myTarget - 1] + ".")
    #             var deckCopy = [...this.localState.deck]
    #             var handsCopy = [...this.localState.hands]
    #             var discardedCard = handsCopy[myTarget - 1]
    #             if (myTarget === this.localState.currentTurn) {
    #                 if (discardedCard === "prince") {
    #                     var discardedCard = this.localState.drawCard
    #                 }
    #             }
    #             if (deckCopy.length >= 1) {
    #                 handsCopy[myTarget - 1] = deckCopy.pop()
    #             } else {
    #                 handsCopy[myTarget - 1] = this.localState.setAsideCard
    #             }
    #             this.localState['hands'] = handsCopy
    #             if (myTarget === this.localState.currentTurn) {
    #                 this.replaceCard(0)
    #                 this.advanceTurn()
    #             } else {
    #                 this.replaceCard(this.localState.currentTurn)
    #                 this.advanceTurn()
    #             }
    #             if (discardedCard === "princess") {
    #                 this.eliminatePlayer(myTarget)
    #                 this.advanceTurn()
    #             } 
    #             break;
    #         case 'handmaiden':
    #             this.updateMessage("Player " + this.localState.currentTurn + " is immune until their next turn.")
    #             var handmaidenCopy = this.localState.isHandMaiden
    #             handmaidenCopy[this.localState.currentTurn - 1] = true
    #             this.localState['isHandMaiden'] = handmaidenCopy
    #             this.normalDrawAndAdvance(isDrawCardPlayed)
    #             break;
    #         case 'baron':
    #             if (isDrawCardPlayed) {
    #                 var playerValue = this.getCardValue(this.localState.hands[this.localState.currentTurn - 1])
    #             } else {
    #                 var playerValue = this.getCardValue(this.localState.drawCard)
    #             }
    #             var targetValue = this.getCardValue(this.localState.hands[myTarget - 1])
    #             var playerToEliminate = 0
    #             var message = "Player " + myTarget + " and Player " + this.localState.currentTurn + " tie in baron comparison."
    #             if (playerValue > targetValue) {
    #                 playerToEliminate = myTarget
    #                 var message = "Player " + this.localState.currentTurn + " wins against Player " + myTarget + " in baron comparison."
    #             } else if (targetValue > playerValue) {
    #                 playerToEliminate = this.localState.currentTurn
    #                 var message = "Player " + this.localState.currentTurn + " loses against Player " + myTarget + " in baron comparison."
    #             }
    #             this.updateMessage(message)
    #             if (playerToEliminate !== 0) {
    #                 this.eliminatePlayer(playerToEliminate)
    #             }
    #             if (!isDrawCardPlayed) {
    #                 this.replaceCard(this.localState.currentTurn)
    #             } else {
    #                 this.replaceCard(0)
    #             }
    #                 this.advanceTurn()
    #             break;
    #         case 'priest':
    #             this.updateMessage("Player " + this.localState.currentTurn + " looks at the hand of Player " + myTarget + ".")
    #             this.alertWindow("Player " + myTarget + " has a " + this.localState.hands[myTarget - 1])
    #             this.normalDrawAndAdvance(isDrawCardPlayed)
    #             break;
    #         case 'guard':
    #             var guess = this.getGuardGuess()
    #             this.updateMessage("Player " + this.localState.currentTurn + " guessed " + guess + ".")
    #             var actualHand = this.localState.hands[myTarget - 1]
    #             var playerToEliminate = 0
    #             var message = "Guess was wrong."
    #             if (guess === actualHand) {
    #                 message = "Guess was right!"
    #                 playerToEliminate = myTarget
    #             } 
    #             this.updateMessage(message)
    #             if (playerToEliminate !== 0) {
    #                 this.eliminatePlayer(playerToEliminate)
    #                 this.normalDrawAndAdvance(isDrawCardPlayed)
    #             } else {
    #                 this.normalDrawAndAdvance(isDrawCardPlayed)
    #             } 
    #             break;
    #         default:
    #             console.log("ERROR, unidentified card found")
    #             console.log(card)
    #     }
    #     this.rerenderState()
    # }

    # getCardValue(card) {
    #     switch(card) {
    #         case "princess":
    #             return 8
    #         case "countess":
    #             return 7
    #         case "king":
    #             return 6
    #         case "prince":
    #             return 5
    #         case "handmaiden":
    #             return 4
    #         case "baron":
    #             return 3
    #         case "priest":
    #             return 2
    #         case "guard":
    #             return 1
    #         default:
    #             console.log("ERROR, unidentified card found")
    #             console.log(card)
    #             return 0
    #     }

    # }

    #     // Check if handmaiden
    #     if (this.isOnlyHandmaidenTargets()) {
    #         return true
    #     } else if (this.localState.isHandMaiden[myTarget - 1]) {
    #     // Check not self unless prince
    #         if (['king', 'guard', 'baron', 'priest', 'guard'].indexOf(card) !== -1) {
    #             if (myTarget === this.localState.currentTurn) {
    #                 this.alertWindow("INVALID MOVE. Cannot target self except with prince.")
    #                 return false
    #             }
    #         } else if (this.localState.playersInGame.length > 2) {
    #             this.alertWindow("INVALID MOVE. Cannot target handmaiden player.")
    #             return false
    #         } else if (card === "prince") {
    #             this.alertWindow("INVALID MOVE. Cannot target handmaiden player. Remember, Prince can target self.")
    #             return false
    #         }
    #     }
    #     return true
    # }

    # replaceCard(playerNumber) {
    #     // var deckCopy = [...this.localState.deck]
    #     if (this.localState.deck.length == 0) {
    #         var drawnCard = "none"
    #     } else {
    #         var drawnCard = this.localState.deck.pop()
    #     }
    #     if (playerNumber === 0) {
    #         this.localState['drawCard'] = drawnCard
    #         this.checkIfGameOver()
    #     } else {
    #         var copyHands = [...this.localState.hands]
    #         copyHands[playerNumber - 1] = this.localState.drawCard
    #         this.localState['hands'] = copyHands
    #         this.localState['drawCard'] = drawnCard
    #         this.checkIfGameOver()
    #     }
    #     this.hideAllCards()
    # }

    # checkIfGameOver() {
    #     if (this.localState.deck.length === 0) {
    #         this.evaluateShowdownWin()
    #         return
    #     }
    # }

    # evaluateShowdownWin() {
    #     this.updateMessage("SHOWDOWN! Players compare card values, highest wins.")
    #     this.showAllCards()
    #     var maxPlayer = 0
    #     var maxValue = 0
    #     var isTie = false
    #     for (var i = 0; i < this.localState.playersInGame.length; i++) {
    #         var currentPlayer = this.localState.playersInGame[i]
    #         var cardValue = this.getCardValue(this.localState.hands[currentPlayer - 1])
    #         if (cardValue > maxValue) {
    #             maxPlayer = currentPlayer
    #             maxValue = cardValue
    #             isTie = false
    #         } else if (cardValue === maxValue) {
    #             isTie = true
    #         }
    #     }
    #     this.localState['currentTurn'] = -1
    #     this.rerenderState()
    #     if (!isTie) {
    #         this.winProcedures(maxPlayer)
    #         // this.updateMessage("Player " + maxPlayer + " wins showdown!")
    #         // window.alert("Player " + maxPlayer + " wins showdown!")
    #     } else {
    #         this.updateMessage("Tie!")
    #         console.log("BUG: Implement tie solution.")
    #     }
    # }

    # advanceTurn() {
    #     var currentIndex = this.localState.playersInGame.indexOf(this.localState.currentTurn)
    #     if (currentIndex === -1) {
    #         var potentialPlayers = []
    #         for (var i = 1; i < this.localState.totalNumberOfPlayers; i++) {
    #             var player = i + this.localState.currentTurn 
    #             if (player <= this.localState.totalNumberOfPlayers) {
    #                 potentialPlayers.push(player)
    #             } else {
    #                 potentialPlayers.push(player % this.localState.totalNumberOfPlayers)
    #             }
    #         }
    #         var nextClosestPlayer = this.localState.playersInGame[0]
    #         for (var i = 0; i < potentialPlayers.length; i++) {
    #             if (this.localState.playersInGame.indexOf(potentialPlayers[i]) !== -1) {
    #                 nextClosestPlayer = potentialPlayers[i]
    #                 break
    #             }
    #         }
    #         this.localState['currentTurn'] = nextClosestPlayer
    #     } else {
    #         this.localState['currentTurn'] = this.localState.playersInGame[(currentIndex + 1) % this.localState.playersInGame.length]  
    #     }
    #     this.rerenderState()
    # }

    # eliminatePlayer(playerNumber) {
    #     var copyPlayers = [...this.localState.playersInGame]
    #     let index = copyPlayers.indexOf(playerNumber)
    #     copyPlayers.splice(index, 1)
    #     this.localState['playersInGame'] = copyPlayers
    #     this.updateMessage("Player " + playerNumber + " was eliminated.")
    #     this.updateMessage("Player " + playerNumber + " discarded a " + this.localState.hands[playerNumber - 1] + ".")
    #     this.localState.playedCards.push(this.localState.hands[playerNumber - 1])
    #     if (copyPlayers.length === 1) {
    #         this.winProcedures(copyPlayers[0])
    #     }
    # }

    # winProcedures(player) {
    #     this.updateMessage("Player " + player + " wins!")
    #     this.isGameOver = true
    #     window.alert("Player " + player + " wins!")
    #     this.showAllCards()
    # }


    # printState() {
    #     console.log(this.state)
    # }

    # showCurrentPlayerCards() {
    #     var displayCopy = this.localState.isDisplayed
    #     displayCopy[this.localState.currentTurn - 1] = true
    #     displayCopy[this.localState.totalNumberOfPlayers] = true
    #     this.localState['isDisplayed'] = displayCopy
    #     this.rerenderState()
    # }

    # hideAllCards() {
    #     var displayCopy = this.localState.isDisplayed
    #     for (var i = 0; i < displayCopy.length; i++) {
    #         displayCopy[i] = false
    #     }
    #     this.localState['isDisplayed'] = displayCopy
    #     this.rerenderState()
    # }

    # showAllCards() {
    #     var displayCopy = this.localState.isDisplayed
    #     for (var i = 0; i < displayCopy.length; i++) {
    #         displayCopy[i] = true
    #     }
    #     this.localState['isDisplayed'] = displayCopy
    #     this.rerenderState()
    # }

    # renderHands() {
    #     // var newPlayers = [];
    #     // for (var i = 1; i <= this.localState.playersInGame.length; i++ ) {
    #     //     newPlayers.push(i)
    #     // }

    #     //SET STATE COLLECTIVELY

    #     return(
    #         <div>
    #             {this.state.playersInGame.map((number) => {
    #                 return(
    #                 <div class="col-12">Hand {number}{this.state.isDisplayed[number - 1] && 
    #                     <div>
    #                         <div>
    #                     <button id={"hand"+number}> 
    #                     <img src={this.getLinkForCard(this.localState.hands[number - 1])} width="100" 
    #                     onClick={(() => { this.playerPlayCard(number, this.localState.hands[number - 1]) })}/>
    #                     </button> 
    #                         </div>
    #                     </div>}
    #                 </div>);
    #             })}
    #         </div>
    #     );
    # }

    # getLinkForCard(card) {
    #     let imageLink=""
    #     switch (card) {
    #         case "guard":
    #             imageLink=guardCard
    #             break
    #         case "priest":
    #             imageLink=priestCard
    #             break
    #         case "baron":
    #             imageLink=baronCard
    #             break
    #         case "handmaiden":
    #             imageLink=handmaidenCard
    #             break
    #         case "prince":
    #             imageLink=princeCard
    #             break
    #         case "king":
    #             imageLink=kingCard
    #             break
    #         case "countess":
    #             imageLink=countessCard
    #             break
    #         case "princess":
    #             imageLink=princessCard
    #             break
    #         default:
    #             console.log("Error, unrecognized")
    #     }
    #     console.log(imageLink)
    #     return imageLink
    # }

    # renderTargets() {
    #     let allPlayers = []
    #     for (let i = 1; i <= this.localState.totalNumberOfPlayers; i++) {
    #         allPlayers.push(i)
    #     }
    #     return(
    #         <div>
    #             {allPlayers.map((number) => {
    #                 return(
    #                     <div class="col-12">
    #                         <input type="radio" value={number} name="target" defaultChecked/>Player {number}
    #                     </div>
    #             )})}
    #         </div>
    #     );
    # }

    # playTurn(player) {
    #     if (this.isGameOver) {
    #         window.alert("Game is over.")
    #         return
    #     }
    #     // Random choice if not princess
    #     let chosenCard = this.getCardToPlay(player)

    #     // Random valid target
    #     let playersCopy = [...this.localState.playersInGame]
    #     playersCopy = this.returnShuffledDeck(playersCopy)
    #     let playerTarget = playersCopy[0]
    #     for (let i = 0; i < playersCopy.length; i++) {
    #         if (playersCopy[i] !== player && !this.localState.isHandMaiden[playersCopy[i] - 1]) {
    #             playerTarget = playersCopy[i]
    #             break
    #         }
    #     }
    #     this.setTarget(playerTarget)

    #     this.setRandomGoodGuess()

    #     this.rerenderState(() => {
    #         this.playerPlayCard(this.localState.currentTurn, chosenCard)
    #     })
    # }
    
    # doesActivePlayerHaveCard(player, card) {
    #     return (this.localState.hands[player - 1] === card || this.localState.drawCard === card)
    # }

    # getCardToPlay(player) {
    #     const playerIndex = player - 1
    #     let playerHand = [this.localState.hands[playerIndex], this.localState.drawCard]
    #     let chosenCard;
    #     if (playerHand.indexOf("princess") !== -1) {
    #         console.log("Non-princess card played")
    #         playerHand.splice(playerHand.indexOf("princess"), 1)
    #         chosenCard = playerHand[0]
    #     } else if ((this.doesActivePlayerHaveCard(player, "countess")) && ((this.doesActivePlayerHaveCard(player, "prince") || this.doesActivePlayerHaveCard(player, "king")))) {
    #         console.log("Forced countess play.")
    #         chosenCard = "countess"
    #     } else {
    #         if (this.localState.deck.length <= this.localState.playersInGame) {
    #             // play low card to keep higher one for showdown
    #             const handCardValue = this.getCardValue(this.localState.hands[player - 1])
    #             const drawCardValue = this.getCardValue(this.localState.drawCard)
    #             chosenCard = this.localState.hands[player - 1]
    #             if (drawCardValue < handCardValue) {
    #                 chosenCard = this.localState.drawCard
    #             }
    #         } else {
    #             chosenCard = playerHand[Math.floor(Math.random() * 2)]
    #             if (this.doesActivePlayerHaveCard(this.localState.currentTurn, 'guard') && Math.random() < 0.8) {
    #                 chosenCard = "guard"
    #             } else if (this.doesActivePlayerHaveCard(this.localState.currentTurn, "handmaiden") && Math.random() < 0.9) {
    #                 chosenCard = "handmaiden"
    #             } else if (this.doesActivePlayerHaveCard(this.localState.currentTurn, "baron")) {
    #                 let handCopy = [...playerHand]
    #                 handCopy.splice(handCopy.indexOf("baron"), 1)
    #                 if ((this.getCardValue(handCopy[0]) >= 3) && (this.getCardValue(handCopy[0]) > (Math.random() * 10))) {
    #                     chosenCard = "baron"
    #                 }
    #             }
    #         }

    #         // // check if close to end

    #     }
    #     return chosenCard
    # }

    # setTarget(number) {
    #     let radioList = document.getElementsByName("target")
    #     for (let i = 0; i < radioList.length; i++) {
    #         let button = radioList[i]
    #         // console.log(button["value"])
    #         if (Number.parseInt(button["value"]) === number) {
    #             button.checked = true;
    #             break
    #         } 
    #     }
    #     // console.log(radioList)
    # }

    # setRandomGoodGuess(player) {
    #     // console.log(this.localState.playedCards)
    #     let deckCopy = [...this.localState.defaultDeck]
    #     for (let i = 0; i < this.localState.playedCards.length; i++) {
    #         deckCopy.splice(deckCopy.indexOf(this.localState.playedCards[i]), 1)
    #     }
    #     for (let i = (deckCopy.length - 1); i >= 0; i--) {
    #         if (deckCopy[i] === "guard") {
    #             deckCopy.splice(i, 1)
    #         }
    #     }
    #     deckCopy.splice(deckCopy.indexOf(this.localState.drawCard), 1)
    #     deckCopy.splice(deckCopy.indexOf(this.localState.hands[player - 1]), 1)
    #     console.log(deckCopy)
    #     const randomGuessNumber = Math.floor(Math.random() * deckCopy.length)
    #     let randomGuessString = "princess"
    #     if (deckCopy.length > 0) {
    #         randomGuessString = deckCopy[randomGuessNumber]
    #     }
    #     let radioList = document.getElementsByName("guardGuess")
    #     for (let i = 0; i < radioList.length; i++) {
    #         let button = radioList[i]
    #         if (button["value"] === randomGuessString) {
    #             button.checked = true;
    #             break
    #         } 
    #     }
    # }