from direct.gui.DirectGui import *
from pandac.PandaModules import *


class Menu:

    def __init__(self, menuGraphics, fonts, inputManager = None):
        self.menuGraphics = menuGraphics
        self.fonts = fonts
        self.inputManager = inputManager
        self.self = self

    def initMenu(self, args):
        type = args[0]
        if(args[1] != None):
            self.title = args[1]
        else:
            self.title = None
            self.items = args[2]
            self.funcs = args[3]
            self.funcArgs = args[4]
            self.buttons = []

        if(type == 0):
            self.frame = DirectFrame(
                geom = self.menuGraphics.find("**/Menu0"),
                relief = None, scale = (1.5,1,1.5),
                frameColor = (1,1,1,.75),
                pos = (.2625,0,.43125), parent = base.a2dBottomLeft)
            framePadding = .1
            height = self.frame.getHeight() - framePadding
            for N in range(len(self.items)):
                xPos = 0
                zPos = height/2 - (height / (len(self.items)-1)) * N
                self.buttons.append(DirectButton(
                    command=self.activateItem, extraArgs = [N],
                    geom=(self.menuGraphics.find("**/BttnNormal"),
                            self.menuGraphics.find("**/BttnPushed"),
                            self.menuGraphics.find("**/BttnNormal"),
                            self.menuGraphics.find("**/BttnNormal")),
                    relief=None, clickSound=None,
                    rolloverSound=None, parent = self.frame,
                    pos = (xPos, 0, zPos)))
                self.items[N] = DirectLabel(text = self.items[N],
                                            text_font = self.fonts["silver"],
                                            text_fg = (1,1,1,.75), relief = None,
                                            text_align = TextNode.ACenter,
                                            text_scale = .035, parent = self.buttons[N])
                self.items[N].setPos(0,0,-self.items[N].getHeight()/2)
        if(self.inputManager != None):
            self.itemHL = 0
            self.keyWait = 0
            self.highlightItem(0)
            taskMgr.add(self.menuControl, "Menu Control")
        return

    def highlightItem(self, item):
        if(item < 0): item = len(self.items) - 1
        if(item == len(self.items)): item = 0
        self.items[self.itemHL]["text_font"] = self.fonts["silver"]
        self.items[item]["text_font"] = self.fonts["orange"]
        self.itemHL = item
        return
    def activateItem(self, item):
        if(type(self.funcs[item]) == list):
            for N in range(len(self.funcs[item])):
                if(self.funcArgs[item][N] != None):
                    self.funcs[item][N](self.funcArgs[item][N])
                else:
                    self.funcs[item][N]()
        else:
            if(self.funcArgs[item] != None):
                self.funcs[item](self.funcArgs[item])
            else:
                self.funcs[item]()
        self.destroy()
        return

    def menuControl(self, task):
        if(self.self == None):
            return task.done
        dt = globalClock.getDt()
        if( dt > .20):
            return task.cont
        self.keyWait += dt
        if(self.keyWait > .25):
            if(self.inputManager.keyMap["up"] == True):
                self.highlightItem(self.itemHL - 1)
                self.keyWait = 0
            elif(self.inputManager.keyMap["down"] == True):
                self.highlightItem(self.itemHL + 1)
                self.keyWait = 0
            elif(self.inputManager.keyMap["fire"] == True):
                self.activateItem(self.itemHL)
                self.keyWait = 0
        return task.cont

    def destroy(self):
        for N in range(len(self.items)):
            self.items[0].destroy()
            self.buttons[0].destroy()
        if(self.title != None):
            self.title.destroy()
        self.frame.destroy()
        self.self = None
        return

if __name__=="__main__":
    menuGraphics = loader.loadModel("../Models/MenuGraphics.egg")
    fonts = {"silver" : loader.loadFont("../Fonts/LuconSilver.egg"),
             "blue" : loader.loadFont("../Fonts/LuconBlue.egg"),
             "orange" : loader.loadFont("../Fonts/LuconOrange.egg")}
    menu = Menu(menuGraphics, self.fonts, self.inputManager)
    menu.initMenu([0,None,
                   ["New Game","Quit Game"],
                   [[self.printTest],[self.printTest]],
                   [[0],[1]]])
