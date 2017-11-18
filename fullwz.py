import re, sys, os.path
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
        print("Usage: python " + sys.argv[0] + " <path/to/file>")
        exit(2)

    filename  = sys.argv[1]

    hwStrings = findHomeworkStrings(filename)
    todos     = getTODOSFromString(hwStrings)
    print("TODOs: ", todos)

    # append the homework to wz with the dictionary
    pathToScripts = {
        "1": "info3/ein.tex",
        "2": "info3/grund.tex",
        "3": "info3/sort.tex",
        "4": "info3/model.tex",
        "5": "info3/einfach.tex",
        "6": "info3/prio.tex",
        "7": "info3/bal.tex",
        "8": "info3/hash.tex",
        "9": "info3/union.tex",
        "10": "info3/dfs.tex",
        "11": "info3/kurz.tex"
    }
    addContentFromScript(filename, todos, pathToScripts)
    return 0

"""
find input file for a string which tells the weekly homework
@param  {string} filename
@return {list} result homework strings
"""
def findHomeworkStrings(filename):
    wz        = open(filename, "r")
    result = []
    temp = []

    # first check for strings that MIGHT be homeworks
    for line in wz.readlines():
        if LIBRARY.isLatexComment(line):
            continue
        elif LIBRARY.maybeHomeworks(line):
            temp.append(line)
    wz.close()

    # remove things that are not homeworks
    nogarbage = LIBRARY.removeGarbage(temp)
    if nogarbage[0]:
        temp = nogarbage[0]
    if nogarbage[1]:
        print("Date removed: ", nogarbage[1])
    if nogarbage[2]:
        print("Time removed: ", nogarbage[2])

    # keep only strings that MIGHT be homeworks
    # after garbage removal surely they'll be homeworks
    for string in temp:
        if LIBRARY.maybeHomeworks(string):
            result.append(string)

    # report & return
    if len(result):
        return result
    else:
        return None
"""
format the string into a list of homeworks
@param {list} hwStrings that contain homeworks
@return {dictionary} hwDicts
currently print the first passed in argument
"""
def getTODOSFromString(hwStrings):
    result = {}

    for hwString in hwStrings:
        # identifies homeworks, also expand range of homeworks
        # e.g. 3.3-3.6 will be expanded to {"3": [3, 4, 5, 6]}
        tokenized   = LIBRARY.tokenizeHomework(hwString)
        # check every key in tokenized
        # to prevent duplication, append only new items to result
        for key in tokenized:
            if key not in result:
                result[key] = tokenized[key]
            if key in result:
                for item in tokenized[key]:
                    if item not in result[key]:
                        result[key].append(item)
    return result
"""
find & extract from script & append to filename
@param {string} filename
@param {dictionary} todos with key=chapter and value=individual homeworks
@param {dictionary} pathToScripts
@return {list} result homework strings
"""
def addContentFromScript(filename, todos, pathToScripts):
    wz = open(filename, "a")
    wz.write("\n")
    wz.write("\\newpage\n")
    wz.write("\\begin{Tproblemsection}\n")
    wz.write("\\renewcommand{\label}[1]{\\ignorespaces}\n")
    wz.write("\\noindent{\\bf Auszug aus dem Skript:}\n")

    for chapter in todos:
        allHomeWorks = LIBRARY.getHWFromScript(pathToScripts[chapter]);

        # move to next chapter if nothing found
        if allHomeWorks["total"] == 0 :
            print("Nothing found in " + pathToScripts[chapter])
            continue

        for hwID in todos[chapter]:
            if not allHomeWorks.get(hwID):
                print(str(chapter) + "." + str(hwID) + " Not Found")
                continue
            else :
                for line in allHomeWorks[hwID]:
                    wz.write(line)


    wz.write("\\end{Tproblemsection}\n")
    wz.close()
    print(filename + " done!")
    return

if __name__ == "__main__":
    main()
    # for i in range(1,15):
    #     filename  = "wz"+str(i)+".tex"
    #     hwStrings = findHomeworkStrings(filename)
    #     print(hwStrings)
