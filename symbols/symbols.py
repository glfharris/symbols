import json

from anki import version as anki_version
from anki.hooks import addHook
from aqt import mw
from aqt.editor import Editor
from aqt.qt import *

config = mw.addonManager.getConfig(__name__)

ANKI_VERSION_TUPLE = tuple(int(i) for i in anki_version.split("."))


def onSymbolButton(self):
    main = QMenu(mw)

    last = main.addAction(f"Last Used: {config['last_used']}")
    last.triggered.connect(symbolFactory(self, config["last_used"]))

    faves = QMenu("Favourites", mw)
    main.addMenu(faves)

    faves_list = list(config["favourites"])
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

    main.exec(QCursor.pos())


def symbolFactory(editor, symbol):
    return lambda: add_char(editor, symbol)


def add_char(editor: Editor, char):
    config["last_used"] = char
    mw.addonManager.writeConfig(__name__, config)
    editor.web.eval(f"pasteHTML({json.dumps(char)}, true, false);")


def setupButtons(buttons, editor: Editor):
    b = editor.addButton(
        None,
        "Sym",
        onSymbolButton,
        tip="Inserts Symbols at Cursor (ctrl+s)",
        keys="ctrl+s",
        rightside=ANKI_VERSION_TUPLE < (2, 1, 50),
    )
    # the rightside version of the button doesn't fit the text on Anki > 2.1.50 so it's better to use rightside=false there

    buttons.append(b)

    return buttons


addHook("setupEditorButtons", setupButtons)
