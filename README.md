# kivy-material-ui
Bunch of classes, layouts and images I use in my projects.  

### Custom kivy theme
You will need to replace the 'defaulttheme-0.png' with mine.  
( Path is ~kivy/data/images )  
  
### Widgets
Most widget are direct subclasses of standard ones.

#### FlatTextInput
Flat version of the standard TextInput.  
Supports cursor color and underlined text while editing.

#### Material UI buttons
* Raised button, transparent background and support to text colors.
* Flat button, supports background and text colors, icons, and shadow.
* Floating action, round button with shadow, supports shadow and colors

#### Popups
I've simply copy-pasted from kivy.uix.popup to create a class named FlatPopup, there are just a fiew more properties, such as *text_align* and *text_font*.

##### PopupComboBox
When a click on this button occur, a popup will be shown to pick a value.  
Arguments named popup_* will be passed down to the popup for customizations.

##### AlertPopup
FlatPopup subclass which allows you to show an alert in a single line of code.  
Supports two action buttons.  

##### OkButtonPopup
FlatPopup subclass with a single 'OK' button.

#### Scroll views
You can use an android-like control to refresh scroll view contents.
Use RefreshableScrollView for that.
Just like you would do with overscroll effects, you can assign different reloading animations.

##### Lollipop Spinner
That's the default animation for RefreshableScrollView, based on gapps spinners.
