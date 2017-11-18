import re, os
'''
quick check to see a string might be a Latex comment
'''
def isLatexComment(string):
    pattern = re.compile(r"^\s*%")
    match = pattern.search(string)
    if match:
        return True
    else:
        return False
'''
quick check to see a string might contains homeworks
@param {string} a string to test
@return {boolean} true if string MIGHT be homeworks
'''
def maybeHomeworks(string):
    pattern = re.compile(r"\d{1,2}\s*\.\s*\d{0,2}")
    match = pattern.search(string)
    if match:
        return True
    else:
        return False
'''
accept a list of strings, remove lots of garbage
@param {list} input_strings
@return {list} cleaned_strings, date_strings, date_strings
'''
def removeGarbage(input_strings):
    cleaned_strings = []
    date_strings = []
    time_strings = []

    for string in input_strings:
        temp = removeDate(string)
        string = temp[0]
        if temp[1]:
            date_strings += temp[1]

        temp = removeTime(string)
        string = temp[0]
        if temp[1]:
            time_strings += temp[1]

        cleaned_strings.append(string)

    return [cleaned_strings, date_strings, time_strings]
'''
accept a string, remove date-like substring
@param {inputStr} the string to clean
@return {list} of two items, first cleaned string, second the date-like substring
'''
def removeDate(inputStr):
    pattern = re.compile(r"\d{1,2}[.\-]\d{1,2}[.\-]\d+")
    found  = []

    # regex.search() to search all matches in string
    startpos = 0
    endpos   = len(inputStr)
    match    = pattern.search(inputStr, startpos, endpos)
    while match:
        matchedString = match.group()
        found.append(matchedString)
        inputStr = inputStr.replace(matchedString, "")
        # match.lastindex not valid because there's no grouping in pattern
        match    = pattern.search(inputStr, match.end() - 1, endpos)

    return [inputStr, found]
'''
accept a string, remove time-like substring
@param {inputStr} the string to clean
@return {list} of two items, first cleaned string, second the time-like substring
'''
def removeTime(inputStr):
    pattern = re.compile(r"(\d{1,2}.\d{1,2})*(\s*\-+\s*)*(\d{1,2}.\d{1,2})\s*(Uhr|bis)", flags=re.IGNORECASE)
    found  = []

    # regex.search() while loop to grab all matches
    startpos = 0
    endpos   = len(inputStr)
    match    = pattern.search(inputStr, startpos, endpos)
    while match:
        matchedString = match.group()
        found.append(matchedString)
        inputStr = inputStr.replace(matchedString, "")
        match    = pattern.search(inputStr, match.lastindex, endpos)


    return [inputStr, found]
'''
accepts a string, returns a dictionary of tokenized homework strings
'''
def tokenizeHomework(hwString):
    pattern = re.compile(r"(\d{1,2}[.]\d{1,2})(\s?-+\s?)?(\d{1,2}[.]\d{1,2})?")
    result  = []

    startpos = 0
    endpos   = len(hwString)
    match    = pattern.search(hwString, startpos, endpos)
    while match:
        HW_RANGE_DELIMITER = match.group(2)
        matchedString = match.group()

        # matched groups should be either 1(only 1 homework)
        # or 3 (start homework, the DELIMITER, end homework)
        if match.lastindex not in [1,3]:
            rangeFormatError(HW_RANGE_DELIMITER, match.group())
        else:
            if match.lastindex is 3:
                theRange     = matchedString.split(HW_RANGE_DELIMITER)
                expandedList = expandHomeworkRange(theRange, HW_RANGE_DELIMITER)
                result       = result + expandedList
            else:
                result.append(matchedString)
        # continue searching, startpos is now match.end(match.lastindex)
        match = pattern.search(hwString, match.end(match.lastindex), endpos)

    result = convertToDict(result)
    return result

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
    print("tokenizeHomeworkRange: The correct format for range of homeworks is:")
    print("tokenizeHomeworkRange: [<chapter>.<number>]" + "(\s?-+\s?)" + "[<chapter>.<number>]")
    print("Curent DELIMITER: " + DELIMITER)
    print("Your input " + str(where))

'''
convert a list of homeworks into a dictionary with same content
'''
def convertToDict(hwList):
    hwDict = {}
    for item in hwList:
        dotIndex = item.find(".")
        chapter  = item[:dotIndex]
        nr       = item[dotIndex + 1:]
        if chapter not in hwDict:
            hwDict[chapter] = []
            hwDict[chapter].append(nr)
        else:
            hwDict[chapter].append(nr)
    return hwDict
'''
search a chapter once for all needed homeworks
append them to wz
chDict defines which skript file to read
@param {Object} wz TextIOBase, returned by open(file, "a")
@param {string} chapter which chapter to read from?
@param {list} nrList of homework numbers
@param {Dict} chDict keys are chapter numbers, values are names of textfiles
'''
def searchAndWritePerChapter(wz, chapter, nrList, chDict):
    fileToRead = chDict[chapter]
    if os.path.isfile(fileToRead) is False:
        print("searchAndWritePerChapter: " + fileToRead + " Not Found")
        return

    script = open(fileToRead).readlines()
    for nr in nrList:
        start_signal = "%HOMEWORK_START_" + nr + "\n"
        end_signal = "%HOMEWORK_END_" + nr + "\n"
        try:
            start = script.index(start_signal)
            end = script.index(end_signal, start)
            for i in range(start, end + 1):
                wz.write(script[i])
        except Exception as e:
            print("\nsearchAndWrite: Following signals not found")
            print(start_signal, end="")
            print(end_signal, end="")
            print("for chapter " + chapter + " in file: " + fileToRead)
            continue
