import maya.cmds as cmds
import functools

if 'turboAlignUiKemot' in globals(): #warunek sprawdzający czy istnieje lista o zadanej nazwie jesli nie to tworzy ją z deffaltowymi wartościami dla UI
    print ''
else:
    turboAlignUiKemot = [True, True, True, 3, 3, False, False, False, False, False, False]

def combineLists(list1,list2, listFilter): #funkcja do łączenia dwuch lsit według klucza z trzeciej
    combinedList = [0,0,0]
    i = 0
    for element in listFilter:
        if element == True:
            combinedList[i] = list1[i]
        else:
            combinedList[i] = list2[i]
        i += 1
    return combinedList

def createUI(uiID,scriptName):    
           
    if cmds.window(uiID, exists = True):    
            cmds.deleteUI(uiID)
            
    objectList = cmds.ls(selection = True)
    alignTarget = objectList.pop(-1)  
    targetRotScl = cmds.xform(alignTarget, query = True, rotation = True, worldSpace = True) + cmds.xform(alignTarget, query = True, scale = True, relative = True, worldSpace = True) #zmienna przechowująca rotacje i skale docelowego obiektu

    objectListInitial = [] #trzyma początkowe transofrmacje obiwktów z objectList
    
    for x in objectList:
        transform = [cmds.getAttr(x + '.translateX'), 
                     cmds.getAttr(x + '.translateY'),
                     cmds.getAttr(x + '.translateZ'),
                     cmds.getAttr(x + '.rotateX'),
                     cmds.getAttr(x + '.rotateY'),
                     cmds.getAttr(x + '.rotateZ'),
                     cmds.getAttr(x + '.scaleX'),
                     cmds.getAttr(x + '.scaleY'),
                     cmds.getAttr(x + '.scaleZ')]
        objectListInitial.append(transform)

    def cancelCallback(*pArgs):
        if cmds.window(uiID, exists = True):
            cmds.deleteUI(uiID)
            
        for obj in objectList: #pętla przywracające wstępne transformacje w razie cancel
            x = objectList.index(obj)
            cmds.setAttr(obj + '.translate',objectListInitial[x][0],objectListInitial[x][1],objectListInitial[x][2])
            cmds.setAttr(obj + '.rotate',objectListInitial[x][3],objectListInitial[x][4],objectListInitial[x][5])
            cmds.setAttr(obj + '.scale',objectListInitial[x][6],objectListInitial[x][7],objectListInitial[x][8])
        
    def okCallback(*pArgs):
        if cmds.window(uiID, exists = True):
            cmds.deleteUI(uiID)
                           
    def changePos(*pArgs):
        turboAlignUiKemot[0] = cmds.checkBox(posX, query = True, value = True)
        turboAlignUiKemot[1] = cmds.checkBox(posY, query = True, value = True)
        turboAlignUiKemot[2] = cmds.checkBox(posZ, query = True, value = True) 
        turboAlignUiKemot[3] = cmds.radioButtonGrp(currentObj, query = True, select = True)   
        turboAlignUiKemot[4] = cmds.radioButtonGrp(targetObj, query = True, select = True)
        posValuList = turboAlignUiKemot[:3] #lista trzymająca checkboxy x y z pozycji
        #alignTargetTransforms = [] --------przetrzymuje dane o pozycji targetu       

        #==========sekcja kodu do wyznaczania pozycji odniesienia docelowego obiektu TARGET
        if turboAlignUiKemot[4] == 1:
            targetPosition = cmds.xform(alignTarget, query = True, boundingBox = True)[:3]
            
        elif turboAlignUiKemot[4] == 2:
            targetPosition = cmds.objectCenter(alignTarget)
            
        elif turboAlignUiKemot[4] == 3:
            targetPosition = cmds.xform(alignTarget, query = True, rp = True, ws = True)
            
        elif turboAlignUiKemot[4] == 4:
            targetPosition = cmds.xform(alignTarget, query = True, boundingBox = True)[3:]
            
        #==========sekcja kodu do wyznaczania pozycji odniesienia zaznaczonych obiektów CURRENT
        if turboAlignUiKemot[3] == 1:
            for obj in objectList:
                objMinimum = cmds.xform(obj, query = True, boundingBox = True)[:3]
                objCenter = cmds.objectCenter(obj)
                positionMinimum = [targetPosition[0] + (objCenter[0] - objMinimum[0]), targetPosition[1] + (objCenter[1] - objMinimum[1]), targetPosition[2] + (objCenter[2] - objMinimum[2])]
                transform = combineLists(positionMinimum, objectListInitial[objectList.index(obj)],posValuList)
                cmds.setAttr(obj + '.translate', transform[0], transform[1], transform[2])
            
        elif turboAlignUiKemot[3] == 2:
            for obj in objectList:
                transform = combineLists(targetPosition, objectListInitial[objectList.index(obj)],posValuList)
                cmds.setAttr(obj + '.translate', transform[0], transform[1], transform[2]) 
                
            
        elif turboAlignUiKemot[3] == 3:
            for obj in objectList:
                objPivot = cmds.xform(obj, query = True, rp = True)
                positionPivot = [targetPosition[0] - objPivot[0], targetPosition[1] - objPivot[1], targetPosition[2] - objPivot[2]]
                transform = combineLists(positionPivot, objectListInitial[objectList.index(obj)],posValuList)
                cmds.setAttr(obj + '.translate', transform[0], transform[1], transform[2]) 
            
        elif turboAlignUiKemot[3] == 4:
            for obj in objectList:
                objMaximum = cmds.xform(obj, query = True, boundingBox = True)[3:]
                objCenter = cmds.objectCenter(obj)
                positionMaximum = [targetPosition[0] + (objCenter[0] - objMaximum[0]), targetPosition[1] + (objCenter[1] - objMaximum[1]), targetPosition[2] + (objCenter[2] - objMaximum[2])]
                transform = combineLists(positionMaximum, objectListInitial[objectList.index(obj)],posValuList)
                cmds.setAttr(obj + '.translate', transform[0], transform[1], transform[2])
                
    def changeRot(*pArgs):
        turboAlignUiKemot[5] = cmds.checkBox(orientX, query = True, value = True)
        turboAlignUiKemot[6] = cmds.checkBox(orientY, query = True, value = True)
        turboAlignUiKemot[7] = cmds.checkBox(orientZ, query = True, value = True)
        for obj in objectList:
            transform = combineLists(targetRotScl[:3],objectListInitial[objectList.index(obj)][3:6],turboAlignUiKemot[5:8])
            cmds.setAttr(obj + '.rotate', transform[0], transform[1], transform[2])
        
    def changeScl(*pArgs):
        turboAlignUiKemot[8] = cmds.checkBox(scaleX, query = True, value = True)
        turboAlignUiKemot[9] = cmds.checkBox(scaleY, query = True, value = True)
        turboAlignUiKemot[10] = cmds.checkBox(scaleZ, query = True, value = True)
        for obj in objectList:
            transform = combineLists(targetRotScl[3:],objectListInitial[objectList.index(obj)][6:],turboAlignUiKemot[8:])
            cmds.setAttr(obj + '.scale', transform[0], transform[1], transform[2])
        
    cmds.window(uiID, title = scriptName, sizeable = False, width = 300) #komenda ropzpoczynająca tworzenie struktury okna  
    cmds.columnLayout(columnAttach = ('both', 5), columnWidth = 300)
    cmds.separator(height = 25, style = 'singleDash')
    cmds.text(label = 'Align position', align = 'center')
    cmds.separator(height = 25, style = 'singleDash')
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns = 3, columnWidth = [(1,100),(2,100),(3,100)])
    posX = cmds.checkBox(label = 'X Position', value = turboAlignUiKemot[0], changeCommand = changePos)
    posY = cmds.checkBox(label = 'Y Position', value = turboAlignUiKemot[1], changeCommand = changePos)
    posZ = cmds.checkBox(label = 'Z Position', value = turboAlignUiKemot[2], changeCommand = changePos)
    cmds.setParent('..') #przestaje szukać childów dla rowLayout
    cmds.separator(height = 20, style = 'none')
    
    cmds.rowLayout(columnAttach = [(1, 'both', 0),(2, 'left', 5)], numberOfColumns = 2, columnWidth = [(1,150),(2,150)])
    cmds.text(label = 'Current object:', align = 'center')
    cmds.text(label = 'Target object:', align = 'center')
    cmds.setParent('..')
    cmds.separator(height = 5, style = 'none')
            
    cmds.rowLayout(columnAttach = [(1, 'both', 25),(2, 'left', 5)], numberOfColumns = 2, columnWidth = [(1,150),(2,150)])
    currentObj = cmds.radioButtonGrp(numberOfRadioButtons = 4, vertical = True, labelArray4 = ('Minimum','Center','Pivot point','Maximum'), select = turboAlignUiKemot[3], onCommand = changePos)
    targetObj = cmds.radioButtonGrp(numberOfRadioButtons = 4, vertical = True, labelArray4 = ('Minimum','Center','Pivot point','Maximum'), select = turboAlignUiKemot[4], onCommand = changePos)
    cmds.setParent('..')
    cmds.separator(height = 25, style = 'singleDash')
    
    cmds.text(label = 'Align orientation (local)', align = 'center')
    cmds.separator(height = 15, style = 'none')
    cmds.rowLayout(numberOfColumns = 3, columnWidth = [(1,100),(2,100),(3,100)])
    orientX = cmds.checkBox(label = 'X Axis', value = turboAlignUiKemot[5], changeCommand = changeRot)
    orientY = cmds.checkBox(label = 'Y Axis', value = turboAlignUiKemot[6], changeCommand = changeRot)
    orientZ = cmds.checkBox(label = 'Z Axis', value = turboAlignUiKemot[7], changeCommand = changeRot)
    cmds.setParent('..')
    cmds.separator(height = 25, style = 'singleDash')
    
    cmds.text(label = 'Align scale', align = 'center')
    cmds.separator(height = 15, style = 'none')
    cmds.rowLayout(numberOfColumns = 3, columnWidth = [(1,100),(2,100),(3,100)])
    scaleX = cmds.checkBox(label = 'X Axis', value = turboAlignUiKemot[8], changeCommand = changeScl)
    scaleY = cmds.checkBox(label = 'Y Axis', value = turboAlignUiKemot[9], changeCommand = changeScl)
    scaleZ = cmds.checkBox(label = 'Z Axis', value = turboAlignUiKemot[10], changeCommand = changeScl)
    cmds.setParent('..')
    cmds.separator(height = 25, style = 'singleDash')
    
    cmds.rowLayout(columnAttach = [(1, 'both', 15),(2, 'both',0)], numberOfColumns = 2)
    cmds.button(label = 'OK', width = 120, height = 30, command = okCallback)
    cmds.button(label = 'Cancel', width = 120, height = 30, command = cancelCallback)
   
    changePos()
    changeRot()
    changeScl()
    print 'done'
          
    cmds.showWindow() #komenda pokazująca okno
    
createUI('turboAlign', 'Turbo Align')

