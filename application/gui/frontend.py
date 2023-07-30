import os 

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QAction, QLayout, QWidget, QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon


class GuiApp():

    def initialize(self):
        
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        
        # Adding an icon
        icon = QIcon(r"C:\projects\pgsm_agent\application\gui\resources\keeper.png")
        
        # Adding item on the menu bar
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        
        # Creating the options
        menu = QMenu()
        option1 = QAction("Games")
        menu.addAction(option1)
        
        # To quit the app
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)
        
        # Adding options to the System Tray
        tray.setContextMenu(menu)

        app.exec_()