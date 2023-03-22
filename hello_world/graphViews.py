from django.http import HttpResponse
from .evernoteDataParsing.privateSrc.mySqlGraphCall import *
from .evernoteDataParsing.src.globalConstants import *
import os

def refreshGraph(request, dataName, timeGroup, noWeekend, minZero, graphType, normalizeData, noLegend, fromFirstValidDate):
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
    elif (graphType == HISTOGRAM):
        optionsDict[HISTOGRAM] = HISTOGRAM
    elif (graphType == SIMPLE_LINEAR_REGRESSION):
        print("graphing SLR")
        optionsDict[SIMPLE_LINEAR_REGRESSION] = SIMPLE_LINEAR_REGRESSION
    else:
        print("defaulting to line graph")

    if (noWeekend != "IncludeWeekends"):  optionsDict[NO_WEEKEND] = NO_WEEKEND
    if (minZero == "YZeroMin"):  optionsDict[Y_MIN] = 0
    if (normalizeData == "NormalizeData"): optionsDict[NORMALIZE] = True
    else: print("NOT NORMALIZING")

    if (noLegend == REMOVE_LEGEND):
        optionsDict[REMOVE_LEGEND] = REMOVE_LEGEND
    
    if (fromFirstValidDate == FROM_FIRST_VALID_DATE):
        optionsDict[FROM_FIRST_VALID_DATE] = FROM_FIRST_VALID_DATE
        print("graphing from first valid date")

    print(optionsDict)

    databaseName = os.getenv(DATABASE_NAME_ARG)
    if databaseName == None:
        return httpErrorResponse(Exception("ERROR: database not set"))
    # print()
    # print()
    # print()
    # myDatabase = PRIVATE_DATABASE_ARG
    # print("CONFIGURED FOR PRIVATE DATABASE. CHANGE FOR PRODUCTION")
    # print()
    # print()
    # print()

    try:
        if "," in dataName:
            dataNameArray = dataName.split(",")
            if (SIMPLE_LINEAR_REGRESSION in optionsDict):
                if (len(dataNameArray) != 2):
                    raise(Exception("Wrong number of data series"))
                fileName = sqlGraphRegression(dataNameArray[0], dataNameArray[1], optionsDict, optionsDict, {}, databaseName)
            else:
                fileName = sqlGraphMultiple(dataNameArray, optionsDict, databaseName)
        else:
            fileName = sqlGraphMultiple([dataName], optionsDict, databaseName)
        print("fileName %s" % fileName)
        return HttpResponse(fileName)
    except Exception as e:
        return httpErrorResponse(e)

def httpErrorResponse(error):
    if (error != None):
        print(error)
    return HttpResponse(status=500)