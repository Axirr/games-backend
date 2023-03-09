from django.http import FileResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .evernoteDataParsing.src.mySqlGraphCall import *
import time
import asyncio

def refreshGraph(request, dataName, timeGroup, noWeekend, minZero, boxPlot, normalizeData):
    optionsDict = {}
    
    if (timeGroup == "Daily"):
        pass
    elif timeGroup == "Rolling Average = 5":
        optionsDict[ROLLING_AVERAGE] = 5
    elif timeGroup == "Rolling Average = 7":
        optionsDict[ROLLING_AVERAGE] = 7
    else:
        optionsDict[timeGroup] = timeGroup
    
    if (boxPlot == BOX_PLOT):
        optionsDict[BOX_PLOT] = timeGroup
    else:
        print("no box plot since isBoxPlot is %s" % boxPlot)

    if (noWeekend != "IncludeWeekends"):  optionsDict[NO_WEEKEND] = NO_WEEKEND
    if (minZero == "YZeroMin"):  optionsDict[Y_MIN] = 0
    if (normalizeData == "NormalizeData"): optionsDict[NORMALIZE] = True
    else: print("NOT NORMALIZING")
    print(optionsDict)


    if "," in dataName:
        dataNameArray = dataName.split(",")
        print(dataNameArray)
        fileName = sqlGraphMultiple(dataNameArray, optionsDict)
    else:
        # Don't think we need this async
        fileName = asyncio.run(sqlWrapperGraphCall(dataName, optionsDict))


    return HttpResponse(fileName)