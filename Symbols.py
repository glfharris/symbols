from anki.hooks import wrap
from aqt.editor import Editor, EditorWebView
from aqt.qt import *
from aqt.utils import shortcut, showInfo, showWarning, getBase, getFile, \
    openHelp, tooltip, downArrow
from BeautifulSoup import BeautifulSoup

# This is the favourites list - Add desired symbols' decimal values here
faves = [8592, 8593, 8594, 8595]

def onAddAnkiSymbol(self, entity_number):
    my_entity = "&#" + str(entity_number) + ";"
    self.note.fields[self.currentField] += unicode(BeautifulSoup(my_entity))
    self.loadNote()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

def onAddAnkiSymbol_factory(self, entity_number):
    return lambda s=self: onAddAnkiSymbol(self, entity_number)

def onAnkiSymbols(self):

    # Creating menus
    main = QMenu(self.mw)

    favourites = QMenu("Favourites", self.mw)
    greek = QMenu("Greek letters", self.mw)
    arrows = QMenu("Arrows", self.mw)

    # Adding submenus to main menu
    main.addMenu(favourites)
    main.addMenu(greek)
    main.addMenu(arrows)

    # Adding symbols to sub menus
    # Greek Letters 913 - 974
    for greek_letter in range(913, 975):
        a = greek.addAction(unichr(greek_letter))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, greek_letter))

    # Arrows 8592 - 8703
    for arrow in range(8592, 8704):
        a = arrows.addAction(unichr(arrow))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, arrow))

    # Add favourites to menu
    for f in faves:
        a = favourites.addAction(unichr(f))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, f))
    main.exec_(QCursor.pos())

def mySetupButtons(self):
    but = self._addButton("symbolButton", lambda s=self: onAnkiSymbols(self),
                    text=unichr(945) + unichr(946) + unichr(947) + downArrow(), size=False)
    but.setShortcut(QKeySequence("Ctrl+S"))

Editor.setupButtons = wrap(Editor.setupButtons, mySetupButtons)