# -*- coding: utf-8 -*-

from anki.hooks import wrap
from aqt.editor import Editor, EditorWebView
from aqt.qt import *
from aqt.utils import shortcut, showInfo, showWarning, getBase, getFile, \
    openHelp, tooltip, downArrow
from BeautifulSoup import BeautifulSoup

# You can modify this to add new character sets
SYMBOLS = {
    "favourites": u"αβγ",
    "Arrows": u"←↑↓→⇇⇈⇊⇉⇅⇄⇌",
    "Greek Lower": u"αβγδεζηθικλμνξοπρστυφχψω",
    "Greek Upper": u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ",
    "Maths Basic": u"+−±∓×⋅÷√∑∫∮∝∞■",
    "Maths Equality": u"=≠≈~≡",
    "Maths Equivalence": u"<>≪≫≤≥",
    "Misc": u"✓✗°℃℉℞☹☺☠☢☣♀♂⚕"
}


def onAddAnkiSymbol(self, char):
    self.web.eval("wrap('%s','');" % char)


def onAddAnkiSymbol_factory(self, entity_number):
    return lambda s = self: onAddAnkiSymbol(self, entity_number)


def onAnkiSymbols(self):

    # Creating menus
    main = QMenu(self.mw)

    for k, v in SYMBOLS.items():
        sub_menu = QMenu(k, self.mw)
        for char in v:
            new_action = sub_menu.addAction(char)
            new_action.connect(new_action, SIGNAL(
                "triggered()"), onAddAnkiSymbol_factory(self, char))
        main.addMenu(sub_menu)

    main.exec_(QCursor.pos())


def mySetupButtons(self):
    but = self._addButton("symbolButton", lambda s=self: onAnkiSymbols(self),
                          text=unichr(945) + unichr(946) + unichr(947) + downArrow(), size=False)
    but.setShortcut(QKeySequence("Ctrl+S"))


Editor.setupButtons = wrap(Editor.setupButtons, mySetupButtons)
