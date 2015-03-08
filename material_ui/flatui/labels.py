import sys
sys.path.append( '..' )

from copy import copy, deepcopy

import kivy.graphics as kg
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

#KV Lang files
from pkg_resources import resource_filename
path = resource_filename( __name__, 'labels.kv' )

Builder.load_file( path )

TOP_LEFT, LEFT, BOTTOM_LEFT = 0, 1, 2
TOP, BOTTOM, CENTER = 3, 4, 5
TOP_RIGHT, RIGHT, BOTTOM_RIGHT = 6, 7, 8

class BindedLabel( Label ) :
    '''
    Standard label with some additions :
        - Binded text_size to size ( so you can center text )
        - Background color
        - Some more user-friendly padding usage
    '''

    fill_color = ListProperty( [0,0,0,0] )

    def __init__( self, **kargs ) : 
        t = str( kargs['text'] if 'text' in kargs.keys() else '' )
        kargs['text'] = str( t )
        super( BindedLabel, self ).__init__( **kargs )    
        self.bind( size=self.setter('text_size') )


class ResizeableLabel( BindedLabel ) :
    '''
    User-resizeable label.
    '''    

    hover_color = ListProperty( [0,0,0,1] )
    '''
    A widget is displayed to show the new size of the label.
    It's filled with this color.
    '''

    root_layout = ObjectProperty( None )
    '''
    The 'hover' is drawn on the root layout due to possible size mismatch.
    You'll need to provide a link to your root layout.
    '''

    on_new_size = ObjectProperty( None )
    '''
    Called by on_size method whenever the size of the label changes.
    '''

    meta = ObjectProperty( None )
    '''
    Passed as argument to on_new_size, use it as you wish...
    '''
    
    min_width = NumericProperty( 50 )
    '''
    Label minimum width.
    '''

    _o = ListProperty( [0,0] )
    _d = ListProperty( [0,0] )
    _hover_size = ListProperty( [0,0] )
    _hover_pos = ListProperty( [0,0] )
    
    
    def __init__( self, **kargs ) :
        super( ResizeableLabel, self ).__init__( **kargs )
        self._touched = False
        self._unique_group = { 'group':'__resizeable_label_%d' % (id(self)) }

    def on_touch_down( self, touch ) :
        self._touched = False
        if ( ( self.pos[0] < touch.pos[0] < self.pos[0]+self.width ) and
             ( self.pos[1] < touch.pos[1] < self.pos[1]+self.height ) ) : 
            self._touched = True
            self._o = touch.pos
            self._pivot = self._get_pivot()
            return True

    def on_touch_move( self, touch ) :
        if self._touched :
            self._d = touch.pos
            self._hover_size, self._hover_pos = self._get_hover()

            if self.root_layout :
                self._clear_canvas()

                with self.root_layout.canvas :
                    kg.Color( *self.hover_color, **self._unique_group )
                    kg.Rectangle( 
                        size=self._hover_size, \
                        pos=self._hover_pos, \
                        **self._unique_group 
                    )
            return True

    def on_touch_up( self, touch ) :
        if self._touched :
            self._clear_canvas()
            self._o = []
            if self._hover_size[0] > self.min_width :
                self._on_size( self.size, self._hover_size )
            return True

    def _on_size( self, oldsize, newsize ) :
        print( 'Size changed' )
        if self.on_new_size : self.on_new_size( oldsize, newsize, self.meta )
        self.size = copy( newsize )

    def _get_pivot( self ) :
            
        tx, ty = abs(self._o[0]-self.pos[0]), abs(self._o[1]-self.pos[1])
        ox, oy = tx/self.size[0], ty/self.size[1]

        if ox < 0.33 :
            x = 0
        elif ox < 0.66 :
            x = 3
        else :
            x = 6
        return x +1

        """
        if oy > 0.66 :
            return x + 0
        elif oy > 0.33 :
            return x + 1
        else :
            return x + 2
        """
    
    def _get_hover( self ) :

        dx = self._d[0] - self._o[0]
        dy = self._d[1] - self._o[1]

        if self._pivot == RIGHT :
            return [self.size[0]+dx, self.size[1]], self.pos
        return self.size, self.pos
   
    def _clear_canvas( self ) :
        self.root_layout.canvas.remove_group( self._unique_group['group'] )

