import json

from aqt import gui_hooks, mw
from aqt.qt import QMenu, QCursor
from aqt.editor import Editor

from . import config_dialog


def onSymbolButton(editor):
    config = mw.addonManager.getConfig(__name__)

    main = QMenu(editor.parentWindow)

    last = main.addAction(f"Last Used: {config['last_used']}")
    last.triggered.connect(symbolFactory(editor, config["last_used"], config))

    faves = QMenu("Favourites", editor.parentWindow)
    main.addMenu(faves)

    faves_list = list(config["favourites"])
    char_sets = config["char_sets"]

    for char in faves_list:
        a = faves.addAction(char)
        a.triggered.connect(symbolFactory(editor, char, config))

    for k, v in char_sets.items():
        tmp_menu = QMenu(k, editor.parentWindow)
        main.addMenu(tmp_menu)

        chars = list(v)

        for char in chars:
            a = tmp_menu.addAction(char)
            a.triggered.connect(symbolFactory(editor, char, config))

    main.exec(QCursor.pos())


def symbolFactory(editor, symbol, config):
    return lambda: add_char(editor, symbol, config)


def add_char(editor: Editor, char, config):
    config["last_used"] = char
    mw.addonManager.writeConfig(__name__, config)
    editor.web.eval(f"pasteHTML({json.dumps(char)}, true, false);")


def setupButtons(buttons, editor: Editor):
    config = mw.addonManager.getConfig(__name__)
    short_cut = config.get("short_cut", "ctrl+s")
    b = editor.addButton( None, 'Sym', onSymbolButton,
                         tip=f"Inserts symbol at cursor ({short_cut})",
                         keys=short_cut,
                    )
    buttons.append(b)

    return buttons


gui_hooks.editor_did_init_buttons.append(setupButtons)
mw.addonManager.setConfigAction(__name__, config_dialog.show_config_dialog)
