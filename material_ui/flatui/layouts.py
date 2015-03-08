import sys
sys.path.append( '..' )

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout

#from flatui.labels import BindedLabel
from . import labels

from pkg_resources import resource_filename
#KV Files
path = resource_filename( __name__, 'layouts.kv' )
Builder.load_file( path )


class ColorAnchorLayout( AnchorLayout ) :
    '''
    Just an AnchorLayout with a background color.
    '''
    
    background_color = ListProperty( [0,0,0,0] )
    '''
    Used in canvas.before as background color.
    '''

class ColorBoxLayout( BoxLayout ) :
    '''
    Just a BoxLayout with a background color.
    '''
    
    background_color = ListProperty( [0,0,0,0] )
    '''
    Used in canvas.before as background color.
    '''

class ColorFloatLayout( FloatLayout ) :
    '''
    Just a FloatLayout with a background color.
    '''
    
    background_color = ListProperty( [0,0,0,0] )
    '''
    Used in canvas.before as background color.
    '''

class ColorRelativeLayout( RelativeLayout ) :
    '''
    Just a RelativeLayout with a background color.
    '''
    
    background_color = ListProperty( [0,0,0,0] )
    '''
    Used in canvas.before as background color.
    '''

class ColorGridLayout( GridLayout ) :
    '''
    Just a GridLayout with a background color.
    '''
    
    background_color = ListProperty( [0,0,0,0] )
    '''
    Used in canvas.before as background color.
    '''

class ColorStackLayout( StackLayout ) :
    '''
    Just a StackLayout with a background color.
    '''
    
    background_color = ListProperty( [0,0,0,0] )
    '''
    Used in canvas.before as background color.
    '''

