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
    '''
    Very simple class to manage you're app views.
    Use it as if it were an Android's Activity or and iOS's View Controller.
    '''

    shared_navigation_controller = ObjectProperty( None )
    '''
    Navigation controller instance, used to pop\push views.
    MUST be provided.
    '''

    title = StringProperty( '' )
    '''
    Title provided in the navigation bar.
    '''

    background_color = ListProperty( None )
    '''
    Solid background color, same color as the navigation controller by default
    '''
    
    def __init__( self, **kargs ) :
        if 'shared_navigation_controller' not in kargs.keys() :
            raise ValueError( 'You MUST provide a valid controller for shared_navigation_controller' )

        if 'background_color' not in kargs.keys() :
            kargs['background_color'] = kargs['shared_navigation_controller'].background_color

        super( Form, self ).__init__( **kargs )

    def push( self ) :
        '''
        Will push this form to the navigation controller.
        '''
        self.shared_navigation_controller.push( self, title=self.title )

    def pop( self ) :
        '''
        Will pop\dismiss this form.
        '''
        self.shared_navigation_controller.push()

    def on_push( self, controller ) :
        '''
        Called by navigation controller whenever the form is being pushed.
        '''
        pass

    def on_pop( self, controller ) :
        '''
        Called by navigation controller whenever the form is being popped.
        '''
        pass

