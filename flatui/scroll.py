#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = "1.0.0"

import pdb
import sys
import traceback

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.graphics.context_instructions import PopMatrix, PushMatrix, Rotate
from kivy.graphics.instructions import *
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.metrics import dp, sp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from pkg_resources import resource_filename

#KV Files
path = resource_filename( __name__, 'scroll.kv' )
Builder.load_file( path )

#Resources
spinner_image_default = resource_filename( __name__, 'spinner.png' )


class _RefreshScrollEffect( DampedScrollEffect ) :
    '''
    This class is simply based on DampedScrollEffect.
    If you need any documentation please look at kivy.effects.dampedscrolleffect.
    '''

    min_scroll_to_reload = NumericProperty( -dp(100) )
    '''
    Minimum overscroll value to reload.
    '''

    def on_overscroll( self, scrollview, overscroll ) :
        if overscroll < self.min_scroll_to_reload :
            scroll_view = self.target_widget.parent
            scroll_view._did_overscroll = True
            return True
        else : return False


class RefreshableScrollView( ScrollView ) :
    '''
    This is a very simple subclass of ScrollView.
    When the user does overscroll the view, a 'ReloadSpinner' is shown.
    You will need to call 'reload_done' once you've dove your loading.
    A ReloadSpinner widget will be added to the root_layout (you can choose ReloadSpinner class to use).
    '''

    on_start_reload = ObjectProperty( None )
    '''
    Will be called whenever overscroll occurs.
    '''
    
    spinner_class = StringProperty( 'LollipopSpinner' )
    '''
    Different class means a different effect.
    For a spinning image, for example, use ImageSpinner.
    By default class is 'LollipopSpinner', based on the latest android GMail app spinner.
    Class loading is done using eval, be careful.
    '''

    spinner_image = StringProperty( spinner_image_default )
    '''
    Set this property to change spinner appearance.
    '''
    
    spinner_diameter = NumericProperty( dp(38) )
    '''
    Size of the spinner
    '''

    spinner_duracy = NumericProperty( .2 )
    '''
    Spinner entrance\exit animation duracy
    '''
    
    root_layout = ObjectProperty( None )
    '''
    The spinner will be attached to this layout.
    ''' 

    spinner_speed = NumericProperty( 12 )
    '''
    Angle of rotation per-frame used by the spinner
    ''' 

    spinner_shadow_alpha = NumericProperty( .05 )
    '''
    Value of the shadow alpha channel.
    ''' 

    reload_spinner = ObjectProperty( None )
    '''
    Spinner widget reference used internally
    ''' 

    def __init__( self, **kargs ) :
        super( RefreshableScrollView, self ).__init__( **kargs )
        self.effect_cls = _RefreshScrollEffect
        self._reloading = False
        self._did_overscroll = False

    def on_touch_up( self, *args ) :
        if self._did_overscroll and not self._reloading :
            if self.on_start_reload : self.on_start_reload()
            self.reload_spinner = self._spinner_class()( 
                root_layout=self.root_layout,
                spinner_image=self.spinner_image,
                shadow_alpha=self.spinner_shadow_alpha,
                diameter=self.spinner_diameter,
                duracy=self.spinner_duracy,
                speed=self.spinner_speed
            )
            self.reload_spinner.start()     
            self._reloading = True
            self._did_overscroll = False
            return True
        
        return super( RefreshableScrollView, self ).on_touch_up( *args )

    def reload_done( self, *args ) :        
        self._reloading = False
        if self.reload_spinner : self.reload_spinner.stop()
    
    def _spinner_class( self ) :
        return eval( self.spinner_class ) 


class ReloadSpinner( Widget ) :
    '''
    Override this class if you want a custom spinner.
    There are fiew thigs to now :
        - Canvas is centered in the spinner center!
        - You need to PopMatrix when you're done drawing content
    See scroll.kv for more informations.
    '''

    spinner_image = StringProperty( 'spinner.png' )
    '''
    Set this property to change spinner appearance.
    '''

    shadow_alpha = NumericProperty( .05 )
    '''
    Value of the shadow alpha channel.
    ''' 

    root_layout = ObjectProperty( None )
    '''
    The spinner will be attached to this layout.
    ''' 
    
    diameter = NumericProperty( dp(48) )
    '''
    Size of the spinner.
    '''

    duracy = NumericProperty( .2 )
    '''
    Animation duracy.
    '''

    speed = NumericProperty( 6 )
    '''
    Angle of rotation increment.
    '''

    angle = NumericProperty( 0 )
    '''
    Current rotation.
    '''
    
    on_update_animation = ObjectProperty( None )
    '''
    Called after update_animation.
    '''

    def __init__( self, **kargs ) :
        super( ReloadSpinner, self ).__init__( **kargs )
    
    def update_animation( self, *args ) :
        self.angle += self.speed
        if self.angle >= 360 : self.angle = 0
        if self.on_update_animation : self.on_update_animation( self, *args )
    
    def start( self ) :

        self.pos = ( 
            self.root_layout.width/2 - self.width/2, 
            self.root_layout.height+self.height
        )

        animation = Animation( 
            y=self.root_layout.height-2*self.height, 
            duration=self.duracy
        )
        animation.start( self )         

        self.angle = 0
        self._hex = 0
        self._color = 0, 0, 0, 1 
        self.root_layout.add_widget( self )
        Clock.schedule_interval( self.update_animation, 0.04 )
    
    def stop( self ) : 
        animation = Animation( 
            y=self.root_layout.height-2*self.height, 
            duration=self.duracy
        )
        animation.bind(
            on_complete=self._remove_animation_done
        )
        animation.start( self )         

    def _remove_animation_done( self, *args ) :
        self.root_layout.remove_widget( self )
        Clock.unschedule( self.update_animation )


class ImageSpinner( ReloadSpinner ) :
    '''
    Based on the default spinner, kv lang provides image rendering.
    '''
    pass


class LollipopSpinner( ReloadSpinner ) :
    '''
    Based on the android gmail app spinner.
    '''

    color = ListProperty( [ 0, 0, 0, 1 ] )
    '''
    Current color of the inner arrow.
    '''

    angle2 = NumericProperty( 0 )
    '''
    Secon angle of rotation, will move slower.
    '''

    colors = ListProperty( [ [.051,.635,.376,1], [.867,.314,.267,1], [.227,.494,.953,1], [.969,.773,.253,1] ] )
    '''
    Colors to use.
    '''

    def __init__( self, **kargs ) :
        self._current_color = 0
        self.color = self.colors[ self._current_color ]     

        kargs['on_update_animation'] = self.update_angle2
        kargs['speed'] = 15
        super( LollipopSpinner, self ).__init__( **kargs )

    def update_angle2( self, *args ) :
        self.angle2 -= self.speed / 2.0
        if abs(self.angle2) == 360 : self.angle2 = 0

        if self.angle == self.angle2 == 0 :
            self._current_color += 1
            if self._current_color == len( self.colors ) : self._current_color = 0
            self.color = self.colors[ self._current_color ]     
        













