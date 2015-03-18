"""
Please refer to Google's Material UI guidelines :
http://www.google.com/design

Guidelines for buttons :
http://www.google.com/design/spec/components/buttons.html
"""

import sys
sys.path.append( '..' )

from kivy.animation import Animation
from kivy.adapters.listadapter import ListAdapter
from kivy.base import EventLoop
from kivy.config import Config
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput

import pdb

#from flatui.labels import BindedLabel
from . import labels

from pkg_resources import resource_filename
#KV Files
path = resource_filename( __name__, 'flatui.kv' )
Builder.load_file( path )


class FlatTextInput( TextInput ) :
    '''
    Flat version of the standard TextInput.
    '''

    show_underline = BooleanProperty( True )
    '''
    If true a line of the same color of the cursor will be drawn under the text.
    '''

    cursor_color = ListProperty( [ 1, 0, 0, .8 ] )
    '''Represents the rgba color used to render the cursor.

    .. versionadded:: 1.0

    :attr:`cursor_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ 1, 0, 0, .8 ].
    '''

    def __init__( self, **kargs ) :
        if not 'background_color' in kargs.keys() :
            kargs['background_color'] = [0,0,0,0]
        super( FlatTextInput, self ).__init__( **kargs )


class _MaterialButton( ButtonBehavior, labels.BindedLabel ) :
    '''
    Replacement for Button class, just more flexible...
    '''

    background_color = ListProperty( [1, 1, 1, 1] )
    '''Represents the rgba color used to render the frame in the normal state.

    .. versionadded:: 1.0

    The :attr:`background_color` is a
    :class:`~kivy.properties.ListProperty` and defaults to [1, 1, 1, 1].
    '''

    background_color_down = ListProperty( [ 0.2, 0.65, 0.81, 1 ] )
    '''Represents the rgba color used to render the frame in the down state.

    .. versionadded:: 1.0

    :attr:`background_color_down` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ 0.2, 0.65, 0.81, 0.5 ] ( cyano with alpha ).
    '''

    color_down = ListProperty( [ 0, 0, 0, .7 ] )
    '''Represents the rgba color used to render the button text in the down state.

    .. versionadded:: 1.0

    :attr:`color_down` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ .3, .3, .3, 1 ] ( cyano with alpha ).
    '''

    background_color_disabled = ListProperty( [ 0.4, 0.4, 0.4, 0.5 ] )
    '''Represents the rgba color used to render the button when disabled.

    .. versionadded:: 1.0

    :attr:`background_color_down` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ 0.4, 0.4, 0.4, 0.5 ] ( grey with alpha ).
    '''

    icon = StringProperty( '' )
    '''Icon image file.

    .. versionadded:: 1.0

    :attr:`icon` is a :class:`~kivy.properties.StringProperty`, default to ''.
    '''

    shadow_alpha = NumericProperty( 0.05 )
    '''Alpha channel used to render the rgba shadow.

    .. versionadded:: 1.0

    :attr:`shadow_alpha` is a :class:`~kivy.properties.NumericProperty`, default to 0.4.
    '''

    corner_radius = NumericProperty( dp(2) )
    '''Button corner radius.

    .. versionadded:: 1.0

    :attr:`corner_radius` is a :class:`~kivy.properties.NumericProperty`.
    '''
    
    def __init__( self, **kargs ) :
        if not 'valign' in kargs.keys() : kargs['valign'] = 'middle'
        if not 'halign' in kargs.keys() : kargs['halign'] = 'center'
        super( _MaterialButton, self ).__init__( **kargs )


class FlatButton( _MaterialButton ) :
    '''
    Material UI flat button.
    '''

    pass

class RaisedButton( _MaterialButton ) :
    '''
    Material UI raised button.
    '''
   
    pass


class FloatingAction( _MaterialButton ) :
    '''
    Round button with frame.
    '''

    diameter = NumericProperty( dp(1) )
    '''Represents the diameter of the button. 
    Will update widget size.

    .. versionadded:: 1.0

    :attr:`diameter` is a :class:`~kivy.properties.NumericProperty`.
    '''

    shadow_offset_x = NumericProperty( 0 )
    '''Use this to move the shadow.

    .. versionadded:: 1.0

    :attr:`shadow_offset_x` is a :class:`~kivy.properties.NumericProperty`, default to 0.
    '''

    shadow_offset_y = NumericProperty( dp(1) )
    '''Use this to move the shadow.

    .. versionadded:: 1.0

    :attr:`shadow_offset_y` is a :class:`~kivy.properties.NumericProperty`, default to 1.
    '''

    animation_duracy = NumericProperty( .1 )
    '''Used to move button when loading a new view

    .. versionadded:: 1.0

    :attr:`animation_duracy` is a :class:`~kivy.properties.NumericProperty`, default to 0.1.
    '''

    entrance = OptionProperty('', options=['', 'down', 'up', 'left','right'])
    '''Direction the button will come from.

    :attr:`entrance` is a :class:`~kivy.properties.OptionProperty` and
    defaults to ''. Available options are '', down, up, left, right
    '''

    def __init__( self, **kargs ) :

        if not 'diameter' in kargs.keys() : 
            kargs[ 'diameter' ] = dp(56)

        if not 'color' in kargs.keys() : 
            kargs[ 'color' ] = [ 1, 1, 1, 1 ]

        if not 'background_color' in kargs.keys() : 
            kargs[ 'background_color' ] = [ 0.88, 0.2, 0.15, 1 ]

        if not 'background_color_down' in kargs.keys() : 
            kargs[ 'background_color_down' ] = [ 0.88, 0.3, 0.2, 1 ]

        super( FloatingAction, self ).__init__( **kargs )

    def add_to_bottom_right( self, parent ) : 

        nx = parent.width-self.diameter*1.2
        ny = self.diameter*0.3

        parent.bind( size=self._repose )
        parent.add_widget( self )

        duracy = self.animation_duracy if self.entrance != '' else 0

        if duracy > 0 :
            if self.entrance == 'down'  : self.pos = [ nx, -self.height ]
            if self.entrance == 'up'    : self.pos = [ nx, self.pos[1]+self.height ]
            if self.entrance == 'left'  : self.pos = [ -self.width, ny ]
            if self.entrance == 'right' : self.pos = [ +self.width, ny ]

            animation = Animation( x=nx, y=ny, duration=duracy )
            animation.start( self ) 
        else :
            self.pos = nx, ny
        self.parent = parent
 
    def remove_from_parent( self ) :  
        duracy = self.animation_duracy if self.entrance != '' else 0
        nx, ny = self.pos
    
        if self.entrance == 'down'  : ny = 0
        if self.entrance == 'up'    : ny = self.parent.height+self.height
        if self.entrance == 'left'  : nx = -self.width
        if self.entrance == 'right' : nx = self.parent.width

        animation = Animation( x=nx, y=ny, duration=duracy )
        animation.bind( on_complete=self._remove_from_parent )
        animation.start( self ) 

    def _remove_from_parent( self, *args ) :
        self.parent.unbind( size=self._repose )
        self.parent.remove_widget( self )
    
    def _repose( self, i, v ) :
        self.pos = [ v[0]-self.diameter*1.2, self.diameter*0.3 ]

















