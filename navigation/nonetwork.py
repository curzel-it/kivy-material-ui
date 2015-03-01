import sys
sys.path.append( '..' )

from kivy.app import App
from kivy.atlas import Atlas
from kivy.cache import Cache
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout

from error import ErrorForm

class NoNetworkForm( ErrorForm ) :

    def __init__( self, **kargs ) :
        kargs['texth1' ] = kargs['texth1' ] if 'texth1'  in kargs.keys() else 'Connectivity problems'
        kargs['texth1' ] = kargs['texth1' ] if 'texth1'  in kargs.keys() else 'You might be offline... Or server is down'
        kargs['details'] = kargs['details'] if 'details' in kargs.keys() else 'Please check your internet connection.'
        kargs['strace' ] = kargs['strace' ] if 'strace'  in kargs.keys() else ''
        kargs['icon'   ] = kargs['icon'   ] if 'icon'    in kargs.keys() else 'nonetwork.png'
        super( NoNetworkForm, self ).__init__( **kargs )
        if not 'title' in kargs.keys() : self.title = 'Network problems'










