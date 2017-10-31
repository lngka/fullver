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
        HW_RANGE_DELIMITER = "-"
        matchedString = match.group()

        if HW_RANGE_DELIMITER in matchedString:
            e = tokenizeHomeworkRange(matchedString, HW_RANGE_DELIMITER)
            hwList = hwList + e
        else:
            hwList.append(matchedString)

        match = pattern.search(hwString, match.end(match.lastindex), endpos)

    return hwList

'''
accepts a string supposedly represent a range of homeworks
return a list of homeworks in range
'''
def tokenizeHomeworkRange(item, DELIMITER):
    pattern = re.compile(r"\d{1,2}\.\d{1,2}")
    theRange = []

    startpos = 0
    endpos = len(item)
    match = pattern.search(item, startpos, endpos)
    while match:
        theRange.append(match.group())
        match = pattern.search(item, match.end(), endpos)

    # just in case
    if len(theRange) != 2:
        rangeFormatError(DELIMITER)
        return []

    # check if same chapter
    dotIndex = theRange[0].find(".")
    chapA = theRange[0][:dotIndex]
    chapB = theRange[1][:dotIndex]
    if chapA != chapB:
        rangeFormatError(DELIMITER)
        return []
    else:
        chapter = chapA

    # get homework number
    firstHomework = int(theRange[0][dotIndex + 1:]) # +1 since start index is inclusive
    lastHomework  = int(theRange[1][dotIndex + 1:])
    if lastHomework < firstHomework:
        swap = lastHomework
        lastHomework = firstHomework
        firstHomework = swap

    # expand the homework range
    tokenized = []
    for i in range(firstHomework, lastHomework + 1): # +1 since end of range is exclusive
        tokenized.append(chapter + "." + str(i))

    return tokenized

def rangeFormatError(DELIMITER):
    print("tokenizeHomeworkRange: Wrong format of range of homeworks")
    print("tokenizeHomeworkRange: [<chapter>.<number>]" + DELIMITER + "[<chapter>.<number>]")
    print("Curent DELIMITER : " + DELIMITER)
