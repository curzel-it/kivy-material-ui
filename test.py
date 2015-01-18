import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout

from flatui.flatui import *

class Test( BoxLayout ) :
    
    def __init__( self, **kargs ) :
        super( Test, self ).__init__( **kargs )

    def show_popup( self ) :
        p = FlatPopup( 
            size_hint=(0.8,.8), \
            title='Customizable title', \
            title_align='left', \
            title_color=[0,0,0,.9], \
            title_size=26
        )
        p.open()



class TestApp( App ) :
    
    def build( self ) : return Test()

if __name__ == '__main__':
    TestApp().run()



