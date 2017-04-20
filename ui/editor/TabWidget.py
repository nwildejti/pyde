from functools import partial
from PyQt5.QtWidgets import QTabWidget, QPushButton

from ui.editor import TextEdit
from ui.dialogs import MessageBox

class TabWidget(QTabWidget):
    """ Class to handle functionality for the TabWidget """

    def __init__(self, parent=None):
        """ Constructor that takes a parent widget as an optional parameter """
        super().__init__(parent)

        # instance variables to manage the new tabs that are created using the new option
        self._new_tab_numbers = []
        self._next_tab_number = 1
        self._deleted_tab_text = ""

        self.init_ui()

    def set_next_tab_number(self):
        if len(self._new_tab_numbers) == 0:
            self._next_tab_number = 1
        else:
            expected = range(1, max(self._new_tab_numbers) + 1)
            missing = list(set(expected) - set(self._new_tab_numbers))
            if len(missing) == 0:
                self._next_tab_number = max(self._new_tab_numbers) + 1
            else:
                self._next_tab_number = min(missing)
            
        

    @property
    def next_tab_number(self):
        return str(self._next_tab_number)

    def on_tab_closing(self, index):
        """ Function to handle when a tab is closed """
        if index >= 0:
            self._deleted_tab_text = self.tabText(index)
            if(self.currentWidget().document().isModified()):
                save_prompt = MessageBox("This document has modified changes that haven't been saved. Do you want to save changes?", self)

                save_button = QPushButton("Save", self)
                save_prompt.addButton(save_button, MessageBox.YesRole)
                save_prompt.addButton("Cancel", MessageBox.RejectRole)
                save_prompt.addButton("Close Without Saving", MessageBox.NoRole)
                save_prompt.setDefaultButton(save_button)
                self.save_prompt_finish(save_prompt.exec_())
            self.removeTab(index)
        else:
            raise IndexError

    def init_ui(self):
        """ Some initial settings for the TabWidget """
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setTabShape(QTabWidget.Triangular)
        self.tabCloseRequested.connect(self.on_tab_closing)

    def save_prompt_finish(self, result):
        if result == MessageBox.YesRole:
            print('saving')
        elif result == MessageBox.NoRole:
            print('Nope, not saving')
        elif result == MessageBox.RejectRole:
            print('Rejectamundo, or just cancelled')

    def tabInserted(self, index):
        tab_text = self.tabText(index)
        if "new" in tab_text:
            self._new_tab_numbers.append(int(tab_text.split()[-1]))
            self.set_next_tab_number()
            super().tabInserted(index)
        else:
            super().tabInserted(index)

    def tabRemoved(self, index):
        tab_text = self._deleted_tab_text
        if "new" in tab_text:
            self._new_tab_numbers.remove(int(tab_text.split()[-1]))
            self.set_next_tab_number()
            super().tabRemoved(index)
        else:
            super().tabRemoved(index)
