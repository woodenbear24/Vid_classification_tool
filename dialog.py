from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from tag_manager import *
import os

# tag setting
class SetTagDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        ui_file = QtCore.QFile("dialog.ui")

        loader = QtUiTools.QUiLoader()
        icon_file = QtGui.QIcon(os.path.join('resources', 'wrench.png'))
        if ui_file.open(QtCore.QFile.ReadOnly): 
            self.ui = loader.load(ui_file, self)
            self.setLayout(self.ui.layout())
            self.setWindowTitle('Tag Setting')
            self.setWindowIcon(icon_file)
        ui_file.close()

        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.author_list = self.findChild(QtWidgets.QTextEdit, "author_list")
        self.tag_list = self.findChild(QtWidgets.QTextEdit, "tag_list")
        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.rejected.connect(self.on_rejected)
        
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
            authors_text += i + "\n"
        for i in tags:
            tags_text += i + "\n"
        self.author_list.setText(authors_text)
        self.tag_list.setText(tags_text)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SetTagDialog()
    window.show()
    app.exec()
