# -*- coding: utf-8 -*-
from generic_flow import *

class LoginFlow(object):

    def _goto_env_screen(self):
        """
        do the secret gesture to open teh developer screen
        """

        # If I try to run the scripts with "runner" I get the Unable to load Appium Server etc. etc.
        self.wait_for_element_to_exist("login_forgot_password_button")

        if (self.ios):
            try:
                self.device.tap(.5,.2, duration=11)
                self.wait_for_element_to_exist("Special Settings", timeout=3)
            except NoSuchElementException:
                self.log.warning("tapped for 11s and did not take us to hidden menu.  now trying for 14s.  if you see this err a lot, maybe that first tap should be increased to > 11s")
                self.device.tap(.5, .2, duration=14)
                self.wait_for_element_to_exist("Special Settings", timeout=10)
        else:
            ta = TouchAction(self.driver)

            for i in range(10):
                # works for moto x, moto g, nexus 6
                ta.press(x=120, y=250).wait(100).move_to(x=120, y=920).wait(100).move_to(x=120, y=650).wait(100).move_to(x=620, y=650).wait(100).move_to(x=620, y=920).wait(100).release().perform()
                # else:
                #     raise RuntimeError("unsupported model type: %s" % self.device_model)

                if (self.exists_and_visible('Web Server Url', timeout=1)):
                    return

                self.sleep(.5)

            raise RuntimeError("in _goto_env_screen(): tried 10 times to go to env screen and failed.")

    def set_env(self, show_geofence_alerts=False):
        """
        open developer screen and set to our testing environment
        :env: the name of the testing environment
        """
        self._goto_env_screen()

        if (self.ios):

            ########## set the environment name to open the PickerWheel
            #if we don't see the env name we're trying to set, then we still need to set it
            if (not self.exists(self.data.env.ios)):

                tcs = self.table().tablecells()

                for i in range(len(tcs)):
                    if (tcs[i].name == self.strings.Environment):
                        tcs[i+1].tap()
                        break

                self.sleep(1)
                #TODO: Issue with line below
                if (self.device_model in ['sim iphone 5', 'sim iphone 5s']):
                    if (self.data.env.ios == 'Backup (Stage)'):
                        self.device.tap(.5, .8) # tap on the PickerWheel to select the environment
                else:
                    raise RuntimeError("please update login.py for your device_model")

                # after we tap the PickerWheel, we should see the environment's name, and it should be the env name specified If not, stop the test
                if (not self.find(self.data.env.ios, partial=True)):
                    raise RuntimeError('Tried to get to the testing environment but did not')
                self.tap("OK")


            ######### turn on alerts if not already on
            if (show_geofence_alerts and not self.exists(self.strings.Show_geofence_alerts)):
                self.tap('geofence alerts', partial=True)

                self.sleep(1)
                #TODO: Issue with line below
                if (self.device_model in ['sim iphone 5', 'sim iphone 5s']):
                    if (self.data.env.ios == 'Backup (Stage)'):
                        self.device.tap(.5, .7) # tap on the PickerWheel to select the environment
                else:
                    raise RuntimeError("please update login.py for your device_model")

                # after we tap the PickerWheel, we should see "Show geofence alerts", if not, stop the test
                if (not self.exists(self.strings.Show_geofence_alerts, partial=True)):
                    raise RuntimeError('Tried to turn on geofence alerts but could not')
                self.tap("OK")

            ######### turn off alerts if on
            elif (not show_geofence_alerts and not self.exists(self.strings.Do_not_show_geofence_alerts)):
                self.tap('geofence alerts', partial=True)

                self.sleep(1)
                #TODO: Issue with line below
                if (self.device_model in ['sim iphone 5', 'sim iphone 5s']):
                    if (self.data.env.ios == 'Backup (Stage)'):
                        self.device.tap(.5, .8) # tap on the PickerWheel to select the environment
                else:
                    raise RuntimeError("please update login.py for your device_model")

                # after we tap the PickerWheel, we should see "Show geofence alerts", if not, stop the test
                if (not self.exists(self.strings.Do_not_show_geofence_alerts, partial=True)):
                    raise RuntimeError('Tried to turn OFF geofence alerts but could not')
                self.tap("OK")

            self.geofence_notifications_on = self.exists(self.strings.Show_geofence_alerts)

            self.tap("DONE", timeout=10)
        else:
            self.tap(self.strings.Geo_fence)
            geofence_notif_checkbox = self.find(self.strings.Enable_geo_fence_notifications)

            # Geofence notifications ARE desired, we make sure to enable if it's OFF
            if(show_geofence_alerts and geofence_notif_checkbox.checked() == False):
                geofence_notif_checkbox.tap()

            # Geofence notifications NOT desired, we make sure to disable if it's ON
            if(not show_geofence_alerts and geofence_notif_checkbox.checked() == True):
                geofence_notif_checkbox.tap()

            self.geofence_notifications_on = self.find(self.strings.Enable_geo_fence_notifications).checked()
            self.device.back()

            self.tap('Web Server Url')
            self.tap(self.data.env.android)
            self.device.back()

    def login(self, user, clear_tut=True, show_geofence_alerts=False, skip_all=False):
        """
        set the environment, then log in
        """

        self.log.debug('login')
        self.wait_for_element("login_username_textfield")
        self.set_env(show_geofence_alerts)

        self.current_user = user

        if (self.ios):
            self.set_text("login_username_textfield", user.username)
            self.set_text("login_password_textfield", user.password)
            self.tap("login_login_button")

            #for testing notifications after login
            if (skip_all):
                return

            # Logging in may take a while (or may never succeed due to network issues)
            self.wait_for_element_to_exist(["Lyric","global_drawer_button"], partial=True, timeout=60)
            self.sleep(2)
            self.tap_safe('Allow', timeout=5)  # wait for OK.  If we don't, we'll actually see the Allow, then OK, then Allow again...   :(
            self.tap_safe('OK', timeout=2)
        else:
            self.find("login_username_textfield").send_keys(user.username)
            self.find("login_password_textfield").send_keys(user.password)
            self.tap("login_login_button")

        if (clear_tut):
            self.clear_tutorial()

        if (self.ios):
            #for some reason, tapping the hamburger right when we log in fails a lot on automini01, sleeping seems to fix this
            self.sleep(1.5)


    def clear_tutorial(self):
        if (self.tap_safe("tutorial_close_button", timeout=10)):
            self.sleep(.75)
            self.tap_safe("tutorial_close_button", timeout=5)
            self.sleep(.75)
            self.tap_safe("tutorial_close_button", timeout=5)
            self.sleep(.75)
            self.tap_safe("tutorial_close_button", timeout=3) # sometimes the first tap fails

    def logout(self):
        if self.android:
            self.tap("More options")
            self.tap('Logout')
        elif self.ios:
            self.tap("global_drawer_button")
            self.tap("side_drawer_logout_button")

        try:
            self.wait_for_element_to_exist('login_username_textfield')
        except:
            raise RuntimeError('Logout failed.  We tapped the button but never saw the login screen.')

        self.current_user = None

        if (self.api and not type(self.api) == mats.appium.ui.elements.UndefinedElement):
            self.api.logout()
            self.api = None


    def login_and_logout(self, user, clear_tut=True, show_geofence_alerts=False, set_loc=None, timeout=0):
        """
        pretty simple
        a timeout value of 140s should be used if you want to wait for geofence triggers to update
        """
        self.login(user, clear_tut=clear_tut, show_geofence_alerts=show_geofence_alerts)
        if (set_loc):
            self.set_geo_location(set_loc)
            if (timeout<5):
                self.sleep(5)

        self.sleep(timeout)
        self.logout()

    def logout_and_login(self, user, clear_tut=True, show_geofence_alerts=False, timeout=0):
        self.logout()
        self.sleep(timeout)
        self.login(user, clear_tut=clear_tut, show_geofence_alerts=show_geofence_alerts)

    def verify_login_button_is_disabled(self):
        return self.find("login_login_button").enabled is False


###################################################################################
# a few random methods.  maybe these should go in their own file (or navigation.py)

    def screenshot_version(self, user):
        if (self.android):
            self.login(user)
            self.goto_app_settings()
        else:
            # unfortunately, the version # on the env_screen is incorrect unless we start pulling builds from hockey
            # self._goto_env_screen()
            self.log.info("screenshot_version is inaccurate for iOS.  try 'grep \"app version\" master.log' or 'grep \"code branch\" master.log'")
            return

        self.device.screenshot('app_version')

    def dismiss_location_services_dialog(self):
        if (self.android):
            self.tap_safe(self.strings.Cancel, timeout=5)
            self.sleep(1)
        elif (self.ios):
            # probably should NOT do anything here because the next method call after this in some
            # scripts is verify_notification(), which is time-dependent
            pass

    def retry_connection(self):
        """
        after turn wifi back on (or airplane off), we may need to hit RETRY to reconnect
        """
        if (self.android):
            if (self.tap_safe(self.strings.RETRY_)):

                for i in range(30):
                    self.sleep(1)
                    if (not self.exists(self.strings.Loading_)):
                        #should we also put a "not exists(retry)" here as well just to be sure?
                        break
                raise RuntimeError('tried to dismiss "Retry Connection" message but could not')
        else:
            if (self.tap_safe(self.strings.Retry)):

                for i in range(30):
                    self.sleep(1)
                    if (not self.exists(self.strings.Retry)):
                        #should we also put a "not exists(retry)" here as well just to be sure?
                        break
                raise RuntimeError('tried to dismiss "Retry Connection" message but could not')

        #give the app a couple seconds to get to a happy state.  We've seen (especially in android)
        #where if it comes back and the RETRY overlay automatically disappears, it will be in a weird state for a bit
        self.sleep(2)
