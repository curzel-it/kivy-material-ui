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

path = pkg_resources.resource_filename( __name__, 'popups.kv' )
Builder.load_file( path )


class FlatPopup(ModalView):
    '''Code copy-pasted from kivy.uix.popup, just some more properties.
    '''

    title = StringProperty('No title')
    '''String that represents the title of the popup.

    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to
    'No title'.
    '''

    title_size = NumericProperty('14sp')
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

    title_font = StringProperty('DroidSans')
    '''Font used to render the title text.

    :attr:`title_font` is a :class:`~kivy.properties.StringProperty` and
    defaults to 'DroidSans'.
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

    separator_height = NumericProperty('2dp')
    '''Height of the separator.

    .. versionadded:: 1.1.0

    :attr:`separator_height` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 2dp.
    '''

    # Internal properties used for graphical representation.

    _container = ObjectProperty(None)

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


class AlertPopup( FlatPopup ) :
    """
    Quick flat popup to show a generic alert message.
    Provide cancel_button_text or cancel_button_on_press to show a second button.
    """

    ok_button_text = StringProperty( 'OK' )
    cancel_button_text = StringProperty( 'No' )
    text = StringProperty( 'No text argument was provided.' )
    ok_button_on_press = ObjectProperty( None )
    cancel_button_on_press = ObjectProperty( None )

    def __init__( self, **kargs ) :

        if not 'title' in kargs.keys() : kargs['title'] = 'Warning'
        if not 'title_size' in kargs.keys() : kargs['title_size'] = 16
        if not 'size_hint' in kargs.keys() : kargs['size_hint'] = (.4,.3)
        if not 'title_color' in kargs.keys() : kargs['title_color'] = (0,0,0,.8)

        super( AlertPopup, self ).__init__( **kargs )

        ok_button = Button( text=self.ok_button_text )
        ok_button.bind( on_press=self.on_ok )
        
        cancel_button = Button( text=self.cancel_button_text )
        cancel_button.bind( on_press=self.on_cancel )

        button_bar = BoxLayout( orientation='horizontal', size_hint=(1,.1) )
        button_bar.add_widget( BoxLayout() )
        button_bar.add_widget( cancel_button )
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

