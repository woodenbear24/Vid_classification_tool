import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6 import QtUiTools, QtGui, QtCore


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # UI Load
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("main.ui")
        icon_file = QtGui.QIcon(os.path.join('resources', 'wrench.png'))
        if ui_file.open(QtCore.QFile.ReadOnly):
            self.window = loader.load(ui_file, self)
            self.setCentralWidget(self.window.centralWidget())
            self.setWindowTitle('Vid_Classification_tool')
            self.setWindowIcon(icon_file)
            ui_file.close()  


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QtCore.QFile("dialog.ui")

        if ui_file.open(QtCore.QFile.ReadOnly):
            self.window = loader.load(ui_file, self)
            # self.(self.window.verticalLayout())  # <- THIS LINE
            ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    window0 = MyDialog()
    window0.show()
    app.exec()
