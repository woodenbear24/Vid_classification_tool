from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QDialog


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("main_2.ui")

        if ui_file.open(QFile.ReadOnly):
            self.window = loader.load(ui_file, self)
            self.setCentralWidget(self.window.centralWidget())  # <- THIS LINE
            ui_file.close()

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("dialog.ui")

        if ui_file.open(QFile.ReadOnly):
            self.window = loader.load(ui_file, self)
            # self.setCentralWidget(self.window.centralWidget())  # <- THIS LINE
            ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    window0 = MyDialog()
    window0.show()
    app.exec()
