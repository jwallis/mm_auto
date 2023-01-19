from _external import *
from strings_generic import *
from ..strings_specific import *

class System(object):
##################################################################
# system settings/copy/paste/etc
# most of this is UIAutomator only #######################

    def goto_system_settings(self):
        """
        Goes to main device system settings page.
        """

        # (No, this should not be in navigation.py because this method is not app-specific)
        if (self.android):
            self.device.home()
            self.sleep(1)

            #on some devices, when you're on the home screen and tap "menu" Settings is not an option.
            #on these devices, we must put the Settings app on the home screen
            if (self.tap_safe(self.strings.System_settings, timeout=3)):
                return

            self.device.menu()

            self.tap(self.strings.System_settings)
        elif (self.ios):
            if (self.simulator):
                self.device.home()
                self.tap(self.strings.Settings)

            else:
                self.blocked("goto_system_settings() not implemented for physical ios device. Need to figure out if we can tap the Home button...")
        else:
            raise RuntimeError('bad platform')

        self.sleep(.5)

    def show_control_center(self):
        if (self.android):
            self.blocked("show_control_center() not implemented for android.  Maybe you want 'goto_system_settings()'?")
        elif (self.ios):
            self.device.bezel_swipe_bottom()
            self.sleep(1)
        else:
            raise RuntimeError('bad platform')

    def hide_control_center(self):
        if (self.android):
            self.blocked("hide_control_center() not implemented for android.  Maybe you want 'goto_system_settings()'?")
        elif (self.ios):
            self.device.tap(.1,.1)
        else:
            raise RuntimeError('bad platform')

    def open_notifications(self):
        if (self.ios):
            return
        elif (self.android):
            self.driver.open_notifications()
        else:
            raise RuntimeError('bad platform')

    def clear_all_notifications(self):
        if (self.ios):
            return
        elif (self.android):
            self.driver.open_notifications()
            self.tap(self.strings.Clear_all_notifications_)
        else:
            raise RuntimeError('bad platform')


    #def set_bluetooth_mode
    #it may be impossible (to tell if it's on or off for iphone)
    #iphone 4:
    #tap(.5, .23)
    #iphone 5:
    #tap(.5, .35)

    def set_location_services(self, on_off, app=True):
        on_off = on_off.lower()

        if (on_off not in ['on', 'off']):
            raise RuntimeError('in set_location_services().  arg must be either "on" or "off"')

        if (self.android):
            self.goto_system_settings()

            if(self.exists_and_visible_on_page(self.strings.Location)):
                self.tap_safe(self.strings.Location)
                self.sleep(.5)

            if self.switch().checked():
                current_mode = 'on'
            else:
                current_mode = 'off'

            if on_off != current_mode:
                self.switch().tap()
                self.location_services_has_been_set = True
                if (self.exists(self.strings.Cancel)):
                    self.tap(self.strings.OK)

            self.sleep(.5)

            if (app):
                self.switch_apps(self.strings.app_name)
        elif (self.ios):
            self.blocked('set_location_services() not yet implemented for iOS')
        else:
            raise RuntimeError('bad platform')

    def set_airplane_mode(self, on_off, app=True):
        """
        This currently works fine, and is nice because it really simulates a user, There may be an easier way to do this.
            Check out http://appium.io/slate/en/v1.2.1/?python#adjusting-network-connection
            or search for: appium adjusting network connection

        This only works for (most) Android phones and hardware iphones on ios7. sets airplane mode to true or false
        :param on_off: boolean - whether to turn mode on/off
        :param app: (android only) should we switch back to app after setting airplane mode? (see what the app's title is in app switcher to determine the string to pass)
        """
        on_off = on_off.lower()

        if (on_off not in ['on', 'off']):
            raise RuntimeError('in set_airplane_mode().  arg must be either "on" or "off"')

        if (self.android):
            self.goto_system_settings()

            # sometimes the airplane mode is directly under settings, sometimes you have to tap "More nentworks" or "More..."
            if (self.tap_safe(self.strings.More_networks)):
                self.sleep(.5)

            if (self.exists(element_type='checkbox')):
                e = self.checkbox()
            else:
                #for nexus 6 on Lollipop
                e = self.switch()

            if (e.checked()):
                current_mode = 'on'
            else:
                current_mode = 'off'

            if (on_off != current_mode):
                e.tap()
                self.airplane_mode_has_been_set=True
                if (self.exists(self.strings.Cancel)):
                    self.tap(self.strings.OK)

            self.sleep(.5)

            if (app):
                self.switch_apps(self.strings.app_name)

        elif (self.ios):
            if (self.simulator or self.iphone_or_ipad() != 'iphone' or self.device_os_version not in ['7.0','7.1']):
                self.blocked('set_airplane_mode() only for hardware iphone 7.0 & 7.1')

            current_mode = 'on' if self.exists('Airplane mode on') else 'off'

            if (on_off != current_mode):
                self.show_control_center()
                if (self.hardware):
                    if (self.device_model.find('iphone 4')>-1):
                        self.device.tap(.12,.23)
                    elif (self.device_model.find('iphone 5')>-1):
                        self.device.tap(.12,.35)
                    else:
                        raise RuntimeError('device_model needs to include either "4" or "5" as in "iphone4s"')
                else:
                    self.device.tap(.12,.23)

                self.airplane_mode_has_been_set=True
                self.hide_control_center()
        else:
            raise RuntimeError('bad platform')

        #let wi-fi reconnect iff airplane was on and we turned it off
        if (current_mode == 'on' and on_off == 'off'):
            self.sleep(7)

    def set_wifi_mode(self, on_off, app=True, sleep=True):
        """
        This currently works fine, and is nice because it really simulates a user, There may be an easier way to do this.
            Check out http://appium.io/slate/en/v1.2.1/?python#adjusting-network-connection
            or search for: appium adjusting network connection

        This only works for (most) Android phones and hardware iphones on ios7. sets wifi mode to true or false
        :param on_off: boolean - whether to turn mode on/off
        :param app: (android only) should we switch back to app after setting wifi mode? (see what the app's title is in app switcher to determine the string to pass)
        """
        on_off = on_off.lower()

        if (on_off not in ['on', 'off']):
            raise RuntimeError('in set_wifi_mode().  arg must be either "on" or "off"')

        if (self.android):
            self.goto_system_settings()

            # sometimes the airplane mode is directly under settings, sometimes you have to tap "More..."
            # if (not self.exists(self.strings.Airplane_mode)):
            #     self.find(self.strings.MORE___).tap()

            #if you are not at the top, scroll to the top first
            e = self.find_safe(self.strings.Wi_Fi)
            if (e):
                e.tap()
            else:
                self.device.swipe(.5, .2, .5, .9, .2)
                self.tap(self.strings.Wi_Fi)

            current_mode = self.switch().text.lower()
            if (on_off != current_mode):
                self.switch().tap()
                # if (self.exists(self.strings.Cancel)):
                #     self.tap(self.strings.OK)
                self.wifi_mode_has_been_set = True

            self.sleep(.5)

            if (app):
                self.switch_apps(self.strings.app_name)

        elif (self.ios):
            if (self.simulator):
                self.log.debug('setting simulator\'s wifi on/off by setting this mac\'s wifi on/off')
                import subprocess
                retval = subprocess.check_output(['networksetup', '-setairportpower', 'airport', on_off])
                self.log.debug("return value from subprocess call:\n" + retval)

                self.wifi_mode_has_been_set = True
                return

            elif (self.iphone_or_ipad() != 'iphone' or self.device_os_version not in ['7.0', '7.1']):
                self.blocked('set_wifi_mode() only for sim, or HW iphone 7.0 & 7.1')

            else:
                current_mode = 'on' if self.exists(' Wi-Fi bars', partial=True) else 'off'

                if (on_off != current_mode):
                    self.show_control_center()
                    if (self.device_model.find('iphone 4')>-1):
                        self.device.tap(.31, .23)
                    elif (self.device_model.find('iphone 5')>-1):
                        self.device.tap(.31, .35)
                    else:
                        raise RuntimeError('device_model needs to include either "4" or "5" as in "iphone 4s"')
                    self.wifi_mode_has_been_set = True
                    self.hide_control_center()

        else:
            raise RuntimeError('bad platform')

        #let wi-fi reconnect iff it was off and we turned it on
        if (sleep and current_mode == 'off' and on_off == 'on'):
            self.sleep(7)
        else:
            self.sleep(2)

    def set_wifi_network(self, name, password):
        pass
        #if ios & simulator sudo networksetup -setairportnetwork en1 "Mutual Mobile" mobilemutual

    def set_language(self, lang=True, app=True):
        """
        For internationalization.
        optional param (defaults to self.data.language) should be something like 'en_US' or 'de_DE'
        """
        if (lang==True):
            #self.data.language is the language that the app was BOOTED in, so it never changes.  It looks something like "en_US"
            lang = self.data.language

        if (self.device_model in ['moto x', 'moto g']):
            self.set_language_using_3rd_party_app(lang)
        else:
            try:
                self.goto_system_settings()
            except Exception, e:
                # if our err msg looks like "no element in our list could be found:['Settings', 'System settings']"
                # then the phone may be in a language we're not expecting (if something crashed hard last run)
                # let's try to figure out which lang we're in...
                if (str(e).find(self.strings.System_settings[0]) > -1):
                    self.tap_system_settings_any_language()
                else:
                    raise e

            self.tap_safe(self.strings.My_device)               #some Samsung phones have this step
            self.tap_on_page(self.strings.Language_and_input)   #settings menu
            self.tap_on_page(self.strings.Language)             #settings menu

            # setup_strings() sets current language to the NEW language we're just about to set.
            self.setup_strings(lang)

            found = self.tap_safe_on_page(self.current_language, 10)    #tap the string in its language

            if (not found):
                self.set_language_using_3rd_party_app(lang)

        self.sleep(1)

        if (app):
            self.switch_apps(self.strings.app_name)

    def set_language_using_3rd_party_app(self, lang):
        """
        used on android.
        prerequisite: install "Locale & Language+" app, which has a yellow globe icon
        can be downloaded from http://automini01.local
        """
        self.device.home()
        self.sleep(1)
        self.tap('Locale & Language+')
        self.sleep(1)

        # setup_strings() sets current language to the NEW language we're just about to set.
        self.setup_strings(lang)
        for i in range(4):
            self.device.swipe(.5, .2, .5, .9, .2)
            self.sleep(.5)
        self.tap_on_page(self.current_language, 15)          #the string in its language




    def tap_system_settings_any_language(self):
        """
        If our device gets into a language we're not expecting, try to get it back to English or whatever language we want it to be now.
        This could happen if something crashed hard last run... we may still be in Polish, but our test is just starting so we're expecting English
        """

        # typical case: the menu button has already been tapped, menu should show 'System settings' in SOME language
        for temp_lang in self.strings.supported_languages:
            self.setup_strings(temp_lang)
            if (self.tap_safe(self.strings.System_settings)):
                return

        # non-typical case: the menu button does some weird thing, so we've hand to manually put the System settings app on the home screen.
        # this is handled in goto_system_settings() also.
        self.device.home()

        # same loop again, just looking on desktop instead of menu...
        for temp_lang in self.strings.supported_languages:
            self.setup_strings(temp_lang)
            if (self.tap_safe(self.strings.System_settings)):
                return

        raise RuntimeError("Tried tapping 'System settings' in every language we know of but couldn't find it...")


    def clear_app_cache(self, app_name=None):
        self.clear_app_generic(app_name, self.strings.Clear_cache)

    def clear_app_data(self, app_name=None):
        self.clear_app_generic(app_name, self.strings.Clear_data)

    def clear_app_generic(self, app_name, clear_what):

        self.blocked_on_ios('clear_app_generic() not implemented for iOS')

        if (app_name == None):
            app_name = self.strings.app_name

        self.goto_system_settings()
        self.tap_on_page(self.strings.Apps, 10)
        self.tap_on_page(app_name, 10)
        self.tap_on_page(clear_what)
        self.tap_on_page(self.strings.OK)
        self.sleep(3)

        self.switch_apps(app_name)


    def launch_app(self, app_name=None):
        """
        Searches for an app by name, launches it.
        :param app_name: To be sure of what the app is called in this context, you should probably try looking at the app switcher yourself on a device.
        """
        self.blocked_on_ios('launch_app() not implemented for iOS')

        if (app_name == None):
            app_name = self.strings.app_name

        self.device.home()
        self.tap(self.strings.Apps) #from homepage,tap the apps button
        self.sleep(.5)
        self.find_on_page_horizontal(app_name).tap()


        # using device search.  doesn't work that well, too many variables
        # self.device.home()
        # self.device.search()
        #
        # e=self.find(self.strings.Search)
        # e.send_keys(app_name + '\n')
        #
        # #now tap the right one.  let's cross our fingers...
        # #todo: make this more robust
        # self.find(app_name).tap()

    def switch_apps(self, app_name=None):
        """
        Takes an app's full name, switches to it.
        :param app_name: To be sure of what the app is called in this context, you should probably try looking at the app switcher yourself on a device.
        """
        if (app_name==None):
            app_name=self.strings.app_name

        if (self.ios):
            if (self.hardware):
                self.blocked('switch_apps() not implemented for iOS hardware')

            self.device.home()
            self.device.app_switch()
            self.sleep(1.5)
            self.tap_by_location(app_name)
        else:
            if (self.hardware):
                self.device.app_switch()
                #TODO: Problematic line below. For some reason, sometimes the app quits?
                #on mac mini, sometimes we tap too fast.  need a little pause.  this may have been the cause of the app crash noted in the TODO above
                self.sleep(.8)

                #This is weird and surprising:
                # on nexus 6 there's an imageView and a textView, both named Lyric.  You can only use the textview.
                # on moto x there's a textView and a frameLayout, both named Lyric.  You can only use the frameLayout.
                if (self.device_model in ['nexus 6']):
                    self.tap(app_name, element_type='statictext')
                else:
                    self.tap(app_name)
            else:
                pass
                #sergio gennymotion

        self.sleep(1)

    def set_geo_location(self, loc, switch_back=True):
        """
        loc should either be:
        1-an AttrDict that looks like:
        geo_loc01a.name            = 'loc01a'     # android
        geo_loc01a.lat             =  31.0934         # ios
        geo_loc01a.long            = -97.2039         # ios
        2-the string "off" or "stop" (Android only)

        prerequisites:
        android: install "Fake Location" (from play store or http://automini01.local)
        """
        if (self.ios):
            self.log.debug("setting geo location to %s, %s" % (loc.lat, loc.long))
            self.driver.execute('setLocation',{"location": {"latitude": loc.lat, "longitude": loc.long}})
        elif (self.android):
            if (type(loc) == str):
                self.log.debug("setting geo location to %s" % loc)
            else:
                self.log.debug("setting geo location to %s" % loc.name)

            self.device.home()

            try:
                self.tap('Fake Location')
            except NoSuchElementException:
                raise RuntimeError("In set_geo_location(). To use this method, you must install Fake Location and put its icon on your Android Home Screen")

            if (type(loc) == str and loc.lower() in ['off', 'stop']):
                self.tap('Stop the service')
            else:
                self.sleep(2.5)
                #later version has different button names
                self.tap(['Stop the service', 'Stop'])
                self.sleep(8)
                self.tap("Favorites")
                self.tap(loc.name)
                self.sleep(1.5)
                self.tap("Start")
                self.sleep(10)
            if(switch_back):
                self.switch_apps()
        else:
            raise RuntimeError("bad platform")

        # Never sleep at the end of this method.  May raise notifications we need to capture.


    def background_and_foreground(self):
        if self.ios:
            self.device.background()
        else:
            self.device.home()
            # do we need an "if device == 'moto x'" statement here...?
            self.launch_app()

    def restart_app(self, app_name=None):
        if(app_name == None):
            app_name = self.strings.app_name
        self.blocked_on_ios("restart_app() not implemented for iOS")
        self.log.debug("Restarting app...")
        self.force_quit(app_name)
        self.device.home()
        self.sleep(.5)
        self.launch_app(app_name)

    def force_quit(self, app_name=None):
        """
        Takes an app's full name, force quits it.
        :param app_name: To be sure of what the app is called in this context, you should probably try looking at the app switcher yourself on a device.
        """
        self.blocked_on_ios('force_quit() not implemented for iOS')

        if (app_name==None):
            app_name=self.strings.app_name

        self.device.app_switch()

        e= self.find(app_name)
        if (self.device.orientation == 'LANDSCAPE'):
            # switched from swipe_down(duration=.2) to flick_down because ui/device->swipe() wasn't implemented for android
            e.flick_down()
        else:
            e.flick_left()
        self.sleep(1)


        assert (not self.is_app_running(app_name)), 'in Flow.force_quit().  Tried to kill app but failed.'

    def is_app_running(self, app_name=None):
        """
        Returns boolean
        :param app_name: the app name.  Defaults to strings.app_name
        """
        self.blocked_on_ios('is_app_running() not implemented for iOS')

        if (app_name == None):
            app_name = self.strings.app_name

        self.device.home()
        # self.wait_for_page_load() does not exist, using sleeps for now...
        self.sleep(.3)

        self.device.app_switch()
        self.sleep(.3)

        running = self.exists(app_name)
        self.device.home()
        self.sleep(.3)
        return running

    def tap_keys_on_keyboard(self, txt):
        """
        With special programming (or in webviews with UIAutomator), send_keys() doesn't work.  Thanks.
        Sometimes you have to just tap the keys yourself.  This will currently work for a limited set of keyboard keys.
        :param txt: The string to tap.
        """
        if self.ios:
            dct = {' ':self.strings.space_key}
            for chr in txt:
                if chr in dct:
                    self.key(dct[chr]).tap()
                elif (re.search(r'[0-9]', chr)):
                    try:
                        self.key(chr).tap()
                    except NoSuchElementException:
                        self.key('more, numbers').tap()
                        self.key(chr).tap()
                else:
                    try:
                        self.key(chr).tap()
                    except NoSuchElementException:
                        if (self.exists("more, letters")):
                            self.key('more, letters').tap()

                        try:
                            self.key(chr).tap()
                        except NoSuchElementException:
                            self.button('shift').tap()
                            self.key(chr).tap()
        elif self.android:
            # http://developer.android.com/reference/android/view/KeyEvent.html
            dct = {'-':69, '=':70, '[':71, ']':72, '\\':73, ';':74, '\'':75, '/': 76, ' ':62, ',':55, '.':56, '\t':61, '\r':66, '\n':66}
            dct2 = {')':7, '!':8, '@':9, '#':10, '$':11, '%':12, '^':13, '&':14, '*':15, '(':16, '_':69, '+':70, '{':71, '}':72, '|':73, ':':74, '"':75, '?':76, '<':55, '>':56}

            for chr in txt:
                metastate=0

                if (re.search(r'[0-9]', chr)):
                    i = ord(chr) - 41
                elif (re.search(r'[a-z]', chr)):
                    i = ord(chr) - 68
                elif (re.search(r'[A-Z]', chr)):
                    i = ord(chr) - 36
                    metastate=1
                elif (chr in dct):
                    i = dct[chr]
                elif (chr in dct2):
                    i = dct2[chr]
                    metastate=1
                else:
                    raise RuntimeError("got a char I don't think we can tap: %s" % chr)

                self.driver.press_keycode(i, metastate)

        else:
            raise RuntimeError('bad platform')

    def tap_keys_by_name(self, keyname):
        """
        Clearly, this is a last resort.  taps keys based on x,y coords.
        This will currently work for a limited set of keyboard keys.
        :param keyname: The key to tap.
        """
        if (self.ios):
            raise RuntimeError('you should not have to use this method for iOS')
        elif (self.android):
            # this is the bottom row, farthest right key in the android keyboard.
            # this needs to be refactored.
            if (keyname.lower() == 'next' or keyname.lower() == 'done' or keyname.lower() == 'go'):
                if (self.device_model in ['moto x','moto g', 'galaxy s4', 'galaxy s3','htc one' ,'nexus 5','nexus 6']):
                    self.device.tap(.95,.95)
                else:
                    raise RuntimeError('your device needs x,y coords put in here...')

        else:
            raise RuntimeError('bad platform')

    def switch_to_emoji_keyboard(self):
        """
        while keyboard is open, tap to switch to the emoji keyboard
        """
        if (self.android):
            1/0
            #see KEYCODE_PICTSYMBOLS in mats/appium/ui/device.py

        elif (self.ios):
            self.tap(self.strings.Next_keyboard)
            #alert says "you can switch to other keyboards..."
            self.tap(self.strings.OK, timeout=3)
        else:
            raise RuntimeError('bad platform')

    def switch_to_alphabet_keyboard(self):
        """
        while keyboard is open, tap to switch to the alphabet keyboard
        """
        if (self.android):
            1/0
            #see KEYCODE_PICTSYMBOLS in mats/appium/ui/device.py
        elif (self.ios):
            self.tap(self.strings.Next_keyboard)
        else:
            raise RuntimeError('bad platform')

    def clear_textfield(self, label, should_be_leftover=''):
        """
        For ios we'll select all/delete
        For android we'll hit delete a million times :(
        :param label: The accessibility label (or other tag) of the textfield
        """
        if (self.android):
            # NOTE!:
            #    There seems to be an animation delay issue here for Android.
            #    elem.clear() might take too long so if you try to do a tap
            #    after a call to this function, it might not work.
            #    This is our work around. What we have below works (so far)
            # TODO: test .clear() on Nike and clean this up...
            # Sergio: The commented code didn't work for me on Android
            #   For now, .clear() works
            elem = self.find(label)
            if (elem.text == should_be_leftover):
                return

            elem.clear()
            # self.device.move_cursor_to_end()
            # length = len(self.get_text(label))
            # self.device.delete(length)
        elif (self.ios):
            try:
                self.select_all(label)
                self.sleep(0.5)
                self.tap(self.strings.Delete)
            except WebDriverException:
                length = len(self.get_text(label))
                for x in range(length):
                    self.tap(self.strings.Delete)
        else:
            raise RuntimeError('bad platform')

        is_leftover = self.get_text(label)
        if (is_leftover != should_be_leftover):
            raise RuntimeError('tried to clear textfield, expected to see "%s" but still see "%s"' % (should_be_leftover, is_leftover))


    def select_all(self, label):
        """
        Selects all from textfield specified by "label"
        !!! This method does NOT handle the case where PART of the textfield is already selected !!!
        :param label: the textfield to select
        """
        if (self.android):
            #todo: write for android
            self.blocked('select_all() not implemented for android')
        elif (self.ios):
            elem = self.find(label)
            elem.tap(duration=1)
            self.sleep(.5)

            #be careful if changing/refactoring this.  I spent a lot of time with all the different cases
            try:
                #if button exists and IS visible, tap it
                #if button exists but IS NOT visible (menu shows Cut, Copy...), we already have a selection, just return
                sa_button = self.find(self.strings.Select_All)
                if (sa_button.visible):
                    sa_button.tap()
                return
            except NoSuchElementException:
                self.tap(label)

            self.tap(self.strings.Select_All)
        else:
            raise RuntimeError('bad platform')


    def copy_textfield(self, label):
        """
        IOS ONLY. Copies entire contents of textfield to OS clipboard using system copy just as if a user is tapping it.
        :param label: The accessibility label (or other tag) of the textfield
        """
        if (self.android):
            #todo: write for ios
            self.blocked('copy_textfield() not implemented for android')
        elif (self.ios):
            self.select_all(label)
            self.tap(self.strings.Copy)
        else:
            raise RuntimeError('bad platform')


    def cut_textfield(self, label):
        """
        IOS ONLY. Cuts entire contents of textfield to OS clipboard using system cut just as if a user is tapping it.
        :param label: The accessibility label (or other tag) of the textfield
        """
        if (self.android):
            #todo: write for ios
            self.blocked('cut_textfield() not implemented for android')
        elif (self.ios):
            self.select_all(label)
            self.sleep(.8)
            self.tap(self.strings.Cut)
        else:
            raise RuntimeError('bad platform')


    def paste_textfield(self, label):
        """
        IOS ONLY. Paste from OS clipboard using system copy just as if a user is tapping it.
        :param label: The accessibility label (or other tag) of the textfield
        """
        if (self.android):
            #todo: write for ios
            self.blocked('paste_textfield() not implemented for android')
        elif (self.ios):
            elem = self.find(label)
            txt = elem.text
            if (txt != ''):

                #clear out text if any.  sometimes there IS text but when we tap to try to Select All, it disappears
                #   for example the textfield may say "enter your name here" and when you tap, it becomes blank
                try:
                    self.select_all(label)
                except NoSuchElementException:
                    pass
            else:
                elem.tap(duration=1)
                self.sleep(.5)

            self.tap(self.strings.Paste)
        else:
            raise RuntimeError('bad platform')

    #     UIAEditingMenu[enabled, valid]
    #         UIAElement[enabled, valid, NAME:"Cut"]
    #         UIAElement[enabled, valid, NAME:"Copy"]
    #         UIAElement[enabled, valid, NAME:"Paste"]
    #         UIAElement[enabled, valid, NAME:"Delete"]
    #         UIAElement[enabled, valid, NAME:"Replace..."]
    #         UIAElement[enabled, valid, NAME:"Style options"]
    #         UIAElement[enabled, valid, NAME:"Define"]
    #         UIAElement[enabled, valid, NAME:"Learn..."]
    #         UIAElement[enabled, valid, NAME:"Speak"]
    #         UIAElement[enabled, valid, NAME:"Speak..."]
    #         UIAElement[enabled, valid, NAME:"Pause"]
    #         UIAElement[enabled, valid, NAME:"Right to left"]
    #         UIAElement[enabled, valid, NAME:"Left to right"]
    #         UIAElement[enabled, valid, NAME:"Show previous items"]
    #         UIAElement[enabled, valid, NAME:"Show more items"]
    #         UIAElement[enabled, valid, NAME:"Select"]
    #         UIAImage[enabled, valid]
    #         UIAImage[enabled, valid]
    #         UIAImage[enabled, valid]
    #         UIAElement[enabled, valid, NAME:"Select All"]
    #