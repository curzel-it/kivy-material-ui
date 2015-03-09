import sys
sys.path.append( '..' )

from kivy.app import App
from kivy.atlas import Atlas
from kivy.cache import Cache
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout

from material_ui.navigation.form import Form

#KV Lang files
from pkg_resources import resource_filename
path = resource_filename( __name__, 'error.kv' )
icon = resource_filename( __name__, 'images/awsnap.png' )
Builder.load_file( path )

class ErrorForm( Form ) :

    texth1  = StringProperty( 'Generic error' )
    texth2  = StringProperty( "We're sorry, but this is bad :/" )
    strace  = StringProperty( '' )
    icon    = StringProperty( icon )
    details = StringProperty( """
If you see this page the software got an error and causes are unknown.
""" )  

    def __init__( self, **kargs ) :
        super( ErrorForm, self ).__init__( **kargs )
        if not 'title' in kargs.keys() : self.title = 'Generic Error'









