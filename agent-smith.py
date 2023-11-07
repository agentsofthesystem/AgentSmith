import sys

from application.gui.launch import GuiApp
from application.gui.globals import GuiGlobals

sys.path.append(".")


##############################################################################
if __name__ == "__main__":
    """
    Main script entry point
    """
    gui_globals = GuiGlobals()
    gui = GuiApp(gui_globals)
    gui.initialize(with_server=True)
