import sys

from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.actionbar import ActionBar, ActionItem, ActionPrevious
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

from pkg_resources import resource_filename
#KV Files
path = resource_filename( __name__, 'control.kv' )
Builder.load_file( path )


class NavigationController( BoxLayout ) :
    '''
    Custom layout you can use to manage navigation in your app.
    This is inspired by iOS navigation system, but much easier...

    You should put a NavigationController as root widget for your app,
    internally uses a stack to manage navigation ( accessible by using the 'stack' property ).

    You can pop\push views by using 'pop' and 'push' methods.
    '''

    root_widget = ObjectProperty( None )
    '''
    The current widget is stored here.
    '''

    stack = ListProperty( [] )
    '''
    Stack used to navigate between various screens\widgets.
    '''

    background_color = ListProperty( [ .93, .93, .93, 1 ] )
    '''
    Solid background color.
    '''

    title = StringProperty( 'Navigation control!' )

    nav_height = NumericProperty( 84 )
    
    nav_color = ListProperty( [.32, .18, .7, 1] )

    font_size = NumericProperty( 36 )

    text_color = ListProperty( [1,1,1,1] )

    actionprev = ObjectProperty( None )
    actiontext = ObjectProperty( None )
    content = ObjectProperty( None )

    def __init__( self, **kargs ) :
        super( NavigationController, self ).__init__( **kargs )
        self._has_root = False
        self._last_args = {'title':'', 'push_animation':None, 'pop_animation':None}

    def pop( self, *args ) :
        '''
        Use this to go back to the last view.
        Will eventually throw EmptyNavigationStack.
        '''
        if len( self.stack ) > 0 :
            self.content.remove_widget( self.root_widget )

            self.root_widget, kargs = self.stack.pop()

            self.content.add_widget( self.root_widget )
            self._update_nav( kargs )
        else :
            raise EmptyNavigationStack()

    def push( self, view, **kargs ) :
        '''
        Will append the last view to the list and show the new one.
        Keyword arguments :
            #is_root_layout, will clean the stack, default False
            push_animation, animation in entrance, default None
            pop_animation,  animation on exit, default None
            title,          navigation bar title, default ''.
        '''
            
        #if not 'is_root_layout' in kargs.keys() : kargs['is_root_layout'] = False
        if not 'push_animation' in kargs.keys() : kargs['push_animation'] = None
        if not 'pop_animation'  in kargs.keys() : kargs['pop_animation' ] = None
        if not 'title'          in kargs.keys() : kargs['title'         ] = ''

        if self._has_root :
            self.stack.append( [ self.root_widget, self._last_kargs ] )        
            self.content.remove_widget( self.root_widget )

        self.root_widget = view
        self.content.add_widget( self.root_widget )

        self._has_root = True
        self._update_nav( kargs )

    def _update_nav( self, kargs ) :
        self.title = kargs['title']
        self._last_kargs = kargs
        has_previous = len( self.stack ) > 0 
        self.actionprev.text = ' < ' if has_previous else ''
        self.actionprev.disabled = not has_previous


class EmptyNavigationStack( Exception ) :
    def __init__( self ) :
        super( EmptyNavigationStack, self ).__init__(
            'Cannot pop view, navigation stack is empty'
        )

#================================================================================
# Private stuff of various use...
#================================================================================

def _navbar_args( kargs ) :
    result = {}
    for key in filter( lambda k:k.startswith('navbar_'), kargs.keys() ) :
        result[ key.replace('navbar_','') ] = kargs[key]
    return result

