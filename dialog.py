from PyQt6 import QtWidgets, uic
from tag_manager import *

# tag setting
class SetTagDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Dialog.ui", self) 

        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")

        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.accepted.connect(self.on_rejected)
        
        self.load()

    def on_accepted(self):
        authors_text = tags_text = ""
        authors_text = self.author_list.toPlainText()
        tags_text = self.tag_list.toPlainText()
        authors_array = authors_text.strip().split('\n')
        tags_array = tags_text.strip().split('\n')
        json = {"author":authors_array, "tag":tags_array}
        tag_save(json)
        print(f"Saving tags:{json}")
        self.accept()

    def on_rejected(self):
        print("Tag Editing Aborted")
        self.reject() 
    
    def load(self):
        json = tag_load()
        authors = json['author']
        tags = json['tag']
        authors_text = tags_text = ""
        for i in authors:
            authors_text = authors_text + i + "\n"
        for i in tags:
            tags_text = tags_text + i + "\n"
        self.author_list.setText(authors_text)
        self.tag_list.setText(tags_text)