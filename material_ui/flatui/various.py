"""
From Google Guidelines : 

Single-line SnackBar height: 48dp
Multi-line SnackBar height: 80dp
Text: Roboto Regular 14sp
Action button: Roboto Medium 14sp, all-caps text
Default background fill: #323232 100%
"""

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.label import Label

from pkg_resources import resource_filename
path = resource_filename( __name__, 'various.kv' )
Builder.load_file( path )

from . import labels

class SnackBar( labels.BindedLabel ) :
    '''
    Material UI SnackBar.
    '''

    alpha          = NumericProperty( 1 )
    duration_short = NumericProperty( 2000 )
    duration_long  = NumericProperty( 3500 )

    def __init__( self, **kargs ) :
        self._bound = False
        super( SnackBar, self ).__init__( **kargs )
        self.color      = [ 1, 1, 1, 1 ]
        self.fill_color = [ .1961, .1961, .1961, 1 ]
        self.size_hint  = 1, None
        self.height = dp(80) if '\n' in self.text else dp(48)
    
    def show( self, isLong, *args ) :
        duration = self.duration_long if isLong else self.duration_short
        timeout_down = duration * 0.1
        if timeout_down > 500 : timeout_down = 500
        if timeout_down < 100 : timeout_down = 100
        self._timeout_down = timeout_down
        self._duration = duration - timeout_down
        Window.add_widget(self)
        Clock.schedule_interval(self.animate, 1/60.0)
        
    def realign( self, window, size ) :
        self.x = (size[0] - self.width) / 2.0
        self.y = size[1] * 0.1

    def animate( self, dt ) :
        self._duration -= dt * 1000
        if self._duration <= 0:
            self.alpha = 1.0 + (self._duration / self._timeout_down)
        if -(self._duration) > self._timeout_down:
            Window.remove_widget(self)
            return False

"""
def do_toast( text, **kargs ):
    isLong = kargs['isLong'] if 'isLong' in kargs.keys() else False
    Toast( text=text, **kargs ).show( isLong )
"""

def do_snack( text, **kargs ):
    isLong = kargs['isLong'] if 'isLong' in kargs.keys() else False
    SnackBar( text=text, **kargs ).show( isLong )
