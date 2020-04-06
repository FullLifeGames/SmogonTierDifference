import datetime
import requests

tier = "gen8ou"
rankingStage = 1695

def dataToDict(data):
    dictionary = {}
    for line in data.split('\n'):
        if line.startswith(" | Rank"):
            continue
        elif line.startswith(" | "):
            line = line[line.index("|") + 1:]
            line = line[line.index("|") + 2:]
            pokemon = line[:line.index("|")].strip()
            line = line[line.index("|") + 2:]
            value = float(line[:line.index("|")].strip().replace("%", ""))

            dictionary[pokemon] = value
    return dictionary

def filterKey(currentDict, lastDict):
    for key in list(currentDict.keys()):
        if key not in lastDict:
            del currentDict[key]
    for key in list(lastDict.keys()):
        if key not in currentDict:
            del lastDict[key]

today = datetime.date.today()
first = today.replace(day=1)
currentMonth = first - datetime.timedelta(days=1)
lastfirst = currentMonth.replace(day=1)
lastMonth = lastfirst - datetime.timedelta(days=1)

tierUrl = "https://www.smogon.com/stats/{:d}-{:02d}/{:s}-{:d}.txt"

currentTierUrl = tierUrl.format(currentMonth.year, currentMonth.month, tier, rankingStage)
lastTierUrl = tierUrl.format(lastMonth.year, lastMonth.month, tier, rankingStage)

currentData = requests.get(currentTierUrl).text
lastData = requests.get(lastTierUrl).text

currentDict = dataToDict(currentData)
lastDict = dataToDict(lastData)

filterKey(currentDict, lastDict)

resultList = [[key, currentDict[key] - lastDict[key]] for key in currentDict]

resultList.sort(key = lambda val: abs(val[1]), reverse = True)

resultDict = {}
for key in resultList:
    resultDict[key[0]] = key[1]

with open("tierDiff.txt", "w") as f:    
    header = "Pokemon              | Last      | Current   | Change\n"
    f.write(header)
    for entry in resultList:
        key = entry[0]
        formatString = "{:20s} | {:8.5f}% | {:8.5f}% | {:s}{:9.5f}%\n"
        f.write(formatString.format(key, lastDict[key], currentDict[key], "+" if resultDict[key] >= 0 else "-", abs(resultDict[key])))