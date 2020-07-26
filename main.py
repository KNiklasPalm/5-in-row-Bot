import pygame
import random
import time

class BordController:
    def __init__(self):
        self.slots = []
        self.freeSlots = {}
        self.playerRedSlots = {}
        self.playerBlueSlots = {}
        

        #Create Board
        lenXY = 25
        counter = 0
        for x in range(lenXY):
            row = []
            for y in range(lenXY):
                counter += 1
                newSlot = Slot([x,y],counter)
                row.append(newSlot)
                self.freeSlots[newSlot.Id] = newSlot
            self.slots.append(row)
        pygame.display.update()

    def setPlayer(self,indexX,indexY,player):
        tempSlot = self.slots[indexX][indexY]
        tempSlot.Player = player
        
        if player == "Red":
            self.playerRedSlots[tempSlot.Id] = tempSlot
            del self.freeSlots[tempSlot.Id]
        elif player == "Blue":
            self.playerBlueSlots[tempSlot.Id] = tempSlot
            del self.freeSlots[tempSlot.Id]
        elif player == "None":
            self.freeSlots[tempSlot.Id] = tempSlot
            try:
                del self.playerRedSlots[tempSlot.Id]
            except:
                pass
            try:
                del self.playerBlueSlots[tempSlot.Id]
            except:
                pass
        
        tempSlot.setPlayer(player)

class Slot:
    def __init__(self, index, id):
        self.Player = "None"
        self.Index = index
        self.Id = id
        self.rect = pygame.draw.rect(screen, (resXY/30,resXY/30,resXY/30),[resXY/30 * (1 + self.Index[0]),resXY/30 * (1 + self.Index[1]),resXY/50,resXY/50], False)
        self.minXY = [resXY/30 * (1 + self.Index[0]),resXY/30 * (1 + self.Index[1])]
        self.maxXY = [self.minXY[0] + resXY/30,self.minXY[1] + resXY/30]
        self.offValue = 0
        self.deffValue = 0

    def setPlayer(self,player):
        if player == "Red":
            self.rect = pygame.draw.rect(screen, (255,0,0),[resXY/30 * (1 + self.Index[0]),resXY/30 * (1 + self.Index[1]),resXY/50,resXY/50], False)
        elif player == "Blue":
            self.rect = pygame.draw.rect(screen, (0,0,255),[resXY/30 * (1 + self.Index[0]),resXY/30 * (1 + self.Index[1]),resXY/50,resXY/50], False)
        elif player == "None":
            self.rect = pygame.draw.rect(screen, (resXY/30,resXY/30,resXY/30),[resXY/30 * (1 + self.Index[0]),resXY/30 * (1 + self.Index[1]),resXY/50,resXY/50], False)
        pygame.display.update()

    def displayWinner(self):
        self.rect = pygame.draw.rect(screen, (255, 255, 0),[resXY / 30 * (1 + self.Index[0]), resXY / 30 * (1 + self.Index[1]), resXY / 50,resXY / 50], False)
        pygame.display.update()

def init():
    global screen, resXY

    #Screen
    resXY = 600
    pygame.display.set_caption("Tic Tac Toe")
    screen = pygame.display.set_mode((resXY, resXY))
    screen.fill((255,255,255))
    pygame.display.update()

    #Mouse
    pygame.mouse.set_visible(1)

def checkWin(slot):
    slotX = slot.Index[0]
    slotY = slot.Index[1]
    player = slot.Player

    directions = [[1,0],[0,1],[1,1],[1,-1]]

    for dirr in directions:
        found = 0
        winningSlots = [slot]
        xMulti = dirr[0]
        yMulti = dirr[1]
        for i in range(1,5):
            try:
                if (slotX + (i*xMulti)) < 0 or (slotY + (i*yMulti)) < 0:
                    continue 
                checkSlot = controller.slots[slotX + (i*xMulti)][slotY + (i*yMulti)]
                if checkSlot.Player == player:
                    found +=1
                    winningSlots.append(checkSlot)
                else:
                    break
            except:
                break
        for i in range(1,(5-found)):
            try:
                if (slotX - (i*xMulti)) < 0 or (slotY - (i*yMulti)) < 0:
                    continue 
                checkSlot = controller.slots[slotX - (i*xMulti)][slotY - (i*yMulti)]
                if checkSlot.Player == player:
                    found +=1
                    winningSlots.append(checkSlot)
                else:
                    break
            except:
                break
        if found == 4:
            print("Winner: ", player)

            for tempSlot in winningSlots:
                tempSlot.displayWinner()

            time.sleep(6)

            for slotRow in controller.slots:
                for slot in slotRow:
                    controller.setPlayer(slot.Index[0],slot.Index[1],"None")
            break

def selectSlot(color):
    me = color
    if me == "Red":
        you = "Blue"
        mySlots = controller.playerRedSlots
        yourSlots = controller.playerBlueSlots
    else:
        you = "Red"
        mySlots = controller.playerBlueSlots
        yourSlots = controller.playerRedSlots


    potentialOff = []
    potentialDeff = []

    #Set vaues to 0 
    for slotIndex in controller.freeSlots:
        slot = controller.freeSlots[slotIndex]
        slot.deffValue = 0
        slot.offValue = 0

    #OFFENSIVE loop through all ownslots
    for slotIndex in mySlots:
        slot = mySlots[slotIndex]
        slotX = slot.Index[0]
        slotY = slot.Index[1]

        #UpdateValues
        directions = [[1,0],[0,1],[1,1],[1,-1]]
        dirLR = [1, -1]
        for dirr in directions:
            xMulti = dirr[0]
            yMulti = dirr[1]

            rightSlots = []
            rightFound = 0
            leftSlots = []
            leftFound = 0

            #Right
            for lr in dirLR:
                inRowFound = 0
                dirrFound = 0
                dirrSlot = []

                for i in range(1,5):
                    try:
                        if (slotX + lr*(i*xMulti)) < 0 or (slotY + lr*(i*yMulti)) < 0:
                            break
                        tempSlot = controller.slots[slotX + lr*(i*xMulti)][slotY + lr*(i*yMulti)]
                        if tempSlot.Player != you:
                            dirrSlot.append(tempSlot)
                            dirrFound += 1
                        else:
                            break
                        if tempSlot.Player == me:
                            inRowFound += 1
                    except:
                        break

                #Four in Row Right
                if inRowFound >= 3 and dirrFound == 4:
                    for i in range(1,5):
                        tempSlot = controller.slots[slotX + lr*(i*xMulti)][slotY + lr*(i*yMulti)]
                        if tempSlot.Player == "None":
                            return (tempSlot)

                #Three in row and freeslot
                foundInThree = 0
                selected = "None"
                if (slotX - lr*(1*xMulti)) <= 24 and (slotY - lr*(1*yMulti)) <= 24:
                    if inRowFound >= 2 and dirrFound >= 4 and controller.slots[slotX - lr*(1*xMulti)][slotY - lr*(1*yMulti)].Player == "None":
                        for i in range(1,4):
                            tempSlot = controller.slots[slotX + lr*(i*xMulti)][slotY + lr*(i*yMulti)]
                            if tempSlot.Player == "None":
                                selected = tempSlot
                            elif tempSlot.Player == me:
                                foundInThree += 1
                    if foundInThree == 2 and selected != "None":
                        potentialOff.append(selected)

                if lr == 1:
                    rightSlots = dirrSlot
                    rightFound = dirrFound
                else:
                    leftSlots = dirrSlot
                    leftFound = dirrFound


            #setValues
            try:
                rightSlots[0].offValue += 1 + min(leftFound,3) - (4-rightFound)
            except:
                pass
            try:
                rightSlots[1].offValue += 1 + min(leftFound,2) - (4-rightFound)
            except:
                pass
            try:
                rightSlots[2].offValue += 1 + min(leftFound,1) - (4-rightFound)
            except:
                pass
            try:
                rightSlots[3].offValue += 1
            except:
                pass
            
            try:
                leftSlots[0].offValue += 1 + min(rightFound,3) - (4-leftFound)
            except:
                pass
            try:
                leftSlots[1].offValue += 1 + min(rightFound,2) - (4-leftFound)
            except:
                pass 
            try:
                leftSlots[2].offValue += 1 + min(rightFound,1) - (4-leftFound)
            except:
                pass
            try:
                leftSlots[3].offValue += 1
            except:
                pass
    
    #DEFENSIVE loop throgh all your slots
    for slotIndex in yourSlots:
        slot = yourSlots[slotIndex]
        slotX = slot.Index[0]
        slotY = slot.Index[1]

        #UpdateValues
        directions = [[1,0],[0,1],[1,1],[1,-1]]
        dirLR = [1, -1]
        for dirr in directions:
            xMulti = dirr[0]
            yMulti = dirr[1]

            rightSlots = []
            rightFound = 0
            leftSlots = []
            leftFound = 0

            #Right
            for lr in dirLR:
                inRowFound = 0
                dirrFound = 0
                dirrSlot = []

                for i in range(1,5):
                    try:
                        if (slotX + lr*(i*xMulti)) < 0 or (slotY + lr*(i*yMulti)) < 0:
                            break
                        tempSlot = controller.slots[slotX + lr*(i*xMulti)][slotY + lr*(i*yMulti)]
                        if tempSlot.Player != me:
                            dirrSlot.append(tempSlot)
                            dirrFound += 1
                        else:
                            break
                        if tempSlot.Player == you:
                            inRowFound += 1
                    except:
                        break

                #Four in Row Right
                if inRowFound >= 3 and dirrFound == 4:
                    for i in range(1,5):
                        tempSlot = controller.slots[slotX + lr*(i*xMulti)][slotY + lr*(i*yMulti)]
                        if tempSlot.Player == "None":
                            return (tempSlot)

                #Three in row and freeslot
                foundInThree = 0
                selected = "None"
                if (slotX - lr*(1*xMulti)) <= 24 and (slotY - lr*(1*yMulti)) <= 24:
                    if inRowFound >= 2 and dirrFound >= 4 and controller.slots[slotX - lr*(1*xMulti)][slotY - lr*(1*yMulti)].Player == "None": #KOLLA Vänstersida
                        for i in range(1,4):
                            tempSlot = controller.slots[slotX + lr*(i*xMulti)][slotY + lr*(i*yMulti)]
                            if tempSlot.Player == "None":
                                selected = tempSlot
                            elif tempSlot.Player == you:
                                foundInThree += 1
                    if foundInThree == 2 and selected != "None":
                        potentialDeff.append(selected)

                if lr == 1:
                    rightSlots = dirrSlot
                    rightFound = dirrFound
                else:
                    leftSlots = dirrSlot
                    leftFound = dirrFound

            #setValues
            try:
                rightSlots[0].offValue += 1 + min(leftFound,3) - (4-rightFound)
            except:
                pass
            try:
                rightSlots[1].offValue += 1 + min(leftFound,2) - (4-rightFound)
            except:
                pass
            try:
                rightSlots[2].offValue += 1 + min(leftFound,1) - (4-rightFound)
            except:
                pass
            try:
                rightSlots[3].offValue += 1
            except:
                pass
            
            try:
                leftSlots[0].offValue += 1 + min(rightFound,3) - (4-leftFound)
            except:
                pass
            try:
                leftSlots[1].offValue += 1 + min(rightFound,2) - (4-leftFound)
            except:
                pass 
            try:
                leftSlots[2].offValue += 1 + min(rightFound,1) - (4-leftFound)
            except:
                pass
            try:
                leftSlots[3].offValue += 1
            except:
                pass

    # find slot
    selected = []
    selectedValue = 0
    if len(potentialDeff) != 0:
        for slot in potentialDeff:
            if slot.offValue >= selectedValue:
                selected = slot
                selectedValue = slot.offValue
        return (selected)

    if len(potentialOff) != 0:
        for slot in potentialOff:
            if slot.offValue >= selectedValue:
                selected = slot
                selectedValue = slot.offValue
        return (selected)

    #Find possible area
    minX = 99
    maxX = 0
    minY = 99
    maxY = 0
    for slotindex in controller.playerRedSlots:
        tempSlot = controller.playerRedSlots[slotindex]
        if tempSlot.Index[0]< minX:
            minX = tempSlot.Index[0]
        if tempSlot.Index[0]> maxX:
            maxX = tempSlot.Index[0]
        if tempSlot.Index[1]< minY:
            minY = tempSlot.Index[1]
        if tempSlot.Index[1]> maxY:
            maxY = tempSlot.Index[1]  
    for slotindex in controller.playerBlueSlots:
        tempSlot = controller.playerBlueSlots[slotindex]
        if tempSlot.Index[0]< minX:
            minX = tempSlot.Index[0]
        if tempSlot.Index[0]> maxX:
            maxX = tempSlot.Index[0]
        if tempSlot.Index[1]< minY:
            minY = tempSlot.Index[1]
        if tempSlot.Index[1]> maxY:
            maxY = tempSlot.Index[1]

    #OFFENSIVE FIND POTENTIAL 2 of 3 in row
    c1 = ["None", "None", me, me, "None", "Any", "Any", "Any"]
    c2 = ["Any", "Any", "Any", "None", me, me, "None", "None"]
    c3 = ["Any", "None", me, me, "None", "None", "Any", "Any"]
    c4 = ["Any", "Any", "None", "None", me, me, "None", "Any"]
    c5 = ["Any", "None", "None", me, me, "None", "Any", "Any"]
    c6 = ["Any", "Any", "None", me, me, "None", "None", "Any"]
    c7 = ["None", me, "None", me, "None", "Any", "Any", "Any"]
    c8 = ["Any", "Any", "Any", "None", me, "None", me, "None"]
    c9 = ["None", me, me, "None", "None", "Any", "Any", "Any"]
    c10 = ["Any", "Any", "Any", "None", "None", me, me, "None"]
    c11 = ["Any", "None", me, "None", me, "None", "Any", "Any"]
    c12 = ["Any", "Any", "None", me, "None", me, "None", "Any"]

    #CHeck Combinations
    combinations = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]
    directions = [[1,0],[0,1],[1,1],[1,-1]]
    for slotIndex in controller.freeSlots:
        slot = controller.freeSlots[slotIndex]
        xIndex = slot.Index[0]
        yIndex = slot.Index[1]

        if xIndex < (minX - 5) or xIndex > (maxX + 5):
            continue
        if yIndex < (minY - 5) or yIndex >(maxY + 5):
            continue

        comboFound = 0
        for dirr in directions:
            xMulti = dirr[0]
            yMulti = dirr[1]

            #GetCombinatio
            combination = []
            outOfRange = False
            for i in range (-4,0):
                try:
                    if (xIndex + i * xMulti) < 0 or (yIndex + i * yMulti) < 0:
                        outOfRange = True
                        break
                    tempSlot = controller.slots[xIndex + i * xMulti][yIndex + i * yMulti]
                    combination.append(tempSlot.Player)
                except:
                    outOfRange = True
                    break
            for i in range (1,5):
                try:
                    if (xIndex + i * xMulti) < 0 or (yIndex + i * yMulti) < 0:
                        outOfRange = True
                        break
                    tempSlot = controller.slots[xIndex + i * xMulti][yIndex + i * yMulti]
                    combination.append(tempSlot.Player)
                except:
                    outOfRange = True
                    break
            if outOfRange == True:
                continue
            
            #Check Combo
            for combo in combinations:
                i = 0
                foundCombo = True
                for string in combo:
                    if string == "Any":
                        i += 1
                    elif string == "None" and combination[i] != you:
                        i += 1
                    elif string == combination[i]:
                        i += 1
                    else:
                        foundCombo = False
                        break
                if foundCombo == True:
                    comboFound += 1
                    break
            
            if comboFound >= 2:
                return (slot)

    #DEFFENSIVE FIND POTENTIAL 2 of 3 in row
    c1 = ["None", "None", you, you, "None", "Any", "Any", "Any"]
    c2 = ["Any", "Any", "Any", "None", you, you, "None", "None"]
    c3 = ["Any", "None", you, you, "None", "None", "Any", "Any"]
    c4 = ["Any", "Any", "None", "None", you, you, "None", "Any"]
    c5 = ["Any", "None", "None", you, you, "None", "Any", "Any"]
    c6 = ["Any", "Any", "None", you, you, "None", "None", "Any"]
    c7 = ["None", you, "None", you, "None", "Any", "Any", "Any"]
    c8 = ["Any", "Any", "Any", "None", you, "None", you, "None"]
    c9 = ["None", you, you, "None", "None", "Any", "Any", "Any"]
    c10 = ["Any", "Any", "Any", "None", "None", you, you, "None"]
    c11 = ["Any", "None", you, "None", you, "None", "Any", "Any"]
    c12 = ["Any", "Any", "None", you, "None", you, "None", "Any"]

    #CHeck Combinations
    combinations = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]
    directions = [[1,0],[0,1],[1,1],[1,-1]]
    for slotIndex in controller.freeSlots:
        slot = controller.freeSlots[slotIndex]
        xIndex = slot.Index[0]
        yIndex = slot.Index[1]

        if xIndex < (minX - 5) or xIndex > (maxX + 5):
            continue
        if yIndex < (minY - 5) or yIndex >(maxY + 5):
            continue

        comboFound = 0
        for dirr in directions:
            xMulti = dirr[0]
            yMulti = dirr[1]

            #GetCombinations
            combination = []
            outOfRange = False
            for i in range (-4,0):
                try:
                    if (xIndex + i * xMulti) < 0 or (yIndex + i * yMulti) < 0:
                        outOfRange = True
                        break
                    tempSlot = controller.slots[xIndex + i * xMulti][yIndex + i * yMulti]
                    combination.append(tempSlot.Player)
                except:
                    outOfRange = True
                    break
            for i in range (1,5):
                try:
                    if (xIndex + i * xMulti) < 0 or (yIndex + i * yMulti) < 0:
                        outOfRange = True
                        break
                    tempSlot = controller.slots[xIndex + i * xMulti][yIndex + i * yMulti]
                    combination.append(tempSlot.Player)
                except:
                    outOfRange = True
                    break
            if outOfRange == True:
                continue
            
            #Check Combo
            for combo in combinations:
                i = 0
                foundCombo = True
                for string in combo:
                    if string == "Any":
                        i += 1
                    elif string == "None" and combination[i] != me:
                        i += 1
                    elif string == combination[i]:
                        i += 1
                    else:
                        foundCombo = False
                        break
                if foundCombo == True:
                    comboFound += 1
                    break
            
            if comboFound >= 2:
                return (slot)

    #Select BY Value
    for slotIndex in controller.freeSlots:
        slot = controller.freeSlots[slotIndex]
        if slot.offValue == selectedValue:
            selected.append(slot)
        elif slot.offValue > selectedValue:
            selectedValue = slot.offValue
            selected = [slot]
    
    index = random.randint(0,len(selected)-1)
    return selected[index]


#INIT
init()
controller = BordController()

#Game Loop
running = True
nextPlayer = "Red"

while running:
    moveMade = "None"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]

            slotFound = False
            for index in controller.freeSlots:
                slot = controller.freeSlots[index]
                if slot.minXY[0] < x < slot.maxXY[0] and slot.minXY[1] < y < slot.maxXY[1]:
                    controller.setPlayer(slot.Index[0], slot.Index[1],nextPlayer)
                    slotFound = True

                    checkWin(slot)

                    #BOT
                    botSelected = selectSlot("Blue")
                    controller.setPlayer(botSelected.Index[0], botSelected.Index[1],"Blue")
                    checkWin(botSelected)
                    break


    ''' Uncomment below to let the bot play both sides.
    #BOT
    botSelected = selectSlot("Blue")
    controller.setPlayer(botSelected.Index[0], botSelected.Index[1],"Blue")
    checkWin(botSelected)
    time.sleep(0.01)

    #BOT
    botSelected = selectSlot("Red")
    controller.setPlayer(botSelected.Index[0], botSelected.Index[1],"Red")
    checkWin(botSelected)
    time.sleep(0.01)
    '''



