from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from anki.hooks import addHook, wrap


config = mw.addonManager.getConfig(__name__)


def onSymbolButton(self):
    main = QMenu(mw)

    last = main.addAction("Last Used: %s" % config["last_used"])
    last.triggered.connect(symbolFactory(self, config["last_used"]))

    faves = QMenu("Favourites", mw)
    main.addMenu(faves)

    faves_list = list(config['favourites'])
    char_sets = config["char_sets"]

    for char in faves_list:
        a = faves.addAction(char)
        a.triggered.connect(symbolFactory(self, char))

    for k, v in char_sets.items():
        tmp_menu = QMenu(k, mw)
        main.addMenu(tmp_menu)

        chars = list(v)

        for char in chars:
            a = tmp_menu.addAction(char)
            a.triggered.connect(symbolFactory(self, char))

    main.exec_(QCursor.pos())


def symbolFactory(editor, symbol):
    return lambda: add_char(editor, symbol)


def add_char(editor, char):
    config["last_used"] = char
    mw.addonManager.writeConfig(__name__, config)
    editor.web.eval("wrap('%s', '');" % char)


def setupButtons(buttons, editor):
    b = editor.addButton(
        None, 'Sym', onSymbolButton, tip="Inserts Symbols at Cursor (ctrl+s)", keys='ctrl+s')
    buttons.append(b)

    return buttons


addHook("setupEditorButtons", setupButtons)
