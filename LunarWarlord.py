from console import fg,bg,fx
from console.utils import cls
from console.printers import print
from random import randint
from random import seed
import os
import time
from datetime import date
import configparser
import errno
import csv

#COLOBLOCK COMPOSITION: [0]: name of colony. [1][0]: culture number. [1][1]: culture name. [2][0]: Colony Population. [2][1]: Colony Food. [2][2]:reactor fuel. [2][3]: Morale
#[2][4]: Colony Location X [2][5]: Colony Location Y [3]: enemy colonies, info stored as sub lists the same as main colony.
#[4]: Facilities List [5][x]: Intelligence Lists. [6][x]: Diplomacy Lists. [7][x]: productionlists [8]: Lunarday, [9]: Flagstring [10]: Save file

#FLAGSTRING: [0]: Reactor Shutdown in progress. [1] Rations (3 = full, 2= reduced, 1= minimal). [2]: Colony Starvation in progress(1,2,3)

def title(versionno): # the 'LUNAR WARLORD' title and version number
    print(bg.red,"""
    \t<b>LUNAR WARLORD         </b>""",fx.end)
    print('--------------')
    print(fg.red,fx.italic,"VERSION: " +str(versionno),fx.end)

def colotitle(coloblock):
    print(fg.red,str(coloblock[0].upper()),fx.end,end='')
    print(' | ',end='')
    print(fg.red,'Population: '+str(coloblock[2][0]),fx.end,end='')
    print(' | ',end='')
    print(fg.red,'Food: '+str(coloblock[2][1]),fx.end)
    print('--------------')

def newgame(versionno): # new game/savegame submenu
    newmenu = True
    while newmenu:
        bl()
        bl()
        print('1. Start New Game')
        print('2. Load Saved Game')
        bl()
        newgameinput = input('>: ')
        if newgameinput == '1':
            newgameflag = True
            bl()
            print('New Game Selected.')
            newmenu = False
        elif newgameinput == '2':
            newgameflag = False
            bl()
            print('Load Game Selected.')
            newmenu = False
        else:
            cls()
            title(versionno)
            error()
    time.sleep(1)
    return newgameflag

def diffpicker(versionno): #difficulty picker submenu
    diffpicking = True
    while diffpicking:
        bl()
        print('What difficulty would you like to play?')
        bl()
        print('1: Easy')
        print('2: Medium')
        print('3: Hard')
        bl()
        difinput = input('>: ')
        if difinput == '1':
            difficulty = 'easy'
            modifier = 12
            cls()
            title(versionno)
            bl()
            diffpicking = False
        elif difinput == '2':
            difficulty = 'medium'
            modifier = 9
            cls()
            title(versionno)
            bl()
            diffpicking = False
        elif difinput == '3':
            difficulty = 'hard'
            modifier = 6
            cls()
            title(versionno)
            bl()
            diffpicking = False
        else:
            cls()
            title(versionno)
            error()
    time.sleep(1)
    difflist = [difficulty,modifier]
    return difflist

def colonamer(cultlist):
    cultnum = cultlist[0]
    rulelist = []
    seed()
    with open ("Data/Names/COLORULES.txt", "r") as rulefile: # reads off the COLORULES file
        for line in rulefile:
            if line.startswith('###'):
                pass
            else:
                rulelist.append(line.strip('\n\r'))
    rulechoice = randint(0, len(rulelist) - 1)
    currentrule = rulelist[rulechoice]
    currentwords = currentrule.split()
    coloname = ''
    for w in range(len(currentwords)):
        currentreplacements = []
        if currentwords[w].isupper():
            with open('Data/Names/'+str(currentwords[w]) + ".txt", "r") as keyextract:
                for line in keyextract:
                    if line.startswith('###'):
                        pass
                    else:
                        if str(cultnum) in line or line[0] == '!': #checks cultural compatibility
                            line = line.split()
                            currentreplacements.append(line[-1].strip('\n\r'))
                        else:
                            pass
            replacementnum = randint(0, len(currentreplacements)-1)
            outputword = currentreplacements[replacementnum]
        else:
            outputword = currentwords[w]
        coloname = coloname + ' ' + outputword
    coloname = coloname[1:]
    return coloname

def colostats(modifier):
    seed()
    colonists = randint(18,40)+modifier
    foodstocks = randint(300,450)+(modifier*5)+31
    reactorstocks = randint(140,160)+(modifier*3)
    morale = randint(3,8)+(modifier//3)
    locationx = randint(1,1000)
    locationy = randint(1,1000)
    colostatlist = [colonists,foodstocks,reactorstocks,morale,locationx,locationy]
    return colostatlist

def othercols(colonamedef,modifier):
    seed()
    today = str(date.today())
    path = currentdir + '/Data/Saves/Save '
    increment = 0
    decrement = 3 - len(str(increment))
    padding = '0'*decrement
    nextpadding = '0'*(decrement-1)
    while os.path.exists((path) + (padding) + str(increment)) or os.path.exists((path) + (nextpadding) + str(increment)):
        increment += 1
    decrement = 3 - len(str(increment))
    padding = '0'*decrement
    increment = (padding)+str(increment)
    path = path+str(increment)
    try:
        os.makedirs(path)
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    enemynumber = randint(2,4)+(modifier//3)
    enemystatlist = []
    allnamelist = [colonamedef]
    while enemynumber > 0:
        workingenemystat = []
        cultlist = coloculter()
        coloname = colonamer(cultlist)
        colostatlist = colostats(modifier)
        workingenemystat = [coloname]
        workingenemystat.extend(cultlist)
        workingenemystat.extend(colostatlist)
        if coloname in allnamelist:
            pass
        else:
            enemystatlist.append(workingenemystat)
            allnamelist.append(coloname)
            enemynumber -= 1
    csv.register_dialect('enemies',delimiter=",", quoting=csv.QUOTE_NONE,escapechar='*') #creates a csv dialect that seperates files on commas
    path = currentdir + '/Data/Saves/Save ' + increment
    os.chdir(path)
    with open('enemies.csv', "w+", newline='') as enemiescsv:
        enemwriter = csv.writer(enemiescsv,dialect='enemies')
        for x in range (len(enemystatlist)):
            enemwriter.writerow(enemystatlist[x])
    os.chdir(currentdir)
    print(enemystatlist)
    enemystatlist =[enemystatlist,increment]
    return enemystatlist

def coloculter():
    seed()
    cultran = randint(1,7)
    if cultran == 1:
        colocult = 'European'
    elif cultran == 2:
        colocult = 'North American'
    elif cultran == 3:
        colocult = 'Asian'
    elif cultran == 4:
        colocult = 'Pacific'
    elif cultran == 5:
        colocult = 'African'
    elif cultran == 6:
        colocult = 'South American'
    elif cultran == 7:
        colocult = 'International'
    cultlist = [cultran,colocult]
    return cultlist

def colonistmaker(coloblock): # this routine makes individual colonists and saves them to csv file
    cultnum = coloblock[1][0]
    rulelist = []
    colonistlist = []
    for x in range (int(coloblock[2][0])):
        seed()
        gendernum = randint (1,4) #gets the gender
        if gendernum == 1:
            gender = 'M'
        elif gendernum == 2:
            gender = 'F'
        elif gendernum == 3:
            gender = 'X'
        elif gendernum == 4:
            gender = 'N'
        with open("Data/Names/NAMERULES"+str(gender)+".txt", "r") as rulefile:  # reads off the NAMERULES file
            for line in rulefile:
                if line.startswith('###'):
                    pass
                else:
                    rulelist.append(line.strip('\n\r'))
        rulechoice = randint(0, len(rulelist) - 1)
        currentrule = rulelist[rulechoice]
        currentwords = currentrule.split()
        newname = ''
        for w in range(len(currentwords)):
            currentreplacements = []
            if currentwords[w].isupper():
                with open('Data/Names/' + str(currentwords[w]) + ".txt", "r") as keyextract:
                    for line in keyextract:
                        if line.startswith('###'):
                            pass
                        else:
                            if str(cultnum) in line or line[0] == '!':  # checks cultural compatibility
                                line = line.split()
                                currentreplacements.append(line[-1].strip('\n\r'))
                            else:
                                pass
                print (currentrule,currentreplacements)
                replacementnum = randint(0, len(currentreplacements) - 1)
                outputword = currentreplacements[replacementnum]
            else:
                outputword = currentwords[w]
            newname = newname + ' ' + outputword
        newname = newname[1:]
        newage = randint(21,46)
        physical = randint(5,10)
        mental = randint(5,10)
        intellect = randint(5,10)
        creativity = randint(5,10)
        colonist = [newname,newage,gendernum,gender,physical,mental,intellect,creativity]
        print(colonist)
        colonistlist.append(colonist)
    csv.register_dialect('colonists',delimiter=",", quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates files on commas
    path = currentdir + '/Data/Saves/Save ' + str(coloblock[10])
    os.chdir(path)
    with open('colonists.csv', "w+", newline='') as colonistcsv:
        colwriter = csv.writer(colonistcsv,dialect='colonists')
        for x in range(len(colonistlist)):
            colwriter.writerow(colonistlist[x])
    os.chdir(currentdir)

def makegame(versionno, difficulty,modifier,currentdir): #this routine makes a new game
    cls()
    title(versionno)
    cultlist = coloculter()
    coloname = colonamer(cultlist)
    colostatlist = colostats(modifier)
    enemystatlist = othercols(coloname,modifier)
    enemystatlist,increment = enemystatlist[0],enemystatlist[1]
    print('Difficulty is '+str(difficulty)+'.')
    bl()
    bl()
    print(fg.green,'The year is 2078. The unthinkable has happened. You watch the fires of nuclear war blossom across the distant Earth.',fx.end)
    input()
    print(fg.green,'The radio channels carry only static and numbers stations, commanding the obliterated forces of a dead world.',fx.end)
    input()
    print(fg.green,'You are the current commander of the small lunar colony of '+str(coloname)+'. The colonists turn to your leadership.',fx.end)
    input()
    print(fg.green,'There are '+str(len(enemystatlist))+ ' other colonies on the lunar surface.',fx.end)
    input()
    print(fg.green,'If you fail your people, the airlock awaits.',fx.end)
    input()
    faclist = ['Reactor 1', 'Large Habitat 1', 'Oxygen Mine 1']
    lunarday = 1  # initialises time counter
    intlist = [[0, 'Nonexistent', '0', '0', '0', '0', '0']] * len(enemystatlist)  # initialises the intelligence scores for each enemy; pop, food, reactor, moralenum, morale
    diplist = [[0, 'Nonexistent']] * len(enemystatlist)  # initialises the diplomacy scores for each enemy
    prodlist = [0] * 6 #initialises the production list. 0: power, 1: oxygen, 2: food, 3: reactor fuel, 4: military materiel, 5: civilian materiel
    flagstring = '03000000000000000000'
    coloblock = [coloname, cultlist, colostatlist, enemystatlist, faclist, intlist, diplist, prodlist, lunarday,flagstring,increment]
    coloblock = savegame(coloblock,currentdir)
    time.sleep(1)
    return coloblock

def savegame(coloblock,currentdir):
    try:
        path = currentdir +'/Data/Saves/Save '+str(coloblock[10])
        os.chdir(path)
    except IndexError:
        today = str(date.today())
        path = currentdir + '/Data/Saves/Save '
        increment = 0
        decrement = 3 - len(str(increment))
        padding = '0'*decrement
        nextpadding = '0'*(decrement-1)
        while os.path.exists((path) + (padding) + str(increment)) or os.path.exists((path) + (nextpadding) + str(increment)):
            increment += 1
        decrement = 3 - len(str(increment))
        padding = '0'*decrement
        increment = (padding)+str(increment)
        path = path+str(increment)
        try:
            os.makedirs(path)
        except OSError as exc:  # handles the error if the directory already exists
            if exc.errno != errno.EEXIST:
                raise
            pass
        coloblock.append(increment)
        os.chdir(path)
    with open ('colonydata.txt',"w+") as colodat:
        colodat.write(str(coloblock[0])+'\n')
        colodat.write(str(coloblock[1][0])+'\n')
        colodat.write(str(coloblock[1][1])+'\n')
        colodat.write(str(coloblock[2][0])+'\n')
        colodat.write(str(coloblock[2][1])+'\n')
        colodat.write(str(coloblock[2][2])+'\n')
        colodat.write(str(coloblock[2][3])+'\n')
        colodat.write(str(coloblock[2][4])+'\n')
        colodat.write(str(coloblock[2][5])+'\n')
        colodat.write(str(len(coloblock[3]))+'\n')
        for x in range (len(coloblock[3])):
            colodat.write(str(coloblock[3][x][0])+'\n')
            colodat.write(str(coloblock[3][x][1])+'\n')
            colodat.write(str(coloblock[3][x][2])+'\n')
            colodat.write(str(coloblock[3][x][3])+'\n')
            colodat.write(str(coloblock[3][x][4])+'\n')
            colodat.write(str(coloblock[3][x][5])+'\n')
            colodat.write(str(coloblock[3][x][6])+'\n')
            colodat.write(str(coloblock[3][x][7])+'\n')
            colodat.write(str(coloblock[3][x][8])+'\n')
        colodat.write(str(len(coloblock[4]))+'\n')
        for y in range (len(coloblock[4])):
            colodat.write(str(coloblock[4][y])+'\n')
        for i in range (len(coloblock[5])):
            colodat.write(str(coloblock[5][x][0])+'\n')
            colodat.write(str(coloblock[5][x][1])+'\n')
            colodat.write(str(coloblock[5][x][2])+'\n')
            colodat.write(str(coloblock[5][x][3])+'\n')
            colodat.write(str(coloblock[5][x][4])+'\n')
            colodat.write(str(coloblock[5][x][5])+'\n')
            colodat.write(str(coloblock[5][x][6])+'\n')
        for j in range (len(coloblock[6])):
            colodat.write(str(coloblock[6][j][0])+'\n')
            colodat.write(str(coloblock[6][j][1])+'\n')
        colodat.write(str(coloblock[7][0]) + '\n')
        colodat.write(str(coloblock[7][1]) + '\n')
        colodat.write(str(coloblock[7][2]) + '\n')
        colodat.write(str(coloblock[7][3]) + '\n')
        colodat.write(str(coloblock[7][4]) + '\n')
        colodat.write(str(coloblock[7][5]) + '\n')
        colodat.write(str(coloblock[8]) + '\n')
        colodat.write(str(coloblock[9]) + '\n')
        colodat.write(str(coloblock[10]) + '\n')
    os.chdir(currentdir)
    return coloblock

def loadgame(currentdir):
    cls()
    title(versionno)
    bl()
    path = currentdir + '/Data/Saves'
    savelist = os.listdir(path)
    savelist.sort()
    for x in range(len(savelist)):
        print (str(x)+'. '+str(savelist[x]))
    bl()
    loadinput = input(">: ")
    sancheck = loadinput.isnumeric()
    if sancheck == True:
        try:
            decrement = 3 - len(str(loadinput))
            padding = '0' * decrement
            path = currentdir + '/Data/Saves/Save ' + padding + str(loadinput)
            os.chdir(path)
            coloblock = []
            with open('colonydata.txt', "r") as colodat:
                lineinput = colodat.readlines()
                for w in range (len(lineinput)):
                    lineinput[w] = lineinput[w].strip('\n')
                coloname = lineinput[0]
                cultlist = [lineinput[1],lineinput[2]]
                colostatlist =[int(lineinput[3]),int(lineinput[4]),int(lineinput[5]),int(lineinput[6]),int(lineinput[7]),int(lineinput[8])]
                enemynumber = int(lineinput[9])
                enemystatlist=[]
                for x in range (enemynumber):
                    mod = x*9
                    print(mod)
                    enemysublist = [str(lineinput[10+mod]),[int(lineinput[11+mod]),str(lineinput[12+mod])],[int(lineinput[13+mod]),int(lineinput[14+mod]),int(lineinput[15+mod]),int(lineinput[16+mod]),int(lineinput[17+mod]),int(lineinput[18+mod])]]
                    enemystatlist.append(enemysublist)
                print(enemystatlist)
                facnumber = int(lineinput[10+(enemynumber*9)])
                faclist = []
                for y in range (facnumber):
                    faclist.append(lineinput[10+(enemynumber*9)+y+1])
                print(faclist)
                intlist=[]
                for i in range (enemynumber):
                    mod = (i*7)+1
                    print(lineinput[10+(enemynumber*9)+facnumber+mod])
                    intsublist = [int(lineinput[10+(enemynumber*9)+facnumber+mod]),str(lineinput[11+(enemynumber*9)+facnumber+mod]),int(lineinput[12+(enemynumber*9)+facnumber+mod]),int(lineinput[13+(enemynumber*9)+facnumber+mod]),int(lineinput[14+(enemynumber*9)+facnumber+mod]),int(lineinput[15+(enemynumber*9)+facnumber+mod]),int(lineinput[16+(enemynumber*9)+facnumber+mod]),int(lineinput[17+(enemynumber*9)+facnumber+mod])]
                    intlist.append(intsublist)
                diplist=[]
                for j in range (enemynumber):
                    mod = j*2
                    dipsublist = [int(lineinput[10+(enemynumber*9)+(enemynumber*7)+mod]),str(lineinput[11+(enemynumber*9)+(enemynumber*7)+mod])]
                    diplist.append(dipsublist)
                prodlist=[int(lineinput[-9]),int(lineinput[-8]),int(lineinput[-7]),int(lineinput[-6]),int(lineinput[-5]),int(lineinput[-4])]
                lunarday = int(lineinput)[-3]
                flagstring = lineinput[-2]
                save = str(lineinput[-1])
                coloblock = [coloname, cultlist, colostatlist, enemystatlist, faclist, intlist, diplist, prodlist,
                             lunarday,flagstring,save]
        except IndexError:
            bl()
            error()
    return coloblock

def displayenemies(coloblock):
    enemylist = coloblock[3]
    enemylist2 = []
    csv.register_dialect('enemies', delimiter=",",quoting=csv.QUOTE_NONE)  # creates a csv dialect that seperates files on commas
    path = currentdir + '/Data/Saves/Save ' + str(coloblock[10])
    os.chdir(path)
    with open('enemies.csv', "w+", newline='') as enemiescsv:
        enemreader = csv.reader(enemiescsv, dialect='enemies')
        for row in enemreader:
            enemylist2.append(row)
    print(enemylist)
    print(enemylist2)
    intlist = coloblock[5]
    print(intlist)
    diplist = coloblock[6]
    bl()
    enemyloop = True
    while enemyloop:
        for x in range(len(enemylist)):
            print(str(x) + '. ' + str(enemylist[x][0]))
        enemyinfo = input('Further Information? >: ')
        sancheck = enemyinfo.isnumeric()
        if sancheck == True:
            try:
                enemyinfo = int(enemyinfo)
                bl()
                print ('Name: '+str(enemylist[enemyinfo][0]))
                print ('Location: LAT: '+str(enemylist[enemyinfo][7])+' LONG: '+str(enemylist[enemyinfo][8]))
                print ('Culture: '+str(enemylist[enemyinfo][2]))
                print ('Population: '+str(intlist[enemyinfo][3]))
                print ('Intelligence Level: '+str(intlist[enemyinfo][1]))
                print ('Diplomacy Level: '+str(diplist[enemyinfo][1]))
                print ('Food Reserves: '+str(intlist[enemyinfo][3]))
                print ('Reactor Reserves: '+str(intlist[enemyinfo][4]))
                print ('Morale: '+str(intlist[enemyinfo][6]))
                input()
            except IndexError:
                bl()
                error()
        else:
            enemyinfo = enemyinfo.upper()
            if enemyinfo == 'EXIT' or enemyinfo == 'X':
                enemyloop = False
        cls()
        colotitle(coloblock)
    time.sleep(1)

def bl():
    print('')

def error():
    print('Invalid command.')
    bl()

def calculator(coloblock):
    colotitle(coloblock)
    bl()
    print('Calculator function accessed')
    calculating = True
    calcoutput = 0
    while calculating:
        bl()
        calcinput = input('Enter Formula >:')
        calcinput = calcinput.upper()
        calcinput = calcinput.split()
        for x in range (len(calcinput)):
            if calcinput[x] == 'ANS':
                calcinput[x] = (calcoutput)
            if calcinput[x] == 'POP':
                calcinput[x] = int(coloblock[2][0])
        if calcinput[0] == 'EXIT':
            calculating = False
        else:
            try:
                if calcinput[1] == '+':
                    calcoutput = int(calcinput[0])+int(calcinput[2])
                elif calcinput[1] == '-':
                    calcoutput = int(calcinput[0])-int(calcinput[2])
                elif calcinput[1] == '/':
                    calcoutput = int(calcinput[0])/int(calcinput[2])
                elif calcinput[1] == '*':
                    calcoutput = int(calcinput[0])*int(calcinput[2])
                bl()
                print (calcoutput)
            except (ValueError,IndexError):
                    bl()
                    error()

def locationread(coloblock):
    print (str(coloblock[0])+' is located at lunar latitude '+str(coloblock[2][4])+', lunar longitude '+str(coloblock[2][5]))
    bl()
    input()

def dayset(coloblock):
    for x in range(len(coloblock[3])):#this for loop creates the estimates for each enemies supplies based on intelligence level
        if coloblock[5][x][0] <= 3:
            seed()
            errormargin = randint(-12,12)
            confidence = '(???)'
        elif coloblock[5][x][0] >= 4 and coloblock[5][x][0] <= 6:
            seed()
            errormargin = randint(-8,8)
            confidence = '(??)'
        elif coloblock[5][x][0] >=7 and coloblock[5][x][0] <= 9:
            seed()
            errormargin = randint(-4,4)
            confidence = '(?)'
        elif coloblock[5][x][0] == 10:
            errormargin = 0
            confidence = '(exact)'
        coloblock[5][x][2] = str(int(coloblock[3][x][3])+(errormargin))+' '+str(confidence)
        coloblock[5][x][3] = str(int(coloblock[3][x][4])+(errormargin*3))+' '+str(confidence)
        coloblock[5][x][4] = str(int(coloblock[3][x][5])+(errormargin*2))+' '+str(confidence)
        coloblock[5][x][5] = int(coloblock[3][x][6])+(errormargin//3)
        if coloblock[5][x][5] < 1:
            coloblock[5][x][6] = 'Very Poor '+str(confidence)
        if coloblock[5][x][5] >= 2 and coloblock[5][x][5] <= 3:
            coloblock[5][x][6] = 'Poor '+str(confidence)
        if coloblock[5][x][5] >= 4 and coloblock[5][x][5] <=6:
            coloblock[5][x][6] = 'Stable '+str(confidence)
        if coloblock[5][x][5] >=7 and coloblock[5][x][5] <= 9:
            coloblock[5][x][6] = 'Good '+str(confidence)
        if coloblock[5][x][5] >= 10:
            coloblock[5][x][6] = 'Excellent '+str(confidence)
    for y in range (len(coloblock[4])): # this for loop handles the energy production
        if coloblock[4][y] == 'Reactor 1' and coloblock[2][2] > 0:
            coloblock[7][0] = 8
        if coloblock[4][y] == 'Reactor 2' and coloblock[2][2] > 0:
            coloblock[7][0] = 12
    powerusage = 0
    oxytemp = 0
    for z in range (len(coloblock[4])):
        if coloblock[4][z] == 'Oxygen Mine 1':
            powerusage += 1
            oxytemp += 50
        if coloblock[4][z] == 'Large Habitat':
            powerusage += 3
            oxytemp -= 30
    if powerusage > coloblock[7][0]:
        print(fg.red,'Power usage exceeds power production!',fx.end)
        bl()
    else:
        coloblock[7][1] += oxytemp
    if coloblock[2][2] == 0:
        if coloblock[9][0] == '0':
            print(fg.red,'<b>REACTOR SHUTDOWN.</B> ~1 Lunar day\'s emergency power remaining',fx.end)
            coloblock[9][0] = '1'
            bl()
        else:
            gameover('reactor')
    if coloblock[2][1] <= 0:
        coloblock[2][1] = 0
        if str(coloblock[9][2]) == '1':
            print(fg.red,'<b>FOOD SUPPLIES ARE EXHAUSTED.</B> ~1 Lunar day\'s emergency rations remaining.',fx.end)
            coloblock[9][2] = str(int(coloblock[9][2]+1))
        elif str(coloblock[9][2]) == '2':
            print(fg.red,'<b>FOOD SUPPLIES ARE EXHAUSTED.</B> ~2 Lunar day\'s emergency rations remaining.',fx.end)
            coloblock[9][2] = str(int(coloblock[9][2]+1))
        elif str(coloblock[9][2]) == '3':
            gameover('starvation')
        else:
            print(fg.red,'<b>FOOD SUPPLIES ARE EXHAUSTED.</B> ~2 Lunar day\'s emergency rations remaining.',fx.end)
            coloblock[9][2] = str(int(coloblock[9][2]+1))
    return coloblock

def dayend(coloblock,currentdir):
    rations = int(coloblock[9][1])
    foodcon = coloblock[2][0]*rations
    coloblock[2][1]-=foodcon
    bl()
    print ('<b>Day End Report:</b>')
    print ('----------------------')
    print ('Your populace consumed '+str(foodcon)+' units of food.')
    print ('Your colony has a reserve of '+str(coloblock[7][1])+' units of oxygen.')
    coloblock[8] += 1
    input()
    coloblock = savegame(coloblock,currentdir)
    time.sleep(1)
    return coloblock

def gameover(overargument):
    mainloop = False
    pass

def colonistlist():
    csv.register_dialect('colonists',delimiter=",", quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates files on commas
    path = currentdir + '/Data/Saves/Save ' + str(coloblock[10])
    os.chdir(path)
    colonistloop = True
    while colonistloop:
        with open('colonists.csv', "r", newline='') as colonistcsv:
            colreader = csv.reader(colonistcsv,dialect='colonists')
            count = 1
            for row in colreader:
                print(str(count)+'. '+row[0])
                count += 1
        bl()
        colonistinfo = input('Further Information? >: ')
        colonistinfo = colonistinfo.upper()
        if colonistinfo == 'EXIT' or colonistinfo == 'X':
            colonistloop = False
    os.chdir(currentdir)

# STARTUP
currentdir = os.getcwd() # retrieves the current directory
config = configparser.ConfigParser()
configseg = 'DEFAULT'
config.read('Settings/config.ini')
versionno = config[(configseg)]['versionno']
cls()
title(versionno)
newgameflag = newgame(versionno)
if newgameflag == True:
    difflist = diffpicker(versionno)
    difficulty, modifier = difflist[0],difflist[1]
    coloblock = makegame(versionno, difficulty, modifier,currentdir)
    colonistmaker(coloblock)
elif newgameflag == False:
    coloblock = loadgame(currentdir)
mainloop = True
cls()
while mainloop: # main loop
    coloblock = dayset(coloblock)
    colotitle(coloblock)
    bl()
    print('Greetings commander. It is day '+str(coloblock[8])+' of your command. The colony awaits your instructions.')
    bl()
    mainprompt = input('>: ')
    bl()
    mainprompt = mainprompt.upper()
    if mainprompt == 'ENEMIES' or mainprompt == 'OTHER COLONIES':
        displayenemies(coloblock)
    elif mainprompt == 'COLONISTS' or mainprompt == 'POP':
        colonistlist()
    elif mainprompt == 'CALC' or mainprompt == 'CALCULATOR':
        calculator(coloblock)
    elif mainprompt == 'LOCATION':
        locationread(coloblock)
    elif mainprompt == 'SAVE':
        coloblock = savegame(coloblock, currentdir)
    elif mainprompt == 'END':
        coloblock = dayend(coloblock,currentdir)
    else:
        bl()
        error()