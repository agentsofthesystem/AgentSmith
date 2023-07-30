# -*- coding: utf-8 -*-

import sys

import argparse as _argparse

from PyQt5.QtWidgets import QApplication

from application.gui.frontend import GuiApp
from application.gui.globals import GuiGlobals

sys.path.append('.')

class MainArgParse:
    
    def __init__(self):
        
        self._g_help = False
        self.__verbose__ = False
        self._run_gui = False
        
        self._subparser_name = None
        
        self._manager = None
        
        self._globals = GuiGlobals()
        
        psr = _argparse.ArgumentParser(prog=__file__,
                                       description=self._globals._DESCRIPTION_MSG,
                                       epilog=self._globals._EPILOG_MSG,
                                       formatter_class=_argparse.RawTextHelpFormatter)
        
        self._add_generic_args(psr)
        
        self._add_subparser(psr)
        
        if len(sys.argv) == 1:
            psr.print_help()
            sys.exit()
            
        psr.parse_args(args=self._sort_args(), namespace=self)
            
            
    def apply(self):
        
        if self._subparser_name == 'gui':
            self._run_gui = True

            
    def _add_subparser(self, psr):
        
        sub = psr.add_subparsers(dest='_subparser_name',
                                 metavar='sub_commands',
                                 help='this is help')

        
        gui = sub.add_parser('gui', help='Runs the main app user interface.')
        
        self._sub_list = [ gui ]
        
        for item in self._sub_list:
            self._add_generic_args(item)
                        
    @staticmethod
    def _add_generic_args(psr):
        
        psr.add_argument('-v', '--verbose', dest="__verbose__", action="store_true", 
                 default=False, help='enable verbose output debug')
        
    def _sort_args(self):
        
        """
        Move all subparsers to the front
        """
        
        sub_names = [x.prog.split()[1] for x in self._sub_list ]
        
        sub_args = sys.argv[1:]
        
        for f in sub_names:
            if f in sub_args:
                sub_args.remove(f)
                sub_args.insert(0,f)

        return sub_args
        
    def __str__(self):
        
        return '\n'.join(['Class info goes here!'])
    
    
##############################################################################
if __name__ == '__main__':
    
    """
    Main script entry point
    """
    
    _globals = GuiGlobals()
    
    _arg = MainArgParse()
    _arg.apply()
    
    if _arg._run_gui:
        app = QApplication(sys.argv)
        ex = GuiApp(_globals._VERSION)
        sys.exit(app.exec_())