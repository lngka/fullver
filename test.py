import re
import fullwz_lib as LIBRARY
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


if __name__ == "__main__":
    filename  = "wz1.tex"
    hwStrings = findHomeworkStrings(filename)
    print(hwStrings)
