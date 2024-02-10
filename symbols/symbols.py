import json

from anki import version as anki_version
from anki.hooks import addHook, wrap

from aqt import mw
from aqt.qt import *
from aqt.editor import Editor

ANKI_VERSION_TUPLE = tuple(int(i) for i in anki_version.split("."))

config = mw.addonManager.getConfig(__name__)

def onSymbolButton(self):
    main = QMenu(self.widget)

    last = main.addAction(f"Last Used: {config['last_used']}")
    last.triggered.connect(symbolFactory(self, config["last_used"]))

    faves = QMenu("Favourites", self.widget)
    main.addMenu(faves)

    faves_list = list(config["favourites"])
    char_sets = config["char_sets"]

    for char in faves_list:
        a = faves.addAction(char)
        a.triggered.connect(symbolFactory(self, char))

    for k, v in char_sets.items():
        tmp_menu = QMenu(k, self.widget)
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
    short_cut = config.get("short_cut", "ctrl+s")
    b = editor.addButton( None, 'Sym', onSymbolButton,
                         tip=f"Inserts symbol at cursor ({short_cut})",
                         keys=short_cut,
                         rightside=ANKI_VERSION_TUPLE < (2,1,50),
                    )
    buttons.append(b)

    return buttons


addHook("setupEditorButtons", setupButtons)
