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

        if match.lastindex > 2:
            rangeFormatError(DELIMITER, match.group(match.lastindex))
        else:
            if HW_RANGE_DELIMITER in matchedString:
                theRange = matchedString.split(HW_RANGE_DELIMITER)
                expandedList = expandHomeworkRange(theRange, HW_RANGE_DELIMITER)
                hwList = hwList + expandedList
            else:
                hwList.append(matchedString)

        match = pattern.search(hwString, match.end(match.lastindex), endpos)

    return hwList

'''
accepts a string supposedly represent a range of homeworks
return a list of homeworks in range
'''
def expandHomeworkRange(theRange, DELIMITER):
    cleanedRange = []
    for item in theRange:
        item = item.strip()
        cleanedRange.append(item)
    dotIndex = cleanedRange[0].find(".")
    chapA    = cleanedRange[0][:dotIndex]
    chapB    = cleanedRange[1][:dotIndex]


    # check if same chapter
    if chapA != chapB:
        rangeFormatError(DELIMITER, theRange)
        return []
    else:
        chapter = chapA

    # get homework number
    firstHomework = int(cleanedRange[0][dotIndex + 1:]) # +1 since start index is inclusive
    lastHomework  = int(cleanedRange[1][dotIndex + 1:])
    if lastHomework < firstHomework:
        swap = lastHomework
        lastHomework = firstHomework
        firstHomework = swap

    # expand the homework range
    tokenized = []
    for i in range(firstHomework, lastHomework + 1): # +1 since end of range is exclusive
        tokenized.append(chapter + "." + str(i))

    return tokenized

def rangeFormatError(DELIMITER, where):
    print("tokenizeHomeworkRange: Wrong format of range of homeworks")
    print("tokenizeHomeworkRange: [<chapter>.<number>]" + DELIMITER + "[<chapter>.<number>]")
    print("Curent DELIMITER : " + DELIMITER)
    print("Your input" + str(where))
