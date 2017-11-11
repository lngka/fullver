import sys
import os.path
import re
import fullwz_lib as LIBRARY

"""
Script identifies the required homeworks in an incomplete wz file,
looks for the content of each homework, and finally appends said contents
to the original wz file.

wz: Wochenzettel for Prof. Hagerup
"""
def main():
    # param checks
    if len(sys.argv) != 2:
        print("Usage: python " + sys.argv[0] + " <wz.tex>")
        exit(1)
    if os.path.isfile(sys.argv[1]) is False:
        print("Usage: python " + sys.argv[0] + " <FULL FILENAME>")
        exit(2)

    # extract a dictionary of homeworks from wz
    filename = sys.argv[1]
    hwString = findHomeworkString(filename)
    hwDict   = buildHomeworkDict(hwString)
    print("Found following assignments: \n"+ str(hwDict))

    # append the homework to wz with the dictionary
    chapterDict = {
        "1": "ein.tex",
        "2": "grund.tex",
        "3": "sort.tex",
        "4": "model.tex",
        "5": "einfach.tex",
        "6": "prio.tex",
        "7": "bal.tex",
        "8": "hash.tex",
        "9": "union.tex",
        "10": "dfs.tex",
        "11": "kurz.tex"
    }
    appendHomework(filename, hwDict, chapterDict)
    return 0
"""
find input file for a string which tells the weekly homework
@param {string} filename
@return {string} hwString homework string
"""
def findHomeworkString(filename):
    wz       = open(filename, "r")
    hwString = ""

    # signal is a line of text that should be pre-written in wz
    signal   = "%HOMEWORK_NEXT_LINE"
    grabNext = False
    for line in wz.readlines():
        if grabNext is True:
            hwString = line
            break
        if signal in line:
            grabNext = True

    # just in case
    if grabNext is False:
        print("findHomeworkString: signal not found in wz")
        wz.close()
        exit(3)

    wz.close()
    return hwString

"""
find input file for a string which tells the weekly homework
@param  {string} filename
@return {list} hwStrings homework strings
"""
def findHomeworkStrings(filename):
    wz        = open(filename, "r")
    hwStrings = []
    temp      = []

    # first check for strings that MIGHT be homeworks
    for line in wz.readlines():
        if LIBRARY.isLatexComment(line):
            continue
        elif LIBRARY.maybeHomeworks(line):
            temp.append(line)
    wz.close()

    # remove things that are not homeworks
    temp = LIBRARY.removeGarbage(temp)

    # keep only strings that MIGHT be homeworks
    # after garbage removal surely they'll be homeworks
    for string in temp:
        if LIBRARY.maybeHomeworks(string):
            hwStrings.append(string)


    # report & return
    if len(hwStrings):
        return hwStrings
    else:
        return None

"""
format the string into a list of homeworks
@return {dictionary} hwDict
currently print the first passed in argument
"""
def buildHomeworkDict(hwString):
    # remove all date-like strings
    hwString = LIBRARY.removeDate(hwString)
    # identifies homeworks, also expand range of homeworks
    # e.g. 3.3-3.6 will be expanded to [3.3, 3.4, 3.5, 3.6]
    hwDict   = LIBRARY.tokenizeHomework(hwString)

    # just in case
    if len(hwDict) == 0:
        print("buildHomeworkDict: No homework found")
        exit(5)
    else:
        return hwDict

"""
write the required homeworks to a file
@param {string} filename to write to
@param {hwDict} dictionary with keys being chapter number
                and values are arrays holding required homeworks' number
@param {chDict} chDict chapter dictionary
"""
def appendHomework(filename, hwDict, chDict):

    wz = open(filename, "a")
    wz.write("\n")
    wz.write("\\newpage\n")
    wz.write("\\begin{Tproblemsection}\n")
    wz.write("\\renewcommand{\label}[1]{\\ignorespaces}\n")
    wz.write("\\noindent{\\bf Auszug aus dem Skript:}\n")

    for chapter in hwDict:
        LIBRARY.searchAndWritePerChapter(wz, chapter, hwDict[chapter], chDict)


    wz.close()
    return 0
'''
run main() if script was executed directly
'''
if __name__ == "__main__":
    main()
