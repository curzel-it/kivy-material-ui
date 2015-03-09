import sys
sys.path.append( '.' )
sys.path.append( '..' )

from kivy.app import App
from kivy.atlas import Atlas
from kivy.cache import Cache
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout

from material_ui.navigation.error import ErrorForm

from pkg_resources import resource_filename
icon = resource_filename( __name__, 'images/nonetwork.png' )

class NoNetworkForm( ErrorForm ) :

    def __init__( self, **kargs ) :
        kargs['texth1' ] = kargs['texth1' ] if 'texth1'  in kargs.keys() else 'Connectivity problems'
        kargs['texth1' ] = kargs['texth1' ] if 'texth1'  in kargs.keys() else 'You might be offline... Or server is down'
        kargs['details'] = kargs['details'] if 'details' in kargs.keys() else 'Please check your internet connection.'
        kargs['strace' ] = kargs['strace' ] if 'strace'  in kargs.keys() else ''
        kargs['icon'   ] = kargs['icon'   ] if 'icon'    in kargs.keys() else icon
        super( NoNetworkForm, self ).__init__( **kargs )
        if not 'title' in kargs.keys() : self.title = 'Network problems'










