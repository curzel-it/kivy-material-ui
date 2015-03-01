import sys

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout

#KV Lang files
from pkg_resources import resource_filename
path = resource_filename( __name__, 'form.kv' )
Builder.load_file( path )

class Form( BoxLayout ) :

    shared_navigation_controller = ObjectProperty( None )
    title = StringProperty( '' )

    def __init__( self, **kargs ) :
        if not 'shared_navigation_controller' in kargs.keys() :
            raise ValueError( 'You MUST provide a valid controller for shared_navigation_controller' )

        super( Form, self ).__init__( **kargs )

    def push( self ) :
        self.shared_navigation_controller.push( self, title=self.title )

    def pop( self ) :
        self.shared_navigation_controller.push()

