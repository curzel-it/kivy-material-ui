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
from kivy.uix.popup import PopupException
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
            kargs[ 'background_color' ] = [ 0.9, 0.2, 0.15, 1 ]

        if not 'background_color_down' in kargs.keys() : 
            kargs[ 'background_color_down' ] = [ 0.9, 0.3, 0.2, 1 ]

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


class PopupComboBox( Label ) :
    '''
    When a click on this button occur, a popup will be shown to pick a value.
    Arguments named popup_* will be passed down to the popup for customizations.

    To customize ListItemButton selected_color and deselected_color please use kv lang.
    '''

    popup = ObjectProperty( None )
    '''Use this property to access the popup object for customizations.

    .. versionadded:: 1.0

    :attr:`popup` is a :class:`~kivy.properties.ObjectProperty`.
    '''

    item_row_height = NumericProperty( dp(40) )
    '''Height of rows shown by the popup

    .. versionadded:: 1.0

    :attr:`item_row_height` is a :class:`~kivy.properties.NumericProperty`, default to 40.
    '''

    popup_args = DictProperty( None )
    '''Use this property to pass down parameters to the popup for customizations.

    .. versionadded:: 1.0

    :attr:`popup_args` is a :class:`~kivy.properties.DictProperty`, default to {}.
    '''

    selected = ObjectProperty( None )
    '''Bind this property to your on-selection function.

    .. versionadded:: 1.0

    :attr:`selected` is a :class:`~kivy.properties.ObjectProperty`.
    '''

    def __init__( self, **kargs ) :

        super( PopupComboBox, self ).__init__( **kargs )

        self.list_data = self.build_list_data( kargs['list_data'] )
        self.popup = FlatPopup( **self._popup_args( kargs ) )
        self.popup.content = self._build_list_view( kargs )

        self.on_selection = kargs['on_selection'] if 'on_selection' in kargs.keys() else None

        self.bind( text=self._fix_text_with_ref )
        self.bind( on_ref_press=self.show_choice )


    def _popup_args( self, kargs ) :
        return kargs['popup_args'] if 'popup_args' in kargs.keys() else {}

    def _build_list_view( self, kargs ) :
        self._list_view = ListView( 
            adapter=self._build_adapter(), 
            propagate_selection_to_data=True
        )
        return self._list_view

    def _fix_text_with_ref( self, label, text ) :
        if not text.startswith( '[ref=' ) :
            self.text = '[ref=main]%s[/ref]' % ( text ) 

    def build_list_data( self, data ) :
        if len( data ) > 0 :
            if data[0].__class__ == str :
                l2dict = [ {'is_selected':False,'rowid':0,'label':x} for x in data ]
                return self.build_list_data( l2dict )
            else :
                result = data
                if 'is_selected' not in data[0].keys() :
                    result = []
                    for x in data :
                        x['is_selected'] = False
                        result.append( x )
                return result
        return []

    def show_choice( self, *args ) :
        self.popup.open()

    def adapter_converter( self ) :
        return lambda i, o : { \
            'is_selected'      : o['is_selected'], \
#            'selected_color'   : self.selected_color, \
#            'deselected_color' : self.deselected_color, \
            'size_hint_y'      : None, \
            'height'           : self.item_row_height, \
#            'font_size'        : dp(12), \
#            'font_name'        : self.font_name, \
            'text'             : o['label'], \
            'rowid'            : o['rowid'] \
        }

    def _build_adapter( self ) :
        self.list_adapter = ListAdapter( 
            cls                   = ListItemButton,
            data                  = self.list_data,
            args_converter        = self.adapter_converter(),
            selection_mode        = 'single',
            allow_empty_selection = True 
        )
        self.list_adapter.bind( on_selection_change=self.on_selection_change )
        return self.list_adapter

    def on_selection_change( self, adapter, *args ) : 
        if ( adapter.selection ) :
            self.selected = self.list_data[ adapter.selection[0].index ]
            self.text = self.selected['label']
            self.on_selection( self )
            self.popup.dismiss()

    def select( self, i ) :
        self.text = self.list_data[ i ][ 'label' ]
        self.list_adapter.get_view(i).trigger_action( duration=0 )


class FlatPopup(ModalView) :
    '''Code copy-pasted from kivy.uix.popup, just some more properties.
    '''

    title = StringProperty('No title')
    '''String that represents the title of the popup.

    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to
    'No title'.
    '''

    title_size = NumericProperty( dp(14) )
    '''Represents the font size of the popup title.

    .. versionadded:: 1.6.0

    :attr:`title_size` is a :class:`~kivy.properties.NumericProperty` and
    defaults to '14sp'.
    '''

    title_align = OptionProperty('left', options=['left', 'center', 'right','justify'])
    '''Horizontal alignment of the title.

    :attr:`title_align` is a :class:`~kivy.properties.OptionProperty` and
    defaults to 'left'. Available options are left, middle, right and justify.
    '''

    title_font = StringProperty( 'DroidSans' )
    '''Font used to render the title text.

    :attr:`title_font` is a :class:`~kivy.properties.StringProperty`.
    '''

    content = ObjectProperty(None)
    '''Content of the popup that is displayed just under the title.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    title_color = ListProperty([1, 1, 1, 1])
    '''Color used by the Title.

    .. versionadded:: 1.8.0

    :attr:`title_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [1, 1, 1, 1].
    '''

    separator_color = ListProperty([47 / 255., 167 / 255., 212 / 255., 1.])
    '''Color used by the separator between title and content.

    .. versionadded:: 1.1.0

    :attr:`separator_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [47 / 255., 167 / 255., 212 / 255., 1.]
    '''

    separator_height = NumericProperty( dp(2) )
    '''Height of the separator.

    .. versionadded:: 1.1.0

    :attr:`separator_height` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 2dp.
    '''

    close_on_esc = BooleanProperty( True )
    '''If false keyboard is not binded and popup is not closed by key events.

    .. versionadded:: 1.0.0

    :attr:`close_on_esc` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True.
    '''

    is_shown = BooleanProperty( False )
    '''
    True whenever the popup is visibile
    '''

    # Internal properties used for graphical representation.
    _container = ObjectProperty( None )

    def __init__( self, **kargs ) :

        if not 'separator_height' in kargs.keys() : 
            kargs['separator_height'] = 0
        super( FlatPopup, self ).__init__( **kargs )

    def open(self, *args, **kargs) :
        super( FlatPopup, self ).open( *args, **kargs )
        self.is_shown = True
        if self.close_on_esc : self._bind_keyboard()

    def dismiss(self, *args, **kargs) :
        self.is_shown = False
        super( FlatPopup, self ).dismiss( *args, **kargs )

    def _bind_keyboard(self) :
        EventLoop.window.bind( on_key_down=self._on_keyboard_down)

    def _on_keyboard_down( self, window, key, *args ) :
        if self.is_shown and key == 27 : #Escape
            self.dismiss()
            return True
        return False

    def add_widget(self, widget):
        if self._container:
            if self.content:
                raise PopupException(
                    'Popup can have only one widget as content')
            self.content = widget
        else:
            super(FlatPopup, self).add_widget(widget)

    def on_content(self, instance, value):
        if not hasattr(value, 'popup'):
            value.create_property('popup')
        value.popup = self
        if self._container:
            self._container.clear_widgets()
            self._container.add_widget(value)

    def on__container(self, instance, value):
        if value is None or self.content is None:
            return
        self._container.clear_widgets()
        self._container.add_widget(self.content)

    def on_touch_down(self, touch):
        if self.disabled and self.collide_point(*touch.pos):
            return True
        return super(FlatPopup, self).on_touch_down(touch)













