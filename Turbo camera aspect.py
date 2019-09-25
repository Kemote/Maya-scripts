import maya.cmds as cmds

selectCam = cmds.ls(selection = True)
selectCam = cmds.listRelatives(shapes = True)[0]
renderW = float(cmds.getAttr("defaultResolution.width"))
renderH = float(cmds.getAttr("defaultResolution.height"))

try:
    cameraW = float(cmds.getAttr(selectCam + ".horizontalFilmAperture"))
    proportion = renderW/renderH
    cmds.setAttr(selectCam + ".verticalFilmAperture", cameraW/proportion)
except:
    cmds.error("Selec camera object!")