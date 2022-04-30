from asyncore import write
import pandas as pd
from pandas.core.dtypes import dtypes
from random import choice, randint, shuffle, sample, choices
from datetime import datetime as dt

ENTERKEY = [10,459]
BACKSPACE = 8
ESC = 27
DELETE = 330

def getItemDict():
    itemsDf = pd.read_csv('mFiles\items.csv', names=['Number','Object'])
    importDict = pd.DataFrame.to_dict(itemsDf,'split')
    dictList = importDict['data']
    itemsDict = {}
    for k,v in dictList:
        itemsDict[k]=v

    return itemsDict

def importObjectList():
    itemsDf = pd.read_csv("mFiles\createAndMemorizeList.txt", names = ['Objects'])
    objects = itemsDf.Objects.to_list()
    return objects

def getObjects():
    objectList = []
    fileList = ['mFiles/most-common-nouns-english.txt','mFiles/nounlist.txt']

    for filename in fileList:
        with open(filename,'r') as objectFile:
            for line in objectFile:
                objectList.append(line)
    
    objectList = list(set(objectList))
    shuffle(objectList)
    return objectList

def printMenu(curses, stdscr, printError):
    stdscr.clear()
    stdscr.addstr('MENU\n\n')
    stdscr.addstr("1) List Memory Objects\n")
    stdscr.addstr("2) Practice Numbers\n")
    stdscr.addstr("3) Practice Memory Objects\n")
    stdscr.addstr("4) Match object to number\n")
    stdscr.addstr("5) Match number to object\n")
    stdscr.addstr("6) List Objects\n")
    stdscr.addstr("7) Memorize List\n")
    if printError:
        errorMessage(curses, stdscr , endnum=7) #endnum is the number of menu items
    stdscr.addstr('\n'*3)

def getduration(startTime):
    now = dt.now()
    duration = now-startTime
    minutes = duration.seconds//60
    seconds = duration.seconds%60
    return {'minutes':minutes,
            'seconds': seconds}

def wrapItUp(curses,stdscr,hit,miss):
    stdscr.clear()
    stdscr.addstr("Final Score:\n")
    stdscr.addstr(f"Hits: {hit}\n")
    stdscr.addstr(f"Misses: {miss}\n")
    stdscr.addstr(f"{round((hit/(hit+miss))*100,1)}%\n\n")
    stdscr.addstr("Press any key to continue")

    stdscr.getkey()    

def getGuess(y,x,curses, stdscr):
    keypress = 0
    currentGuess = ''
    stdscr.addstr(y,x,'')
    while True:
        keypress = stdscr.getch()
        if keypress in ENTERKEY:
            break
        elif keypress==BACKSPACE:
            stdscr.addch(keypress)
            stdscr.addstr(' ')
            stdscr.addch(keypress)
            currentGuess = currentGuess[:-1]
        elif keypress == ESC:
            currentGuess = -1
            break
        else:
            stdscr.addch(keypress)
            currentGuess += chr(keypress)
    currentGuess = currentGuess.strip()
    return currentGuess

def practiceObjectList(curses, stdscr, NUMSDICT):
    stdscr.clear()
    startTime = dt.now()
    score = 0
    stdscr.addstr('Type objects in order:\n')
    for key, value in NUMSDICT.items():
        
        stdscr.addstr(str(key))
        y = stdscr.getyx()[0]
        stdscr.addstr(y, 3, '')
        currentGuess = getGuess(y,0,curses, stdscr)
        if currentGuess == -1: break
        currentGuess = currentGuess.strip()
        if currentGuess.upper() == value.upper():
            y = stdscr.getyx()[0]
            stdscr.addstr(y, 0, currentGuess + '\n', curses.color_pair(1))
            score += 1
        else:
            stdscr.addstr(y, 0, currentGuess, curses.color_pair(2))
            stdscr.addstr(y, 30, value + '\n')

    duration = getduration(startTime)   
    stdscr.addstr(f'\nYour score is {score}\n')
    stdscr.addstr(f"Your time was {duration['minutes']} minutes and {duration['seconds']} seconds.")
    stdscr.getkey()

def errorMessage(curses, stdscr, endnum):
    stdscr.addstr('\n'*4 + f"Must be a number between 1 and {endnum}.",curses.color_pair(2))
    stdscr.getkey()

def inputNumber(curses, stdscr,question):
    loopRangeSTR = ''
    acceptableKeys = [x for x in range(48,58)]
    acceptableKeys.append(BACKSPACE)
    stdscr.addstr(question)
    while loopRangeSTR == '':
        keypress = 0
        while keypress not in ENTERKEY:
            keypress = stdscr.getch()
            if keypress in acceptableKeys:
                stdscr.addch(keypress)
                if keypress == BACKSPACE:
                    stdscr.addstr(' ')
                    stdscr.addch(keypress)
                    loopRangeSTR = loopRangeSTR[:-1]
                else:
                    loopRangeSTR += chr(keypress)
    stdscr.clear()
    return int(loopRangeSTR)

def getIntegerDict(number):
    return  {'str':str(number),'int':number}

def updateScore(y,x,score,length,curses,stdscr):
    score = str(score)
    while len(score) < length:
        score = ' ' + score
    stdscr.addstr(y,x,score)

def getRandomItem(weights,numOfItems):
    numbers = [x for x in range(1,numOfItems+1)]
    return choices(numbers,weights=weights)[0]

def gameSetup(curses,stdscr, numOfItems):
    stdscr.clear()
    weights = [5 for x in range(1,numOfItems+1)]
    loopRange = inputNumber(curses,stdscr,"How high would you like to go?\n\n")
    hit,miss = 0,0
    return [weights,loopRange,hit,miss]

def memoryNumbers(curses, stdscr, NUMSDICT):
    weights,loopRange,hit,miss = gameSetup(curses,stdscr,len(NUMSDICT))
    stdscr.addstr(0,0,"Type the object associated with the number:")
    stdscr.addstr(1,0,"Hits:  0 Misses:  0")
    numOfItems = len(NUMSDICT)

    for number in range(loopRange):
        integer = getIntegerDict(getRandomItem(weights,numOfItems))
        stdscr.addstr(3,0,integer['str']+'\n')
        stdscr.addstr(4,0,' ' * 30)
        currentGuess = getGuess(4,0,curses,stdscr)
        if currentGuess == -1: break

        if currentGuess.upper() == NUMSDICT[integer['int']].upper():
            hit += 1
            updateScore(1,5,hit,3,curses,stdscr)
        else:
            miss +=1
            updateScore(1,16,miss,3,curses,stdscr)
            weights[integer['int']-1] += 1

    wrapItUp(curses,stdscr,hit,miss)



def memoryObjects(curses, stdscr, NUMSDICT):
    weights,loopRange,hit,miss = gameSetup(curses,stdscr,len(NUMSDICT))
    stdscr.addstr(0,0,"Type the number associated with the object:")
    stdscr.addstr(1,0,"Hits:  0 Misses:  0")    
    numOfItems = len(NUMSDICT)

    for number in range(loopRange):
        integer = getIntegerDict(getRandomItem(weights,numOfItems))
        stdscr.addstr(3,0, NUMSDICT[integer['int']]+'\n')
        stdscr.addstr(4,0,' ' * 30)
        currentGuess = getGuess(4,0,curses,stdscr)
        if currentGuess == -1: break

        if int(currentGuess.strip()) == integer['int']:
            hit += 1
            updateScore(1,5,hit,3,curses,stdscr)
        else:
            miss +=1
            updateScore(1,16,miss,3,curses,stdscr)
            weights[integer['int']-1] += 1

    wrapItUp(curses,stdscr,hit,miss)


def randomObjects(curses,stdscr,OBJECTLIST, objects = []):
    weights,loopRange,hit,miss = gameSetup(curses,stdscr,len(OBJECTLIST))
    if objects == []:
        numOfObjects = inputNumber(curses,stdscr,"How many Objects would you like?\n")
        objects = sample(OBJECTLIST,numOfObjects)
    objects = [x.strip() for x in objects]
    stdscr.addstr("Memorize this list. Take as long as you need.")
    stdscr.addstr(5,0,"Press any key to continue")
    for index,object in enumerate(objects,1):
        stdscr.addstr(2,0,str(index))
        stdscr.addstr(3,0," " * 30)
        stdscr.addstr(3,0,object)
        keypress = stdscr.getch()
        if keypress == DELETE:
            objects = replaceObject(curses, stdscr, object, objects, 3)
    stdscr.clear()
    stdscr.addstr("What item is in each location")
    stdscr.addstr(1,0,"Hits:  0 Misses:  0")  

    sampleObjects = getSampleObjects(loopRange,objects)

    for item in sampleObjects:
        listNumber = objects.index(item) + 1
        stdscr.addstr(3,0,'  ')
        stdscr.addstr(3,0,str(listNumber))
        stdscr.addstr(4,0,' ' * 30)
        currentGuess = getGuess(4,0,curses,stdscr)
        if currentGuess == -1: break

        if currentGuess.upper() == item.upper():
            hit += 1
            updateScore(1,5,hit,3,curses,stdscr)
        else:
            miss +=1
            updateScore(1,16,miss,3,curses,stdscr)
            stdscr.addstr(4,40,item)
            stdscr.getch()
            stdscr.addstr(4,40,' ' * 25)

    wrapItUp(curses,stdscr,hit,miss)

def randomNumbers(curses,stdscr,OBJECTLIST,objects = []):
    weights,loopRange,hit,miss = gameSetup(curses,stdscr,len(OBJECTLIST))
    if objects == []:
        numOfObjects = inputNumber(curses,stdscr,"How many Objects would you like?\n")
        objects = sample(OBJECTLIST,numOfObjects)
    objects = [x.strip() for x in objects]
    stdscr.addstr("Memorize this list. Take as long as you need.")
    stdscr.addstr(5,0,"Press any key to continue")
    for index,object in enumerate(objects,1):
        stdscr.addstr(2,0,str(index))
        stdscr.addstr(3,0," " * 30)
        stdscr.addstr(3,0,object)
        stdscr.getch()
    
    stdscr.clear()
    stdscr.addstr("What index is each object located at?")
    stdscr.addstr(1,0,"Hits:  0 Misses:  0")  

    while len(weights) > numOfObjects:
        weights.pop()

    sampleObjects = getSampleObjects(loopRange,objects)

    for item in sampleObjects:
        listNumber = objects.index(item) + 1
        stdscr.addstr(3,0,'  ' * 10)
        stdscr.addstr(3,0,item)
        stdscr.addstr(4,0,' ' * 30)
        currentGuess = getGuess(4,0,curses,stdscr)
        if currentGuess == -1: break

        if int(currentGuess) == listNumber:
            hit += 1
            updateScore(1,5,hit,3,curses,stdscr)
        else:
            miss +=1
            updateScore(1,16,miss,3,curses,stdscr)
            stdscr.addstr(4,40,str(listNumber))
            stdscr.getch()
            stdscr.addstr(4,40,' ' * 25)

    wrapItUp(curses,stdscr,hit,miss)

def listObjects(curses, stdscr, OBJECTLIST):
    stdscr.clear()
    numOfObjects = inputNumber(curses,stdscr,"How many Objects would you like?\n")
    objects = sample(OBJECTLIST,numOfObjects)
    objects = [x.strip() for x in objects]
    stdscr.addstr("Memorize this list. Take as long as you need.")
    stdscr.addstr(5,0,"Press any key to continue")
    for index,object in enumerate(objects,1):
        stdscr.addstr(2,0,str(index))
        stdscr.addstr(3,0," " * 30)
        stdscr.addstr(3,0,object)
        stdscr.getch()
    
    startTime = dt.now()
    score = 0
    stdscr.clear()
    stdscr.addstr('Type objects in order:\n')
    for index, object in enumerate(objects,1):
        
        stdscr.addstr(str(index))
        y = stdscr.getyx()[0]
        stdscr.addstr(y, 3, '')
        currentGuess = getGuess(y,3,curses, stdscr)
        if currentGuess == -1: break
        currentGuess = currentGuess.strip()
        if currentGuess.upper() == object.upper():
            y = stdscr.getyx()[0]
            stdscr.addstr(y, 0, currentGuess + '\n', curses.color_pair(1))
            score += 1
        else:
            stdscr.addstr(y, 0, currentGuess, curses.color_pair(2))
            stdscr.addstr('  ' + object + '\n')
    duration = getduration(startTime)   
    stdscr.addstr(f'\nYour score is {score}\n')
    stdscr.addstr(f"Your time was {duration['minutes']} minutes and {duration['seconds']} seconds.")
    stdscr.getkey()

def createAndMemorizeList(curses,stdscr):
    index = 0
    objects = []
    currentGuess = ''
    stdscr.clear()
    options = ["Create List","Import List"]
    printError = False
    optionSelected = False

    while not optionSelected:
        optionsMenu(curses,stdscr,options,printError)
        keypress = stdscr.getch()
        option = keypress - 48
        if (option < 1 or option > len(options)):
            printError = True
        else:
            printError = False
            optionSelected = True

    if option == 1:
        stdscr.addstr("Create your list:\n\n")
        
        while currentGuess == '':
            index += 1
            stdscr.addstr(str(index) + ' ')
            y,x = stdscr.getyx()
            item = getGuess(y,3,curses, stdscr)
            if item != '':
                objects.append(item.strip())
                stdscr.addstr('\n')
            else:
                break
    if option == 2:
        objects = importObjectList()
        stdscr.clear()
        stdscr.addstr("Memorize this list. Take as long as you need.")
        stdscr.addstr(5,0,"Press any key to continue")
        for index,object in enumerate(objects,1):
            stdscr.addstr(2,0,str(index))
            stdscr.addstr(3,0," " * 30)
            stdscr.addstr(3,0,object)
            stdscr.getch()
            
    stdscr.clear()
    stdscr.addstr('Type objects in order:\n')

    for index, object in enumerate(objects,1):
        
        stdscr.addstr(str(index))
        y = stdscr.getyx()[0]
        stdscr.addstr(y, 3, '')
        currentGuess = getGuess(y,3,curses, stdscr)
        if currentGuess == -1: break
        currentGuess = currentGuess.strip()
        if currentGuess.upper() == object.upper():
            y = stdscr.getyx()[0]
            stdscr.addstr(y, 0, currentGuess + '\n', curses.color_pair(1))
        else:
            stdscr.addstr(y, 0, currentGuess, curses.color_pair(2))
            stdscr.addstr('  ' + object + '\n')

    stdscr.addstr("Press any key to continue")
    stdscr.getkey()

    stdscr.clear()
    randomObjects(curses,stdscr,[],objects = objects)


def getSampleObjects(loopRange,objects):
    lenObj = len(objects)
    loops = loopRange//lenObj
    spares = loopRange%lenObj
    sampleObjects = []
    for i in range(loops):
        sampleObjects.extend(sample(objects,lenObj))
    sampleObjects.extend(sample(objects,spares))
    return sampleObjects

def optionsMenu(curses,stdscr,options,printError):
    stdscr.clear()
    stdscr.addstr('Would you like to:\n\n')

    for index,option in enumerate(options,1):
        optionIndex = str(index) + ') '
        optionSTR = optionIndex + option +'\n'
        stdscr.addstr(optionSTR)

    if printError:
        errorMessage(curses, stdscr , endnum=index) #endnum is the number of menu items
    stdscr.addstr('\n'*3)

def getKeyNum():
    import curses
    from curses import wrapper

    def main(stdscr):
        x = stdscr.getch()
        print(x)

    wrapper(main)

def replaceObject(curses, stdscr, object, objects, xline):
    objectLists = [[],[]]
    fileList = ['mFiles/most-common-nouns-english.txt','mFiles/nounlist.txt']

    for i,filename in enumerate(fileList):
        with open(filename,'r') as objectFile:
            for line in objectFile:
                objectLists[i].append(line)
    
    for i,filename in enumerate(fileList):
        with open(filename,'w') as objectFile:
            for line in objectLists[i]:
                if line.strip('\n') != object:
                    objectFile.write(line)

    replacementObjects = getObjects()
    i=0
    while replacementObjects[i].strip() in objects:
        i+=1

    objects[objects.index(object)]=replacementObjects[i].strip()
    stdscr.addstr(xline,0," " * 30)
    stdscr.addstr(xline,0,replacementObjects[i])
    keypress = stdscr.getch()
    if keypress == DELETE:
        objects = replaceObject(curses, stdscr, replacementObjects[i].strip(), objects, xline)
    return objects
                    