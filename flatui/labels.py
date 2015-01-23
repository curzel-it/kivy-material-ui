import sys
sys.path.append( '..' )

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

    background_color = ListProperty( [0,0,0,0] )

    def __init__( self, **kargs ) : 
        t = str( kargs['text'] if 'text' in kargs.keys() else '' )
        kargs['text'] = str( t )
        super( BindedLabel, self ).__init__( **kargs )    
        self.bind( size=self.setter('text_size') )


class ResizeableLabel( BindedLabel ) :
    '''
    Label you can user-resizeable.
    '''    

    #hover_color = ListProperty( [.4,.4,.6,.5] )
    hover_color = ListProperty( [0,0,0,1] )
    root_layout = ObjectProperty( None )

    _o = ListProperty( [0,0] )
    _d = ListProperty( [0,0] )
    _hover_size = ListProperty( [0,0] )
    _hover_pos = ListProperty( [0,0] )
    
    
    def __init__( self, **kargs ) :
        super( ResizeableLabel, self ).__init__( **kargs )
        self._unique_group = { 'group':'__resizeable_label_%d' % (id(self)) }

    def on_touch_down( self, touch ) :
        self._o = touch.pos
        self._pivot = self._get_pivot()

    def on_touch_move( self, touch ) :
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

    def on_touch_up( self, touch ) :
        self._clear_canvas()
        self.size = self._hover_size

    def _get_pivot( self ) :
            
        tx, ty = self._o[0]-self.pos[0], self._o[1]-self.pos[1]
        ox, oy = tx/self.size[0], ty/self.size[1]

        if ox < 0.33 :
            x = 0
        elif ox < 0.66 :
            x = 3
        else :
            x = 6

        if oy < 0.33 :
            return x + 0
        elif oy < 0.66 :
            return x + 1
        else :
            return x + 2
            
    def _get_hover( self ) :

        size, pos = self.size, self.pos
        dx = abs( self._d[0] - self._o[0] )
        dy = abs( self._d[1] - self._o[1] )

        if self._pivot == TOP_RIGHT :
            size[0] = self.size[0] + dx
            
        elif self._pivot == RIGHT :
            size[0] = self.size[0] + dx

        elif self._pivot == BOTTOM_RIGHT :
            pos[1] = self.pos[1] - dy
            size[0] = self.size[0] + dx
            size[1] = self.size[1] - dy


        elif self._pivot == TOP :
            pos[1] = self.pos[1] + dy
            size[0] = self.size[0] + dx
            size[1] = self.size[1] + dy
            
        elif self._pivot == CENTER :
            ...

        elif self._pivot == BOTTOM :
            pos[1] = self.pos[1] - dy
            size[0] = self.size[0] + dx
            size[1] = self.size[1] + dy


        elif self._pivot == TOP_LEFT :
            pos[0] = self.pos[0] - dx
            pos[1] = self.pos[1] + dy
            size[0] = self.size[0] + dx
            size[1] = self.size[1] + dy
            
        elif self._pivot == LEFT :
            pos[0] = self.pos[0] - dx
            size[0] = self.size[0] + dx

        elif self._pivot == BOTTOM_LEFT :
            pos[0] = self.pos[0] - dx
            pos[1] = self.pos[1] - dy
            size[0] = self.size[0] + dx
            size[1] = self.size[1] + dy


        return size, pos














   
    def _clear_canvas( self ) :
        self.root_layout.canvas.remove_group( self._unique_group['group'] )

