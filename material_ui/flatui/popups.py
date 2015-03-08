import sys

from kivy.animation import Animation
from kivy.adapters.listadapter import ListAdapter
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

#from flatui.flatui import FlatButton, FlatPopup
from . import flatui

import pkg_resources

path = pkg_resources.resource_filename( __name__, 'popups.kv' )
Builder.load_file( path )


class AlertPopup( flatui.FlatPopup ) :
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



class OkButtonPopup( flatui.FlatPopup ) :
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
        
