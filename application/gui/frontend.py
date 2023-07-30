from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QAction, QLayout, QWidget
from PyQt5.QtGui import QIcon


class GuiApp(QMainWindow):

    def __init__(self, ver):
        super().__init__()
        
        self.title = 'Game Keeper App v%s' % ver
        
        self.left = 50
        self.top = 50
        self.width = 1280
        self.height = 960
        
        self.initialize_ui()
        
    def initialize_ui(self):
        
        self.setWindowTitle(self.title)
        
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.addWidgetItems()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(' &File')

        exitButton = QAction(QIcon('exit24.png'), ' &Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        
        self.show()
        
        
    def addWidgetItems(self):
              
        self._main_widget = QWidget(self)