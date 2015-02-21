#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = "1.0.0"

import pdb
import sys
import traceback

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from flatui.scroll import RefreshableScrollView


class Test( FloatLayout ) :

    myscroll = ObjectProperty( None ) 

    def __init__( self, **kargs ) :
        super( Test, self ).__init__( **kargs )
        self.myscroll = RefreshableScrollView( 
            on_start_reload=self.on_start_reload, root_layout=self 
        )
            
        b = Button( height=1000, size_hint=(1,None) )
        self.myscroll.add_widget( b )
        self.add_widget( self.myscroll )

    def on_start_reload( self, *args ) :
        Clock.schedule_once( self.myscroll.reload_done, 3 )


class TestApp( App ) :
    
    def build( self ) :
        return Test()

if __name__ == '__main__':
    TestApp().run()



