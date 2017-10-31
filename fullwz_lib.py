import re
'''
accept a string, return a copy without any date in form of mm.dd.yyyy
'''
def removeDate(inputStr):
    pattern = re.compile(r"\d{1,2}\.\d{1,2}\.\d+")

    startpos = 0
    endpos = len(inputStr)
    match = pattern.search(inputStr, startpos, endpos)
    while match:
        matchedString = match.group()
        print("Removed date-like string: " + matchedString)
        inputStr = inputStr.replace(matchedString, "")
        match = pattern.search(inputStr, match.end(), endpos)

    return inputStr
'''
accepts a string, returns a list of tokenized homework strings
'''
def tokenizeHomework(hwString):
    pattern = re.compile(r"(\d{1,2}[.]\d{1,2})(\s?-\s?\d{1,2}[.]\d{1,2})?")
    hwList = []

    startpos = 0
    endpos = len(hwString)
    match = pattern.search(hwString, startpos, endpos)
    while match:
        hwList.append(match.group())
        match = pattern.search(hwString, match.end(match.lastindex), endpos)

    return hwList

'''
accepts a string supposedly represent a range of homeworks
return a list of homeworks in range
'''
def tokenizeHomeworkRange(item, HW_RANGE_DELIMITER):
    pattern = re.compile(r"\d{1,2}\.\d{1,2}")
    theRange = []

    startpos = 0
    endpos = len(item)
    match = pattern.search(hwString, startpos, endpos)
    while match:
        hwList.append(match.group())
        match = pattern.search(hwString, match.end(), endpos)

    if len(theRange) != 2:
        pass
    return hwList
