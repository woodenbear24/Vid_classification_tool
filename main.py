import os
from mutagen.mp4 import MP4
from tag_manager import *
from dialog import SetTagDialog
from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from PySide6.QtMultimedia import QMediaPlayer, QVideoSink
from PySide6.QtMultimediaWidgets import QVideoWidget

vid_metadata = None


# main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print(QtWidgets.QStyleFactory.keys())
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

        # UI
        self.loaddir_button = self.findChild(QtWidgets.QToolButton,'loaddir_button') 
        self.dir_entry = self.findChild(QtWidgets.QLineEdit, 'dir_entry')
        self.fileList = self.findChild(QtWidgets.QListWidget, 'filelist') 

        mid_grid = self.findChild(QtWidgets.QGridLayout, "mid_grid")
        # self.video_widget = self.findChild(QVideoWidget, "video_widget")

        # if self.video_widget is None:
        print(999)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(300, 300)
        print(444)
        if mid_grid:
            mid_grid.addWidget(self.video_widget, 0, 0, 1, 2) # add to mid_grid
        else:
            print("Error: mid_grid layout not found in main.ui") 
        
        self.play_button = self.findChild(QtWidgets.QToolButton, "play_button")
        self.up_dir_button = self.findChild(QtWidgets.QToolButton, 'up_dir_button')
        self.author_list = self.findChild(QtWidgets.QListWidget, 'author_list')
        self.tag_list = self.findChild(QtWidgets.QListWidget, 'tag_list')

        self.tag_display_box = self.findChild(QtWidgets.QTextBrowser, 'tag_display_box')
        self.video_slider = self.findChild(QtWidgets.QSlider, 'video_slider')


        self.reload_tags_button = self.findChild(QtWidgets.QToolButton, "reload_tags_button")
        self.tag_config_button = self.findChild(QtWidgets.QToolButton, "tag_config_button")
        self.write_tag = self.findChild(QtWidgets.QPushButton, 'write_tag')
        self.clear_tag_button = self.findChild(QtWidgets.QToolButton, 'clear_tag_button')
        # Media Player
        print(111)
        self.mediaPlayer = QMediaPlayer(self)
        print(222)
        self.mediaPlayer.setVideoOutput(self.video_widget)
        print(333)


        # Signal Connecting
        self.play_button.clicked.connect(self.play_video)
        self.loaddir_button.clicked.connect(self.on_button_clicked)
        self.dir_entry.textChanged.connect(self.update_file_list) 
        self.fileList.itemClicked.connect(self.handle_file_list_click) 
        self.up_dir_button.clicked.connect(self.dir_up)
        self.reload_tags_button.clicked.connect(self.load_tags)
        self.tag_config_button.clicked.connect(self.tag_set)
        self.author_list.itemClicked.connect(self.author_selected)
        self.tag_list.itemClicked.connect(self.tag_selected)
        self.write_tag.clicked.connect(self.tag_mod)
        self.clear_tag_button.clicked.connect(self.tag_clear)


        # initialization
        self.load_tags()


    def test_func(self):
        print(f"test_triggered")

    def on_button_clicked(self):
        Dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Dir", "")
        print(f"Selected:{Dir}")
        if Dir:
            self.dir_entry.setText(Dir)

    def update_file_list(self, text): 
        dir_path = text 
        self.fileList.clear() 

        if dir_path: 
            if os.path.isdir(dir_path): 
                try:
                    files = os.listdir(dir_path) 
                    self.fileList.addItems(files) 
                except Exception as e: 
                    print(f"Error reading directory: {e}")

    def handle_file_list_click(self, item): 
        clicked_item_text = item.text() 
        current_dir_path = self.dir_entry.text() 

        if current_dir_path: 
            full_item_path = os.path.join(current_dir_path, clicked_item_text) 
            full_item_path = full_item_path.replace("\\","/")
            split_path = os.path.splitext(full_item_path)
            if os.path.isdir(full_item_path): 
                self.dir_entry.setText(full_item_path) 
                print(f"Jumping to:{full_item_path}")
            elif (split_path[-1]=='.mp4'):
                global vid_metadata
                vid = full_item_path
                print(f"Selected mp4:{vid}")
                vid_metadata=MP4(vid)
                print (vid_metadata)
                if not '\xa9cmt' in vid_metadata:
                    vid_metadata['\xa9cmt'] = []    # tags
                if not '\xa9ART' in  vid_metadata:
                    vid_metadata['\xa9ART'] = []    # author
                print(vid_metadata)
                self.tag_display()
                self.set_video(vid)

    def dir_up(self):
        current_path = self.dir_entry.text()
        up_dir = os.path.dirname(current_path)
        print(f"Back to:{up_dir}")
        self.dir_entry.setText(up_dir)

    def set_video(self, path):
        self.mediaPlayer.setSource(QtCore.QUrl.fromLocalFile(path))
        self.mediaPlayer.play()
        global vid_metadata
        print(f"Absolute path: {os.path.abspath(path)}")
        print(f"Media player state: {self.mediaPlayer.mediaStatus()}")
        print(f"Media player error: {self.mediaPlayer.error()}")

        # Get video duration and set slider range
        duration = self.mediaPlayer.duration()
        self.video_slider.setRange(0, duration)

        # Create a timer to update the slider position
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)  # Update every 100 milliseconds
        self.timer.timeout.connect(self.update_slider)
        self.timer.start()

        self.video_slider.sliderMoved.connect(self.set_position)

    def update_slider(self):
        position = self.mediaPlayer.position()
        self.video_slider.setValue(position)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def play_video(self):
        if self.mediaPlayer.isPlaying():
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def load_tags(self):
        json = tag_load()
        authors = json['author']
        tags = json['tag']
        self.author_list.clear()
        self.author_list.addItems(authors)
        self.tag_list.clear()
        self.tag_list.addItems(tags)
        print("tags loaded")
    
    def tag_set(self):
        SetTagDialog().exec()
        self.load_tags()

    def author_selected(self, item):
        global vid_metadata
        author = item.text()
        try:
            if author in vid_metadata['\xa9ART']:
                vid_metadata['\xa9ART'].remove(author)
            else:
                vid_metadata['\xa9ART'].append(author)
            self.tag_display()
        except Exception:
            print(f"Err:{Exception}")

    def tag_selected(self, item):
        global vid_metadata
        tag = item.text()
        try:
            vid_metadata['\xa9cmt']
            if tag in vid_metadata['\xa9cmt']:
                vid_metadata['\xa9cmt'].remove(tag)
            else:
                vid_metadata['\xa9cmt'].append(tag)
            self.tag_display()
        except Exception:
            print(f"Err:{Exception}")

    def tag_display(self):
        global vid_metadata
        vid_metadata_text = ""
        try:
            for key,value in vid_metadata.items():
                value_str = ", ".join(map(str, value))
                vid_metadata_text += f"{key}: {value_str}\n"
            print(vid_metadata_text)
            vid_metadata_text = vid_metadata_text.replace("\xa9ART","Author").replace("\xa9cmt","Tag")
            print(vid_metadata_text)
            self.tag_display_box.setText(vid_metadata_text)
        except:pass

    def tag_mod(self):
        global vid_metadata
        try:
            vid_metadata.save()
            print("Tag edit Successful")
        except Exception:
            print(f"Err editing tag:{Exception}")

    def tag_clear(self):
        global vid_metadata
        try:
            vid_metadata['\xa9ART']=[]
            vid_metadata['\xa9cmt']=[]
            self.tag_display()
        except Exception:
            print(f"Err:{Exception}")


if __name__ == '__main__':
    os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
