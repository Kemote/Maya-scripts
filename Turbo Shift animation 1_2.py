import maya.cmds as cmds
import functools
import re


offset = 0
baseFrame = 0 #klatka do ktĂłrej standardowo  przesĂłwa sie caĹ‚a animacja 
animCurves = cmds.ls(type = 'animCurve')
selectedCurves = []   #wszystkie krzywe animacji zaznaczoncyh obiektĂłw uzyskuje na podstawie animCurves oraz selectedObj
selectedObj = cmds.ls(selection = True)
startTime = cmds.playbackOptions(query = True, minTime = True)
endTime = cmds.playbackOptions(query = True, maxTime = True)

if not selectedObj:    #w razie braku zaznaczenia
    selectedObj = cmds.ls(transforms = True)
  
for sObj in selectedObj:    #filtruje zaznaczone obiekty z krzywymi animacji, w celu uzyskania potrzebnytch krzywych animacji najpierw bierze wszystkie obiekty typu animCurves, a nastÄ™pnie filtruje przez posiadane obiekty
    checkObj =  sObj.split('_')[0]
    selectedCurves.append(filter(lambda x: re.search('%s.' %checkObj, x), animCurves)) #wyĹ‚uskuje nazwy krzywych animacji wybranych elementĂłw 
selectedCurves = filter(None, selectedCurves)

initialFrame = []
for sCurve in selectedCurves:
    initialFrame += cmds.keyframe(sCurve, query = True)
initialFrame = min(initialFrame)

def animShift():
    print baseFrame
    minimal = [] #najniĹĽsza klakta wszystkich animacji
    for sCurve in selectedCurves:
        minimal += cmds.keyframe(sCurve, query = True)
    minimal = min(minimal) 
    for sCurve in selectedCurves:
        keyframes = cmds.keyframe(sCurve, query = True)
        keyframes = list(dict.fromkeys(keyframes))
        if (int(baseFrame) - int(minimal) + int(keyframes[0]) + int(offset)) > minimal:
            keyframes.sort(reverse = True)
        else:
            keyframes.sort()
        for kFrame in keyframes:
            cmds.keyframe(sCurve, time = (kFrame,kFrame), absolute = True, timeChange = int(baseFrame) - int(minimal) + int(kFrame) + int(offset))
                 
def createUI(uiID, scriptName):
      
    cancelUI(uiID)
    
    #def valChange(self):
     #   global baseFrame
      #  baseFrame = self
       # cmds.intSlider(baseSlider, edit = True, value = int(baseFrame))
        #cmds.textField(baseTextField, edit = True, text = str(baseFrame))
         #animShift()
    
    def valChangeOffset(self): 
        global offset
        offset = self
        cmds.intSlider(offsetSlider, edit = True, value = int(offset))
        cmds.textField(offsetTextField, edit = True, text = str(offset))
        animShift()
    
    def valChangeBase(self):
        global baseFrame
        baseFrame = float(self)
        animShift()
           
    cmds.window(uiID, title = scriptName, resizeToFitChildren = True)
    cmds.rowColumnLayout(numberOfColumns = 2, columnAttach = [(1, 'both', 15), (2,'both', 15)])
    
   # cmds.text(label = 'Base frame:', align = 'left', height = 25)
   # cmds.separator(style = 'none')
   # baseSlider = cmds.intSlider(min = startTime, max = endTime, value = baseFrame, width = 300, dragCommand = valChange)
   # baseTextField = cmds.textField(text = str(baseFrame), width = 60, textChangedCommand = valChange)
    
    cmds.text(label = 'Offset from base:', align = 'left', height = 35)
    cmds.separator(style = 'none')
    offsetSlider = cmds.intSlider(min = -100, max = 100, value = 0, width = 300, dragCommand = valChangeOffset)
    offsetTextField = cmds.textField(text = str(0), width = 60, textChangedCommand = valChangeOffset)
    
    cmds.text(label = 'Base frame:', align = 'left', height = 35)
    cmds.separator(style = 'none')
    baseFrameTextField = cmds.textField(text = str(0), width = 60, textChangedCommand = valChangeBase)
    baseFrameButton = cmds.button(label = 'set current frame as base', command = lambda _: cmds.textField(baseFrameTextField, edit = True, text = cmds.currentTime(query = True)))
    
    cmds.separator(style = 'none', height = 20)
    cmds.separator(style = 'none', height = 20)
    cmds.separator(style = 'none', height = 20)
    autoExtendCheckBox = cmds.checkBox(label = 'Trim', value = False)
    
    cmds.rowLayout(columnAttach = [(1, 'both', 15),(2, 'both',0)], numberOfColumns = 2)
    cmds.button(label = 'OK', width = 120, height = 30, command = functools.partial(okCallback, uiID, autoExtendCheckBox, animCurves))
    cmds.button(label = 'cancel', width = 120, height = 30, command = functools.partial(cancelCallback, uiID, animCurves))    
    
    animShift()
    cmds.showWindow() 

def cancelUI(uiID, *args):
    if cmds.window(uiID, exists = True):
        cmds.deleteUI(uiID)

def okCallback(uiID, autoExtendCheckBox, animCurves, *args):
    if cmds.checkBox(autoExtendCheckBox, query = True, value = True) == True:
        lastFrame = cmds.findKeyframe(animCurves, which = 'last')
        cmds.playbackOptions(max = lastFrame)
        firstFrame = cmds.findKeyframe(animCurves, which = 'first')
        cmds.playbackOptions(min = firstFrame)
    cancelUI(uiID)
    
def cancelCallback(uiID, *args):
    global offset, baseFrame, initialFrame
    offset = 0
    baseFrame = initialFrame
    animShift()
    cancelUI(uiID)   
    
createUI('turboAnimationShift','Turbo Animation Shift')   
