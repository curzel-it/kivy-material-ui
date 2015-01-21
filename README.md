# kivy-material-ui
Bunch of classes, layouts and images I use in my projects.  
I've documented almost everything, so this is good.

### Screenshot from test.py
Main view
![alt tag]( https://github.com/Cuuuurzel/kivy-material-ui/blob/master/images/screen-1.png )

FlatPopup example
![alt tag]( https://github.com/Cuuuurzel/kivy-material-ui/blob/master/images/screen-2.png )

OkButtonPopup example
![alt tag]( https://github.com/Cuuuurzel/kivy-material-ui/blob/master/images/screen-3.png )

AlertPopup with a single button
![alt tag]( https://github.com/Cuuuurzel/kivy-material-ui/blob/master/images/screen-4.png )

AlertPopup with two buttons
![alt tag]( https://github.com/Cuuuurzel/kivy-material-ui/blob/master/images/screen-5.png )

### Custom kivy theme
You will need to replace the 'defaulttheme-0.png' with mine.  
( Path is ~kivy/data/images )  
I've also developed some fork of kivy.uix.popup, adding title font, color and align customizations.  
  
Needs a little addition to defaulttheme.atlas :  
{"defaulttheme-0.png": {**"transparent": [0,0,0,0], **"progress...

### Widgets
Most widget are direct subclasses of standard ones.

#### FlatTextInput
Flat version of the standard TextInput.  
Supports cursor color and underlined text while editing.

#### FlatButton
Flat button, supports fill color, icons, and shadow.

#### FloatingAction
Round and flat button, supports fill color, icons, and shadow.

#### PopupComboBox
When a click on this button occur, a popup will be shown to pick a value.  
Arguments named popup_* will be passed down to the popup for customizations.

#### FlatPopup
Code is simply copy-pasted from kivy.uix.popup.  
There are just a fiew more properties, such as *text_align* and *text_font*.

#### AlertPopup
FlatPopup subclass which allows you to show an alert in a single line of code.  
Supports two action buttons.  

#### OkButtonPopup
FlatPopup subclass with a single 'OK' button.
