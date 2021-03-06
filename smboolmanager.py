# object to handle the smbools and optimize them

from functools import reduce

from smbool import SMBool
from rom import RomPatches
from graph_helpers import HelpersGraph
from cache import Cache

class SMBoolManager(object):
    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack', 'Nothing', 'NoEnergy']
    countItems = ['ETank', 'Reserve', 'Missile', 'Super', 'PowerBomb']

    def __init__(self):
        Cache.reset()
        self.helpers = HelpersGraph(self)
        self.createFacadeFunctions()
        self.createKnowsFunctions()
        self.resetItems()

    def getItems(self):
        # get a dict of collected items and how many (to be displayed on the solver spoiler)
        itemsDict = {}
        for item in self.items[:-2]: # ignore last two items: nothing and noenergy
            itemsDict[item] = getattr(self, item)
        for item in self.countItems:
            itemsDict[item] = getattr(self, item+"Count")
        return itemsDict

    def eval(self, func, item=None):
        if item is not None:
            self.addItem(item)

        ret = func(self)

        if item is not None:
            self.removeItem(item)

        return ret

    def resetItems(self):
        # start without items
        for item in SMBoolManager.items:
            setattr(self, item, False)

        for item in SMBoolManager.countItems:
            setattr(self, item+'Count', 0)

        Cache.reset()

    def addItem(self, item):
        # a new item is available
        setattr(self, item, True)
        if item in self.countItems:
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def addItems(self, items):
        if len(items) == 0:
            return
        for item in items:
            setattr(self, item, True)
            if item in self.countItems:
                setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if item in self.countItems:
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, False)
        else:
            setattr(self, item, False)

        Cache.reset()

    def createFacadeFunctions(self):
        for fun in dir(self.helpers):
            if fun != 'smbm' and fun[0:2] != '__':
                setattr(self, fun, getattr(self.helpers, fun))

    def createKnowsFunctions(self):
        # for each knows we have a function knowsKnows (ex: knowsAlcatrazEscape()) which
        # take no parameter
        from parameters import Knows, isKnows
        for knows in Knows.__dict__:
            if isKnows(knows):
                setattr(self, 'knows'+knows, lambda knows=knows: self.knowsKnows(knows,
                                                                                 (Knows.__dict__[knows].bool,
                                                                                  Knows.__dict__[knows].difficulty)))

    def isCountItem(self, item):
        return item in ['Missile', 'Super', 'PowerBomb', 'ETank', 'Reserve']

    def itemCount(self, item):
        # return integer
        return getattr(self, item+'Count')

    def haveItem(self, item, difficulty=0):
        return SMBool(getattr(self, item), difficulty, items=[item])

    def knowsKnows(self, knows, smKnows):
        return SMBool(smKnows[0], smKnows[1], knows=[knows])

    def wand2(self, a, b):
        if a.bool is True and b.bool is True:
            return SMBool(True, a.difficulty + b.difficulty,
                          a.knows + b.knows, a.items + b.items)
        else:
            return SMBool(False)

    def wand(self, a, b, c=None, d=None):
        if c is None and d is None:
            ret = self.wand2(a, b)
        elif c is None:
            ret = self.wand2(self.wand2(a, b), d)
        elif d is None:
            ret = self.wand2(self.wand2(a, b), c)
        else:
            ret = self.wand2(self.wand2(self.wand2(a, b), c), d)

        return ret

    def wor2(self, a, b):
        if a.bool is True and b.bool is True:
            if a.difficulty <= b.difficulty:
                return SMBool(True, a.difficulty, a.knows, a.items)
            else:
                return SMBool(True, b.difficulty, b.knows, b.items)
        elif a.bool is True:
            return SMBool(True, a.difficulty, a.knows, a.items)
        elif b.bool is True:
            return SMBool(True, b.difficulty, b.knows, b.items)
        else:
            return SMBool(False)

    def wor(self, a, b, c=None, d=None):
        if c is None and d is None:
            ret = self.wor2(a, b)
        elif c is None:
            ret = self.wor2(self.wor2(a, b), d)
        elif d is None:
            ret = self.wor2(self.wor2(a, b), c)
        else:
            ret = self.wor2(self.wor2(self.wor2(a, b), c), d)

        return ret

    # negates boolean part of the SMBool
    def wnot(self, a):
        return SMBool(not a.bool, a.difficulty, a.knows, a.items)

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            return SMBool(True, difficulty, items = [item])
        else:
            return SMBool(False)

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            return SMBool(True, difficulty, items = ['ETank', 'Reserve'])
        else:
            return SMBool(False)
