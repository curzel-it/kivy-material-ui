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


class TestApp( App ) :
    
    def build( self ) : 
        nav = NavigationController()
        nav.push( Label(), title='View #1' )
        nav.push( Label(), title='View #2' )
        nav.push( Label(), title='View #3' )
        return nav

if __name__ == '__main__':
    TestApp().run()


