import sys
sys.path.append( '..' )

from kivy.app import App
from kivy.atlas import Atlas
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from navigation.form import Form
from navigation.error import ErrorForm
from navigation.nonetwork import NoNetworkForm

from flatui.scroll import RefreshableScrollView

#KV Lang files
from pkg_resources import resource_filename
path = resource_filename( __name__, 'dashboard.kv' )
Builder.load_file( path )


class DashBoardForm( Form ) :

    def __init__( self, **kargs ) :
        kargs['title'] = 'Refreshable ScrollView'
        super( DashBoardForm, self ).__init__( **kargs )

        """
        ScrollView with a refresh controll...
        """
        self.myscroll = RefreshableScrollView( 
            on_start_reload=self.on_start_reload, 
            root_layout=self.shared_navigation_controller.floating_panel
        )
        self.add_widget( self.myscroll )
            
        """
        Loading fake elements...
        """
        temp = GridLayout( size_hint=(1,None), cols=1 )
        for n in ['Pull down to reload','A fake error will be raised']+list(range(0,20)) :
            l = Label( text='Element no '+str(n), height=dp(50), size_hint=(1,None), color=[0,0,0,.8] )
            temp.add_widget( l )
            temp.height += dp(50)

        self.myscroll.add_widget( temp )

    """
    Called whenever the user asks for a refresh of the scrollview.
    """
    def on_start_reload( self, *args ) :
        Clock.schedule_once( self.raise_fake_error, 5 )

    """
    Will show an error form.
    """
    def raise_fake_error( self, *args ) :
        self.myscroll.reload_done()
        try :        
           raise IOError( "Fake exeption to show pop\\push animations." )
        except IOError as e :
            self.shared_navigation_controller.push( 
                NoNetworkForm(
                    shared_navigation_controller=self.shared_navigation_controller, 
                    strace=str(e) 
                ), 
                title='Network Error'
            )
        except Exception as e :
            self.shared_navigation_controller.push( 
                ErrorForm( 
                    shared_navigation_controller=self.shared_navigation_controller,
                    strace=str(e) 
                ), 
                title='Generic Error' 
            )
        return True






