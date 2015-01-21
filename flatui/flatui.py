from kivy.adapters.listadapter import ListAdapter
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.modalview import ModalView
from kivy.uix.popup import PopupException
from kivy.uix.textinput import TextInput

import pkg_resources

path = pkg_resources.resource_filename( __name__, 'flatui.kv' )
Builder.load_file( path )


class FlatTextInput( TextInput ) :
    '''
    Flat version of the standard TextInput.
    '''

    show_underline = BooleanProperty( True )
    '''
    If true a line of the same color of the cursor will be drawn under the text.
    '''

    cursor_color = ListProperty( [ 1, 0, 0, 1 ] )
    '''Represents the rgba color used to render the cursor.

    .. versionadded:: 1.0

    :attr:`cursor_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ 1, 0, 0, 1 ] ( red ).
    '''

    def __init__( self, **kargs ) :
        if not 'background_color' in kargs.keys() :
            kargs['background_color'] = [0,0,0,0]
        super( FlatTextInput, self ).__init__( **kargs )


class _ColorButton( Button ) :

    background_color_down = ListProperty( [ 0.2, 0.65, 0.81, 1 ] )
    '''Represents the rgba color used to render the frame in the normal state.

    .. versionadded:: 1.0

    :attr:`background_color_down` is a :class:`~kivy.properties.ListProperty` and
    defaults to [ 0.2, 0.65, 0.81, 0.5 ] ( cyano with alpha ).
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

    shadow_alpha = NumericProperty( 0.5 )
    '''Alpha channel used to render the rgba shadow.

    .. versionadded:: 1.0

    :attr:`shadow_alpha` is a :class:`~kivy.properties.NumericProperty`, default to 0.4.
    '''
    

class FlatButton( _ColorButton ) :
    '''
    Completely flat button.
    '''

    corner_radius = NumericProperty( 2 )
    '''Button corner radius.

    .. versionadded:: 1.0

    :attr:`corner_radius` is a :class:`~kivy.properties.NumericProperty`.
    '''

    def __init__( self, **kargs ) :
        super( FlatButton, self ).__init__( **kargs )


class FloatingAction( _ColorButton ) :
    '''
    Round button with frame.
    '''

    diameter = NumericProperty( 1 )
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

    shadow_offset_y = NumericProperty( 1 )
    '''Use this to move the shadow.

    .. versionadded:: 1.0

    :attr:`shadow_offset_y` is a :class:`~kivy.properties.NumericProperty`, default to 1.
    '''

    shadow_ratio = NumericProperty( 1.03 )
    '''Used to get a bigger shadow.

    .. versionadded:: 1.0

    :attr:`shadow_ratio` is a :class:`~kivy.properties.NumericProperty`, default to 1.03.
    '''

    def __init__( self, **kargs ) :

        if not 'color' in kargs.keys() : 
            kargs[ 'color' ] = [ 1, 1, 1, 1 ]
        super( FloatingAction, self ).__init__( **kargs )


class PopupComboBox( Label ) :
    '''
    When a click on this button occur, a popup will be shown to pick a value.
    Arguments named popup_* will be passed down to the popup for customizations.
    '''

    popup = ObjectProperty( None )
    '''Use this property to access the popup object for customizations.

    .. versionadded:: 1.0

    :attr:`popup` is a :class:`~kivy.properties.ObjectProperty`.
    '''

    item_row_height = NumericProperty( 40 )
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
        self.popup = Popup( **self._popup_args( kargs ) )
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
            'selected_color'   : [ 0.2, 0.65, 0.81, 1 ], \
            'deselected_color' : [ 1, 1, 1, 1 ], \
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
            self.text = self.selected['label']
            self.on_selection( self )
            self.popup.dismiss()

    def select( self, i ) :
        self.text = self.list_data[ i ][ 'label' ]
        self.list_adapter.get_view(i).trigger_action( duration=0 )














