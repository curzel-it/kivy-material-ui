# kivy-material-ui
Bunch of classes, layouts and images I use in my projects.  
For graphical objects I've tried to follow Google's Materia UI guidelines.  
Also, I've tried to keep the project documented and clean...  

### Custom kivy theme
You will need to replace the 'defaulttheme-0.png' with mine.  
( Path is ~kivy/data/images )  
  
### Navigation system 
I've implemented a basic ios-like navigation system.  
You will need to put a NavigationController widget as top widget in your app, this will provide :  
* Navigation bar support, easier and more flexible than the standard ActionBar...  
* You can pop\push other views as the main content.  
* A FloatingLayout is provided to show special widgets and animations.  
* On-pop and on-push callbacks.  
  
Also, I've implemented a simple "Form" class, to handle views contents.  

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

* **PopupComboBox**  
When a click on this button occur, a popup will be shown to pick a value.  
Arguments named popup_* will be passed down to the popup for customizations.

* **AlertPopup**  
FlatPopup subclass which allows you to show an alert in a single line of code.  
Supports two action buttons.  

* **OkButtonPopup**  
FlatPopup subclass with a single 'OK' button.

#### Scroll views
You can use an android-like control to refresh scroll view contents.  
Use RefreshableScrollView for that.  
Just like you would do with overscroll effects, you can assign different reloading animations.  

The default animation for RefreshableScrollView is LollipopSpinner, based on gapps spinners.
