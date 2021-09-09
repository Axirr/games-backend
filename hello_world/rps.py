from django.db import models
from django.core import serializers
from django_mysql.models import ListCharField
from django.db.models import CharField
import copy
import random
import math

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
