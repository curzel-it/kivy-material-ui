import sys

from kivy.animation import Animation
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.behaviors import ButtonBehavior
from kivy.base import EventLoop
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.modalview import ModalView
from kivy.uix.popup import PopupException
from kivy.uix.textinput import TextInput

from . import flatui

import pkg_resources

path = pkg_resources.resource_filename( __name__, 'popups.kv' )
Builder.load_file( path )


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
                raise PopupException('Popup can have only one widget as content')
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


class AlertPopup( FlatPopup ) :
    """
    Quick flat popup to show a generic alert message.
    Provide cancel_button_text or cancel_button_on_press to show a second button.
    """

    text = StringProperty( 'No text argument was provided.' )

    ok_button_text = StringProperty( '[b]OK[/b]' )
    ok_button_text_color = ListProperty( [1,1,1,1] )
    ok_button_on_press = ObjectProperty( None )
    ok_button_color = ListProperty( [0,.59,.53,1] )
    ok_button_color_down = ListProperty( [0,.41,.36,1] )

    cancel_button_text = StringProperty( None )
    cancel_button_text_color = ListProperty( [1,1,1,1] )
    cancel_button_on_press = ObjectProperty( None )
    cancel_button_color = ListProperty( [0,.59,.53,1] )
    cancel_button_color_down = ListProperty( [0,.41,.36,1] )

    def __init__( self, **kargs ) :

        if not 'title'       in kargs.keys() : kargs['title'      ] = 'Warning'
        if not 'title_size'  in kargs.keys() : kargs['title_size' ] = dp(16)
        if not 'size_hint'   in kargs.keys() : kargs['size_hint'  ] = (.4,.3)
        if not 'title_color' in kargs.keys() : kargs['title_color'] = (0,0,0,.8)

        super( AlertPopup, self ).__init__( **kargs )

        ok_button = flatui.FlatButton( 
            text=self.ok_button_text,
            markup=True,
            color=self.ok_button_color,
            color_down=self.ok_button_color_down 
        )
        ok_button.bind( on_press=self.on_ok )
        
        cancel_button = flatui.FlatButton( 
            text=self.cancel_button_text or '',
            markup=True,
            color=self.cancel_button_color,
            color_down=self.cancel_button_color_down 
        )
        cancel_button.bind( on_press=self.on_cancel )

        button_bar = BoxLayout( 
            orientation='horizontal',\
            size_hint=(1,None), height=dp(55),\
            spacing=dp(10), padding=[10,10,10,10] 
        )
        button_bar.add_widget( BoxLayout() )
        if self.cancel_button_text : button_bar.add_widget( cancel_button )
        button_bar.add_widget( ok_button )

        self.content = BoxLayout( orientation='vertical' )        
        lbl = Label( text=self.text, size_hint=(1,.9), color=self.title_color )
        self.content.add_widget( lbl )
        self.content.add_widget( button_bar )
        
    def on_ok( self, *args ) :
        self.dismiss()
        if self.ok_button_on_press : self.ok_button_on_press( *args )
        
    def on_cancel( self, *args ) :
        self.dismiss()
        if self.cancel_button_on_press : self.cancel_button_on_press( *args )



class OkButtonPopup( FlatPopup ) :
    """
    Quick flat popup to show a generic hint to the user.
    Has and OK button to dismiss itself and nothing more
    """

    ok_button_text = StringProperty( '[b]OK[/b]' )
    text = StringProperty( 'No text argument was provided.' )
    ok_button_color = ListProperty( [0,.59,.53,1] )
    ok_button_text_color = ListProperty( [1,1,1,1] )
    ok_button_color_down = ListProperty( [0,.41,.36,1] )

    def __init__( self, **kargs ) :

        if not 'title'       in kargs.keys() : kargs['title'      ] = 'Info'
        if not 'title_size'  in kargs.keys() : kargs['title_size' ] = dp(16)
        if not 'size_hint'   in kargs.keys() : kargs['size_hint'  ] = (.8,.5)
        if not 'title_color' in kargs.keys() : kargs['title_color'] = (0,0,0,.8)

        super( OkButtonPopup, self ).__init__( **kargs )

        ok_button = flatui.FlatButton( 
            text=self.ok_button_text,
            markup=True,
            size_hint=(.2,1),
            color=self.ok_button_color,
            color_down=self.ok_button_color_down 
        )
        ok_button.bind( on_press=self.on_ok )

        button_bar = BoxLayout( 
            orientation='horizontal',\
            size_hint=(1,None), height=dp(55),\
            spacing=dp(10), padding=[10,10,10,10]
        )
        button_bar.add_widget( BoxLayout( size_hint=(.8,1) ) )
        button_bar.add_widget( ok_button )

        self.content = BoxLayout( orientation='vertical' )        
        lbl = Label( text=self.text, color=self.title_color, size_hint=(1,.8) )
        self.content.add_widget( lbl )
        self.content.add_widget( button_bar )
        
    def on_ok( self, *args ) :
        self.dismiss()

        
class PopupListView( FlatPopup ) :
    '''
    When a click on this button occur, a popup will be shown to pick a value.
    Arguments named popup_* will be passed down to the popup for customizations.

    To customize ListItemButton selected_color and deselected_color please use kv lang.
    '''

    item_row_height = NumericProperty( dp(40) )
    '''Height of rows shown by the popup

    .. versionadded:: 1.0

    :attr:`item_row_height` is a :class:`~kivy.properties.NumericProperty`, default to 40.
    '''

    selected = ObjectProperty( None )
    '''Bind this property to your on-selection function.

    .. versionadded:: 1.0

    :attr:`selected` is a :class:`~kivy.properties.ObjectProperty`.
    '''

    on_selection = ObjectProperty( None )
    '''Called whenever a value is selected, see 'on_selection_change' method code.

    .. versionadded:: 1.0

    :attr:`on_selection` is a :class:`~kivy.properties.ObjectProperty`.
    '''

    def __init__( self, list_data, **kargs ) :
        super( PopupListView, self ).__init__( **kargs )
        #if len(list_data) == 0 : raise ValueError( 'Empty list data.' )
        self.list_data = self.build_list_data( list_data )
        self.content = self._build_list_view( kargs )

    def _build_list_view( self, kargs ) :
        self._list_view = ListView( 
            adapter=self._build_adapter(), 
            propagate_selection_to_data=True
        )
        return self._list_view

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

    def show_choices( self, *args ) :
        self.open()

    def adapter_converter( self ) :
        return lambda i, o : { \
            'is_selected'      : o['is_selected'], \
            'size_hint_y'      : None, \
            'height'           : self.item_row_height, \
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
            if self.on_selection : self.on_selection( self )
            self.dismiss()

    def select( self, i ) :
        self.list_adapter.get_view(i).trigger_action( duration=0 )


class PopupComboBox( flatui.FlatButton ) :
    '''
    When a click on this widget occur, a popup will be shown to pick a value.
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

    popup_args = DictProperty( {} )
    '''Use this property to pass down parameters to the popup for customizations.

    .. versionadded:: 1.0

    :attr:`popup_args` is a :class:`~kivy.properties.DictProperty`, default to {}.
    '''

    selected = ObjectProperty( None )
    '''Bind this property to your on-selection function.

    .. versionadded:: 1.0

    :attr:`selected` is a :class:`~kivy.properties.ObjectProperty`.
    '''
    
    list_data = ListProperty( [] )
    '''Used to store data...

    .. versionadded:: 1.2

    :attr:`list_data` is a :class:`~kivy.properties.ListProperty`.
    '''

    def __init__( self, **kargs ) :

        super( PopupComboBox, self ).__init__( **kargs )
        self.bind( on_press=self.show_choices )
        self.bind( list_data=self.feed_data )

    def feed_data( self, i, data ) :
        self.list_data = data
        self.popup = PopupListView( self.list_data, **self.popup_args )

    def show_choices( self, *args ) :
        self.popup.show_choices()

