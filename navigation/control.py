import sys
from kivy.animation import Animation
from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp
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

    animation_duracy = NumericProperty( .25 )
    '''
    Push & pop animation duracy, default 0.25 seconds.
    '''

    push_mode = OptionProperty( 'right', options=['left','right'] )
    '''
    Left or right, will push/pop views from/to the given direction.
    '''

    disable_widget = BooleanProperty( False ) 
    '''
    If true, root widget will be disabled during animations.
    This will hide animations!
    '''

    #Navigation bar

    title = StringProperty( 'Navigation control!' )
    '''
    Navigation bar title.
    '''    
    
    nav_height = NumericProperty( dp(84) )
    '''
    Navigation bar height.
    '''
    
    nav_color = ListProperty( [.32, .18, .7, 1] )
    '''
    Navigation bar color.
    '''

    font_size = NumericProperty( dp(36) )
    '''
    Navigation bar font size.
    '''

    text_color = ListProperty( [1,1,1,1] )
    '''
    Navigation bar text color.
    '''

    #Private stuffs...
    _push_cache = ListProperty( [] )
    _anim_area = ObjectProperty( None )
    _actionprev = ObjectProperty( None )
    _actiontext = ObjectProperty( None )
    _content = ObjectProperty( None )
    _width = NumericProperty( float(Config.get('graphics','width')) )

    def __init__( self, **kargs ) :
        super( NavigationController, self ).__init__( **kargs )
        self._has_root = False
        self._last_args = {'title':'', 'animation':None}
        self._animation = None

    def pop( self, *args ) :
        '''
        Use this to go back to the last view.
        Will eventually throw EmptyNavigationStack.
        '''
        if self._animation is None :
            if len( self.stack ) > 0 : 
                self._save_temp_view( 0, self.root_widget )
                self._run_pop_animation()
            else :
                raise EmptyNavigationStack()

    def push( self, view, **kargs ) :
        '''
        Will append the last view to the list and show the new one.
        Keyword arguments :
            title
                Navigation bar title, default ''.
        '''
            
        if self._animation is None :

            if not 'title' in kargs.keys() : kargs['title'] = ''
            self._last_kargs = kargs
            x = -1 if self.push_mode == 'left' else 1
            self._save_temp_view( x, view )
            self._run_push_animation()

    def _run_push_animation( self ) :
        try : 
            self._temp_view.disabled = self.disable_widget 
            duracy = self.animation_duracy if self._has_root else 0
            self._animation = Animation( x=0, duration=duracy )
            self._animation.bind( on_complete=self._push_temp_view )
            self._animation.start( self._temp_view ) 
        except : pass

    def _run_pop_animation( self ) :
        try : 
            self._temp_view.disabled = self.disable_widget 
            x = self._temp_view.width * ( -1 if self.push_mode == 'left' else 1 )
            self._animation = Animation( x=x, duration=self.animation_duracy )
            self._animation.bind( on_complete=self._pop_temp_view )
            self._animation.start( self._temp_view ) 
        except : pass

    def _push_temp_view( self, *args ) :
        self._temp_view.disabled = False
                
        if self._has_root :            
            self.content.remove_widget( self.root_widget )

        self.stack.append( [ self.root_widget, self._last_kargs ] )
        self.root_widget = self._temp_view
        self._clear_temp_view()
        self.content.add_widget( self.root_widget )
        self._has_root = True
        self._update_nav()
        self._animation = None

    def _pop_temp_view( self, *args ) :
        self._temp_view.disabled = False
        self.content.remove_widget( self.root_widget )
        self.root_widget, self._last_kargs = self.stack.pop()
        if len(self.stack) > 0 : self._last_kargs = self.stack[-1][1]        
        self.content.add_widget( self.root_widget )
        self._update_nav()
        self._animation = None

    def _clear_temp_view( self, *args ) :
        try : 
            self._anim_area.remove_widget( self._temp_view )
        except : pass
        self._temp_view = None  

    def _save_temp_view( self, p, view ) :
        self._temp_view = view
        try : 
            self._temp_view.pos = [ self._width*p, 0 ]
            self._anim_area.add_widget( self._temp_view )
        except : pass

    def _update_nav( self ) :
        self.title = self._last_kargs['title']
        has_previous = len( self.stack ) > 1 
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

