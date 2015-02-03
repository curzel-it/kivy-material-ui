import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.actionbar import ActionBar, ActionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from flatui.flatui import *
from flatui.labels import *
from flatui.popups import *

from navigation.control import *

Builder.load_file( 'nav-test.kv' )

i = 1

class TestApp( App ) :
    
    def build( self ) : 

        self.nav = NavigationController()
        self.nav.next = self.next   
        self.nav.next()
        return self.nav

    def next( self, *args ) :
        global i
        msg = 'SAMPLE #%d' % ( i )
        self.nav.push( Label( text=msg, size_hint=(1,1) ), title=msg )
        i += 1

    def on_pause( self, *args ) : return True

if __name__ == '__main__':
    TestApp().run()


