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
        #     newDeck = ["guard", "guard", "guard", "guard", "guard", "priest", "priest", "baron", "baron", "handmaiden",
        # "handmaiden", "prince", "prince", "king", "countess", "princess"]
            newDeck = ["guard", "guard", "guard", "guard", "guard", "baron", "baron", "handmaiden",
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
        self.message = ["blank message","blank message","blank message","blank message","blank message","blank message"]

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
        if (not (cardIndex == -1) and self.isOnlyHandmaidenTargets(card)):
            self.updateMessage("Player " + str(self.currentTurn) + " played a " + card + " but had no valid targets.")
            isDrawCardPlayed = (card == self.drawCard)
            self.normalDrawAndAdvance(isDrawCardPlayed)
        else:
            self.applyCardEffect(card, target, guardGuess)

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
        print(newMessage)
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
    
    def winProcedures(self, player):
        self.updateMessage("Player " + str(player) + " wins!")
        # self.isGameOver = True
        # window.alert("Player " + player + " wins!")
    
    
    def applyCardEffect(self, card, myTarget, guess):
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
            # self.alertWindow("Player " + str(myTarget) + " has a " + self.hands[myTarget - 1])
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