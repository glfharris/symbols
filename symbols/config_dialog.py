from aqt import mw
from aqt.qt import (
    QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QInputDialog,
    QKeySequence, QKeySequenceEdit, QLabel, QLineEdit, QListWidget,
    QMessageBox, QPushButton, QVBoxLayout,
)


def show_config_dialog():
    ConfigDialog(mw).exec()


class ConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Symbols")
        self.config = dict(mw.addonManager.getConfig(__name__) or {})
        self.char_sets = dict(self.config.get("char_sets", {}))
        self._current_set = None
        self._build_ui()
        self._load_sets()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.shortcut_edit = QKeySequenceEdit(
            QKeySequence(self.config.get("short_cut", "ctrl+s"))
        )
        form.addRow("Shortcut:", self.shortcut_edit)

        self.fav_edit = QLineEdit(self.config.get("favourites", ""))
        form.addRow("Favourites:", self.fav_edit)
        layout.addLayout(form)

        layout.addWidget(QLabel("Character Sets"))

        body = QHBoxLayout()
        self.set_list = QListWidget()
        self.set_list.currentItemChanged.connect(self._on_set_changed)
        body.addWidget(self.set_list, 1)

        right = QVBoxLayout()
        right.addWidget(QLabel("Characters:"))
        self.chars_edit = QLineEdit()
        right.addWidget(self.chars_edit)
        right.addStretch(1)
        body.addLayout(right, 2)
        layout.addLayout(body)

        btn_row = QHBoxLayout()
        for label, slot in (
            ("Add Set", self._add_set),
            ("Rename", self._rename_set),
            ("Delete", self._delete_set),
        ):
            b = QPushButton(label)
            b.clicked.connect(slot)
            btn_row.addWidget(b)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self._save)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        self.resize(520, 420)

    def _load_sets(self):
        self.set_list.clear()
        for name in self.char_sets:
            self.set_list.addItem(name)
        if self.set_list.count():
            self.set_list.setCurrentRow(0)
        else:
            self.chars_edit.setEnabled(False)

    def _flush_current(self):
        if self._current_set is not None and self._current_set in self.char_sets:
            self.char_sets[self._current_set] = self.chars_edit.text()

    def _on_set_changed(self, current, _previous):
        self._flush_current()
        if current is None:
            self._current_set = None
            self.chars_edit.clear()
            self.chars_edit.setEnabled(False)
            return
        self._current_set = current.text()
        self.chars_edit.setEnabled(True)
        self.chars_edit.setText(self.char_sets.get(self._current_set, ""))

    def _add_set(self):
        name, ok = QInputDialog.getText(self, "Add Set", "Set name:")
        name = name.strip()
        if not ok or not name:
            return
        if name in self.char_sets:
            QMessageBox.warning(self, "Symbols", f"A set called {name!r} already exists.")
            return
        self._flush_current()
        self.char_sets[name] = ""
        self.set_list.addItem(name)
        self.set_list.setCurrentRow(self.set_list.count() - 1)

    def _rename_set(self):
        item = self.set_list.currentItem()
        if item is None:
            return
        old = item.text()
        new, ok = QInputDialog.getText(self, "Rename Set", "New name:", text=old)
        new = new.strip()
        if not ok or not new or new == old:
            return
        if new in self.char_sets:
            QMessageBox.warning(self, "Symbols", f"A set called {new!r} already exists.")
            return
        self._flush_current()
        self.char_sets = {(new if k == old else k): v for k, v in self.char_sets.items()}
        self._current_set = new
        item.setText(new)

    def _delete_set(self):
        item = self.set_list.currentItem()
        if item is None:
            return
        name = item.text()
        confirm = QMessageBox.question(self, "Symbols", f"Delete set {name!r}?")
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.char_sets.pop(name, None)
        self.set_list.takeItem(self.set_list.row(item))

    def _save(self):
        self._flush_current()
        new_config = dict(self.config)
        new_config["short_cut"] = (
            self.shortcut_edit.keySequence().toString().lower() or "ctrl+s"
        )
        new_config["favourites"] = self.fav_edit.text()
        new_config["char_sets"] = self.char_sets
        mw.addonManager.writeConfig(__name__, new_config)
        self.accept()
