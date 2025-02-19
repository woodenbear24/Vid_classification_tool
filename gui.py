import sys
import os 
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog

class Test(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Form - untitled.ui', self)
        #Signal
        self.loaddir_button = self.findChild(QtWidgets.QToolButton,'loaddir_button') 
        self.dir_entry = self.findChild(QtWidgets.QLineEdit, 'dir_entry')
        self.fileList = self.findChild(QtWidgets.QListWidget, 'filelist') 
        self.up_dir_button = self.findChild(QtWidgets.QToolButton, 'up_dir_button')

        #if self.LoadDir_button: 
        self.loaddir_button.clicked.connect(self.on_button_clicked)

        # if self.Dir_entry: 
        self.dir_entry.textChanged.connect(self.update_file_list) 

        # if self.FileList: # Ensure FileList object exists
        self.fileList.itemDoubleClicked.connect(self.handle_file_list_click) 

        # if self.up_dir_button:
        self.up_dir_button.clicked.connect(self.dir_up)

    def test_func(self):
        print(f"test_triggered")

    def on_button_clicked(self):
        Dir = QFileDialog.getExistingDirectory(self, "Select Dir", "")
        print(f"Selected:{Dir}")
        if Dir:
            self.dir_entry.setText(Dir)

    def update_file_list(self, text): 
        dir_path = text # 获取输入框中的目录路径
        self.fileList.clear() # 清空列表

        if dir_path: # 确保路径不为空
            if os.path.isdir(dir_path): # 检查路径是否是有效目录
                try:
                    files = os.listdir(dir_path) # 获取目录下的所有文件和文件夹
                    self.fileList.addItems(files) # 将文件列表添加到 QListWidget
                except Exception as e: # 捕获可能发生的异常，例如权限错误
                    print(f"Error reading directory: {e}")

    def handle_file_list_click(self, item): # 新的槽函数，用于处理文件列表中的项目点击事件
        clicked_item_text = item.text() # 获取被点击项目的文本
        current_dir_path = self.dir_entry.text() # 获取输入框中当前的目录路径

        if current_dir_path: # 确保存在当前的目录路径
            full_item_path = os.path.join(current_dir_path, clicked_item_text) # 构建完整路径
            print(f"Clicked:{full_item_path}")
            if os.path.isdir(full_item_path): # 检查是否为目录
                self.dir_entry.setText(full_item_path) # 将输入框文本设置为被点击的目录路径
                print(f"Jumping to:{full_item_path}")

    def dir_up(self):
        current_path = self.dir_entry.text()
        up_dir = os.path.dirname(current_path)
        print(f"Back to:{up_dir}")
        self.dir_entry.setText(up_dir)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

