import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout

from flatui.flatui import *
from flatui.labels import *
from flatui.popups import *

Builder.load_file( 'ui-test.kv' )

class Test( BoxLayout ) :
    
    def __init__( self, **kargs ) :
        super( Test, self ).__init__( **kargs )

    def show_popup1( self ) :
        p = FlatPopup( 
            size_hint=(0.8,.8), \
            title='Customizable title', \
            title_align='left', \
            title_color=[0,0,0,.9], \
            title_size=26
        )
        p.open()

    def show_popup2( self ) :
        AlertPopup( text='This is a quick alert!\nWith two buttons...', cancel_button_text='Cancel' ).open()

    def show_popup3( self ) :
        AlertPopup( text='This is a quick alert!' ).open()

    def show_popup4( self ) :
        OkButtonPopup( text='This is an other shortcut,\nto be used for quick messages' ).open()


class TestApp( App ) :
    
    def build( self ) : return Test()

if __name__ == '__main__':
    TestApp().run()



