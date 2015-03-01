#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = "1.0.0"

import sys
sys.path.append( '..' )

import traceback

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from demo.forms import Screen1
from navigation.control import *

Builder.load_file( 'demo/commons.kv' )

class TestApp( App ) :
    
    def build( self ) :
        self.nav = NavigationController( 
            push_mode='left',
            font_name='font/Roboto-Regular.ttf'
        )
        Screen1( shared_navigation_controller=self.nav ).push() 
        return self.nav

if __name__ == '__main__':
    TestApp().run()



