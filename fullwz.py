import sys
import os.path
import re
import fullwz_lib as LIBRARY

"""
Script identifies the required homeworks in an incomplete wz file,
looks for the content of each homework, and finally append said contents
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

    filename = sys.argv[1]
    hwString = findHomeworkString(filename)
    # build an array of exercise
    hwList = buildHomeworkList(hwString)
    # append to input file
    appendHomework(filename, hwList)

"""
find input file for a string which tells the weekly homework
@param {string} filename
@return {string} hwString homework string
currently return "hwString"
"""
def findHomeworkString(filename):
    wz = open(filename, "r")
    hwString = ""

    # signal is a line of text in the incomplete wz
    signal = "%HOMEWORK_NEXT_LINE"
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
format the string into a list of homeworks
@return {dictionary} hwList
currently print the first passed in argument
"""
def buildHomeworkList(hwString):
    hwString = LIBRARY.removeDate(hwString);
    rawList = LIBRARY.tokenizeHomework(hwString);

    # just in case
    if len(rawList) == 0:
        print("buildHomeworkList: No homework found")
        exit(5)

    hwList = []
    HW_RANGE_DELIMITER = "-"
    for item in rawList:
        if HW_RANGE_DELIMITER in item:
            items = LIBRARY.tokenizeHomeworkRange(item, HW_RANGE_DELIMITER);
            hwList = hwList + items
        else:
            hwList.append(item)


    return hwList

"""
add the needed homeworks to the Wochenzettel
@param {Object} wz the file object of the Wochenzettel
@param {list} hwList homework list
"""
def appendHomework(wz, hwList):
    print("appendHomework print hwList")
    print(hwList)
    return 0

# run main() if script is executed independently
if __name__ == "__main__":
    main()
