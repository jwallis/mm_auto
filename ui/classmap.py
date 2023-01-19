class Classmap(object):
    """
    The classes in self.classmap are classes the framework defines.  They are subclasses of UIObject
    and provide some added functionality
    """
    def __init__(self, platform):
        self.platform = platform

        if (self.platform == 'ios'):
            self.mapping = {
                'actionsheet': 'UIAActionSheet',
                'activityindicator': 'UIAActivityIndicator',
                'alert': 'UIAAlert',
                'button': 'UIAButton',
                'collectioncell': 'UIACollectionCell',
                'collection': 'UIACollectionView',
                'editingmenu': 'UIAEditingMenu',
                'image': 'UIAImage',
                'key': 'UIAKey',
                'keyboard': 'UIAKeyboard',
                'link': 'UIALink',
                'mapview': 'UIAMapView',
                'pageindicator': 'UIAPageIndicator',
                'picker': 'UIAPicker',
                'pickerwheel': 'UIAPickerWheel',
                'popover': 'UIAPopover',
                'progress': 'UIAProgressIndicator',
                'scrollview': 'UIAScrollView',
                'searchbar': 'UIASearchBar',
                'secure': 'UIASecureTextField',
                'segmented': 'UIASegmentedControl',
                'slider': 'UIASlider',
                'statictext': 'UIAStaticText',      # do not use "text" only "statictext"
                'statusbar': 'UIAStatusBar',
                'switch': 'UIASwitch',
                'tabbar': 'UIATabBar',
                'table': 'UIATableView',
                'tablecell': 'UIATableCell',
                'tablegroup': 'UIATableGroup',
                #'text': 'UIAStaticText',           # NO!  Do not use "text" always use "statictext"
                'textfield': 'UIATextField',
                'textview': 'UIATextView',
                'toolbar': 'UIAToolbar',
                'webview': 'UIAWebView',
                'window': 'UIAWindow',
                'navigationvar': 'UIANavigationBar'
            }
        elif (self.platform == 'android'):
            self.mapping = {
                "abslist": "android.widget.AbsListView",
                "absseek": "android.widget.AbsSeekBar",
                "absspinner": "android.widget.AbsSpinner",
                "absolute": "android.widget.AbsoluteLayout",
                "adapterview": "android.widget.AdapterView",
                "adapter": "android.widget.AdapterView",
                "adapterviewanimator": "android.widget.AdapterViewAnimator",
                "adapterviewflipper": "android.widget.AdapterViewFlipper",
                "analogclock": "android.widget.AnalogClock",
                "appwidgethost": "android.widget.AppWidgetHostView",
                "autocomplete": "android.widget.AutoCompleteTextView",
                "button": "android.widget.Button",
                "breadcrumbs": "android.widget.FragmentBreadCrumbs",
                    "crumbs": "android.widget.FragmentBreadCrumbs",
                "calendar": "android.widget.CalendarView",
                "checkbox": "android.widget.CheckBox",
                "checked": "android.widget.CheckedTextView",
                "checkedtextview": "android.widget.CheckedTextView",
                "chronometer": "android.widget.Chronometer",
                "compound": "android.widget.CompoundButton",
                "datepicker": "android.widget.DatePicker",
                "dialerfilter": "android.widget.DialerFilter",
                "digitalclock": "android.widget.DigitalClock",
                "drawer": "android.widget.SlidingDrawer",
                    "slidingdrawer": "android.widget.SlidingDrawer",
                "expandable": "android.widget.ExpandableListView",
                "extract": "android.widget.ExtractEditText",
                "fragmenttabhost": "android.widget.FragmentTabHost",
                "frame": "android.widget.FrameLayout",
                "gallery": "android.widget.Gallery",
                "gesture": "android.widget.GestureOverlayView",
                "glsurface": "android.widget.GLSurfaceView",
                "grid": "android.widget.GridView",
                "gridlayout": "android.widget.GridLayout",
                "horizontal": "android.widget.HorizontalScrollView",
                "image": "android.widget.ImageView",
                "imagebutton": "android.widget.ImageButton",
                "imageswitcher": "android.widget.ImageSwitcher",
                "keyboard": "android.widget.KeyboardView",
                "linear": "android.widget.LinearLayout",
                "list": "android.widget.ListView",
                "media": "android.widget.MediaController",
                "mediaroutebutton": "android.widget.MediaRouteButton",
                "multiautocomplete": "android.widget.MultiAutoCompleteTextView",
                "numberpicker": "android.widget.NumberPicker",
                "pagetabstrip": "android.widget.PageTabStrip",
                "pagetitlestrip": "android.widget.PageTitleStrip",
                "progress": "android.widget.ProgressBar",       # based on ios naming
                "quickcontactbadge": "android.widget.QuickContactBadge",
                "radio": "android.widget.RadioButton",
                "radiogroup": "android.widget.RadioGroup",
                "rating": "android.widget.RatingBar",
                "relative": "android.widget.RelativeLayout",
                "rssurface": "android.widget.RSSurfaceView",
                "rstexture": "android.widget.RSTextureView",
                "scroll": "android.widget.ScrollView",
                "search": "android.widget.SearchView",
                "seek": "android.widget.SeekBar",
                    "seekbar": "android.widget.SeekBar",
                "space": "android.widget.Space",
                "spinner": "android.widget.Spinner",
                "stack": "android.widget.StackView",
                "surface": "android.widget.SurfaceView",
                "switch": "android.widget.Switch",
                "tabhost": "android.widget.TabHost",
                "tabwidget": "android.widget.TabWidget",
                "table": "android.widget.TableLayout",
                "tablerow": "android.widget.TableRow",
                "statictext": "android.widget.TextView",        # based on ios naming
                #'text': 'android.widget.TextView',             # NO!  Do not use "text" always use "statictext"
                "textclock": "android.widget.TextClock",
                "textswitcher": "android.widget.TextSwitcher",
                "texture": "android.widget.TextureView",
                "textfield": "android.widget.EditText",         # based on ios naming
                "timepicker": "android.widget.TimePicker",
                "toggle": "android.widget.ToggleButton",
                "twolinelistitem": "android.widget.TwoLineListItem",
                "video": "android.widget.VideoView",
                "viewanimator": "android.widget.ViewAnimator",
                "view": "android.view.View",
                "viewflipper": "android.widget.ViewFlipper",
                "viewgroup": "android.widget.ViewGroup",
                "viewpager": "android.widget.ViewPager",
                "viewstub": "android.widget.ViewStub",
                "viewswitcher": "android.widget.ViewSwitcher",
                "web": "android.webkit.widget.WebView",
                "window": "android.widget.FrameLayout",
                "zoom": "android.widget.ZoomButton",
                "zoomcontrols": "android.widget.ZoomControls"
            }
        else:
            raise RuntimeError('invalid platform: ' + self.platform)

        # helps identify plurals
        self.appium_aliases = ['image', 'table', 'scrollview', 'secure', 'relative', 'space', 'toggle']


    def map(self, shortcut):
        try:
            return self.mapping[shortcut.lower()]
        except KeyError:
            raise RuntimeError(shortcut + " is not a valid element type (or a plural word that was unhandled).  Maybe Classmap needs to be updated?")
