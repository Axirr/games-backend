from django.http import HttpResponse
from .evernoteDataParsing.privateSrc.mySqlGraphCall import *

def refreshGraph(request, dataName, timeGroup, noWeekend, minZero, graphType, normalizeData):
    optionsDict = {}
    
    if (timeGroup == "Daily"):
        # Not sure about this one
        timeGroup = "date"
    elif timeGroup == "Rolling Average = 5":
        optionsDict[ROLLING_AVERAGE] = 5
    elif timeGroup == "Rolling Average = 7":
        optionsDict[ROLLING_AVERAGE] = 7
    else:
        optionsDict[timeGroup] = timeGroup
    
    if (graphType == BOX_PLOT):
        optionsDict[BOX_PLOT] = timeGroup
    elif (graphType == BAR_OPTION):
        optionsDict[BAR_OPTION] = timeGroup
    else:
        print("defaulting to line graph")

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
        print("Trying out multi graph for single graph")
        # fileName = sqlWrapperGraphCall(dataName, optionsDict)
        fileName = sqlGraphMultiple([dataName], optionsDict)


    return HttpResponse(fileName)