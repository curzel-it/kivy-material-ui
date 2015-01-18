# kivy-material-ui
Bunch of classes, layouts and images I use in my projects.  
I've documented almost everything, so this is good.

### Test.py screenshot
![alt tag]( https://github.com/Cuuuurzel/kivy-material-ui/blob/master/images/screenshot.png )

### Custom kivy theme
You will need to replace the 'defaulttheme-0.png' with mine.  
( Path is ~kivy/data/images )  
I've also developed some fork of kivy.uix.popup, adding title font, color and align customizations.  

### Widgets
Most widget are direct subclasses of standard ones.

####FlatTextInput
Flat version of the standard TextInput.

####FlatButton
Flat button, supports fill color and shadow.

####FloatingAction
Round and flat button, supports fill color and shadow.

####PopupComboBox
When a click on this button occur, a popup will be shown to pick a value.
Arguments named popup_* will be passed down to the popup for customizations.

