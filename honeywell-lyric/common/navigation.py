import json, sys
from generic_flow import *

class NavigationFlow(object):
    def go_back(self):
        """
        android: tap HW back button
        ios: try to tap the < button and then the x button
        """
        if (self.ios):
            self.tap(["global_cancel_button", u'\u200b', 'CANCEL', 'Back', 'DONE'])
        else:
            self.device.back()

    def on_login_screen(self):
        return self.exists_and_visible(["login_username_textfield",
                                        "login_password_textfield",
                                        "login_login_button",
                                        "login_forgot_password_button"])

    def on_eula_screen(self):
        if self.ios:
            #TODO: Use AccIDs
            return self.exists_and_visible("HONEYWELL CONNECTED HOME PRIVACY STATEMENT AND END-USER LICENSE AGREEMENT", partial=True, timeout=5)
        elif self.android:
            return self.exists_and_visible(["EULA",
                                            "create_account_cancel_button",
                                            "create_account_accept_button"])
        return False

    def on_create_account_screen(self):
        if self.ios:
            return self.exists_and_visible(["create_account_first_name_textfield",
                                           "create_account_last_name_textfield",
                                           "create_account_email_textfield",
                                           "create_account_password_textfield",
                                           "create_account_verify_password_textfield"])
        elif self.android:
            return self.exists_and_visible(["create_account_first_name_textfield",
                                           "create_account_last_name_textfield",
                                           "create_account_email_textfield",
                                           "create_account_password_detail_label"])

    def on_forgot_password_screen(self):
        if self.ios:
            return self.exists_and_visible(["forgot_password_instructions_label",
                                            "forgot_password_email_textfield",
                                            "forgot_password_send_button"])
        elif self.android:
            return self.exists_and_visible(["forgot_password_instructions_label",
                                            "forgot_password_email_textfield",
                                            "forgot_password_send_button"])

    def on_home_screen(self, ohs_timeout=0):
        return self.exists_and_visible(["home_screen_current_temperature_button",
                                        "home_screen_new_otb_button"],
                                       timeout=ohs_timeout)

    def on_device_card_screen(self):
        return self.exists_and_visible(['device_card_current_temperature_button', 'device_card_temperature_dial'])

    def on_loc_settings_screen(self, timeout=0):
        """
        This is really a menu screen that you get to by tapping the Gear Icon for a location.
        It has the Location Details and Geofence Settings options among others
        """
        return self.exists_and_visible('location_settings_location_details_button', timeout=timeout)

    #--- On New OTB / Sub-screens ---
    def on_new_otb_screen(self):
        if self.ios:
            return self.exists_and_visible(["new_shortcut_trigger_type_spinner","new_shortcut_next_button"])
        elif self.android:
            return self.exists_and_visible(["new_shortcut_trigger_type_spinner", "new_shortcut_trigger_type_label"])

    def on_how_much_cooler_screen(self):
        return self.exists_and_visible(self.strings.How_Much_Cooler_)

    def on_how_much_warmer_screen(self):
        return self.exists_and_visible(self.strings.How_Much_Warmer_)

    def on_name_your_shortcut_screen(self):
        if self.ios:
            return self.exists_and_visible(self.strings.Name_Your_New_Shortcut)
        elif self.android:
            return self.exists_and_visible(self.strings.New_Shortcut)

    #--- On Secondary Card / Sub-screens ---

    def on_secondary_card_screen(self):
        return self.exists_and_visible(["secondary_card_home_settings_button", "secondary_card_away_settings_button",
                                        "secondary_card_sleep_brightness_mode_button",
                                        "secondary_card_sound_spinner",
                                        "secondary_card_sound_button"])

    def on_home_settings_screen(self):
        return self.exists_and_visible(["home_settings_when_cooling_button", "home_settings_when_heating_button"])

    def on_away_settings_screen(self):
        return self.exists_and_visible(["away_settings_when_cooling_button", "away_settings_when_heating_button"])

#----------------------------------------------
#     'Main screen / Dashboard' navigation
    def goto_home(self):
        # if we're already home
        if (self.on_home_screen()):
            return

        # if we're on a device card
        if (self.on_device_card_screen()):
            self.go_back()
            return

        if (self.on_loc_settings_screen()):
            self.go_back()
            #calling recursively here because sometimes the side drawer is still visible, so we need to hide it
            self.goto_home()

        # if the side drawer is open
        if self.is_side_drawer_visible():
            self.hide_side_drawer()


    def goto_device_card(self, device=None):
        self.log.debug("goto_device_card()")
        if (self.on_device_card_screen()):
            return

        if (device):
            tap_string = device.name
        else:
            tap_string = ['home_screen_current_temperature_button', 'home_stat_name']

        self.tap(tap_string)

        #sometimes this tap fails on both ios or android.  if the geofence notifications are on.  try tapping again.
        if (not self.on_device_card_screen()):
            self.log.warn('had to tap TWICE to get to the device card screen')
            self.sleep(1)
            self.tap(tap_string)

#------------------------------------------------------------
#           'App Settings'
#
# To get here:
#       Android: From Home screen -> Tap ... in upper right then "Settings"
#       ios: really no general "app settings" screen

    def goto_app_settings(self):
        if (self.android):
            self.goto_home()
            self.tap(self.strings.More_options)
            self.tap(self.strings.Settings)
        else:
            raise RuntimeError("This doesn't really exist for iOS")


#--------------------------------------------
#           side drawer navigation

    def open_side_drawer(self):
        if (self.is_side_drawer_visible()):
            #if it's already open, just exit...
            return True

        if self.ios:
            self.tap_safe('global_drawer_button')
        elif self.android:
            self.find(" navigation drawer", partial=True).tap_by_location()

        self.sleep(1)

        #if it's not open now, throw an error
        if (not self.is_side_drawer_visible()):
            raise RuntimeError('failed opening side drawer. for ios: app is likely frozen. android: do not know')

    show_side_drawer = open_side_drawer

    def close_side_drawer(self):
        if (not self.is_side_drawer_visible()):
            #if it's already closed, just exit...
            return True

        self.device.tap(.99, .3)
        self.sleep(1)

        #if it's open now, throw an error
        if (self.is_side_drawer_visible()):
            raise RuntimeError('failed closing side drawer.')

    hide_side_drawer = close_side_drawer

    def is_side_drawer_visible(self, first_name=None, last_name=None, timeout=0.5):
        self.sleep(1)
        if (self.ios):
            return self.exists_and_visible('side_drawer_location_settings_button', timeout=1)
        else:
            return (self.exists_and_visible(' navigation drawer', partial=True) and
                    not self.exists_and_visible('home_screen_hold_label'))

    is_side_drawer_open = is_side_drawer_visible

    def goto_location(self, loc):
        self.log.debug("In goto_location()")
        self.open_side_drawer()
        try:
            self.tap(loc.name, timeout=5) #may be a notif popup
        except NoSuchElementException:
            #weird error sometimes in android.  give it another try, see if this helps consistency
            self.close_side_drawer()
            self.open_side_drawer()
            self.sleep(5)
            self.tap(loc.name, timeout=5) #may be a notif popup

    def goto_location_settings(self, loc=None):
        if (loc):
            self.goto_location(loc)
        self.open_side_drawer()

        if (self.ios):
            self.tap("side_drawer_location_settings_button", timeout=5)  #may be a notif popup
            if not (self.on_loc_settings_screen(timeout=2)):
                raise RuntimeError('we tried to tap on the loc settings gear icon but we\'re not on the loc_settings screen.')
        if (self.android):
            # this is unbelievable.  the gear icon is clearly visible but reports that it offscreen.
            # this apparently gets better after about 7-10 seconds.  ridiculous.
            for i in range(30):
                e=self.wait_for_element("side_drawer_location_settings_button", timeout=5)
                if (e.location['x'] > 250):
                    # i have seen e.tap() fail sometimes, so we'll try tap_by_location() which should not fail
                    try:
                        e.tap_by_location()
                    except WebDriverException, e:
                        self.log.warn("Got exception: %s" % e.message)

                        # I actually think both of these Trys could be removed, but having them won't hurt anything.
                        #
                        try:
                            self.tap_by_location("side_drawer_location_settings_button")
                        except NoSuchElementException:
                            pass

                    if (not self.on_loc_settings_screen(timeout=2)):
                        raise RuntimeError('we tried to tap on the loc settings gear icon but we\'re not on the loc_settings screen.  Sometimes that tap registers as a tap on the homescreen that takes us to the thermostat screen.')
                    return
                self.log.warn("stupid location setting Gear Icon isn't behaving correctly.  attempt %s" % i)
                self.sleep(1)

            raise RuntimeError("waited but gear icon is nowhere to be found.")

    def goto_add_new_thermostat(self):
        self.open_side_drawer()
        self.tap('Add New Thermostat')

    def goto_messages(self):
        self.open_side_drawer()
        self.tap('Messages')

    def goto_privacy_policy(self):
        self.open_side_drawer()
        self.tap('Privacy Policy & EULA')

    def goto_tour_the_app(self):
        self.open_side_drawer()
        self.tap('Tour the App')

    def goto_help(self):
        self.open_side_drawer()
        self.tap('Help')

#----------------------------------------
#         'New OTB' navigation


#----------------------------------------
#         'Device card' navigation
# To get here:
# Main Screen or Dashboard -> Tap circle with temperature reading

    # Takes you to 'Secondary Card' (The Preferences screen)
    def goto_secondary_card(self, dev):
        self.log.debug("goto_secondary_card()")

        #if we need to navigate to the right location
        # if (not self.exists(dev.name)):
        #     self.goto_location(dev.loc)

        if self.ios:
            self.tap("device_card_preferences_button")
        elif self.android:
            self.tap("Secondary Controls")

#------------------------------------------------------------
#           'Thermostat Settings' / Preferences navigation
#
# To get here:
#     From Home screen -> Tap on circle icon to go to -> Device Card -> Tap on icon gear to go to -> Preferences

    def thermostat_settings_tap(self, option, suboptions=[]):
        options = ["Home Settings",
                   "Away Settings",
                   "Fan Mode",
                   "Auto Changeover",   # switch
                   "Hardware",
                   "Advanced Preferences"]
        if option in options:
            self.tap(option)
            if type(suboptions) == list:
                while suboptions != []:
                    self.tap_safe(suboptions.pop(0), timeout=1)



#--------------------------------------------
#           'Location Settings' navigation
#
# To get here:
# Main Screen -> Side drawer -> tap icon gear for 'Location settings'

    def loc_settings_tap2(self, option, suboptions=[]):
        options = ["Location Details",
                   "Thermostats",
                   "Notification Preferences",
                   "Users",
                   "Geofence this Location",    # When geofence is not set
                   "Geofence Size",
                   "DONE"]

        if option in options:
            if(option == "Geofence this Location"):
                # Geofencing is [SET]
                self.find_by_type("Switch").tap()
                self.sleep(1)
                ## Disabling will display a popup warning
                if(self.exists_and_visible("OK")):
                    self.tap_safe("OK")
            else:
                self.tap(option)
                if type(suboptions) == list:
                    while suboptions != []:
                        self.tap_safe(suboptions.pop(0), timeout=1)

    ######## Thermostats navigation ########
    # To get here:
    # Main Screen -> Side drawer -> tap icon gear for 'Location settings' -> Thermostats

    # TODO: do this correctly
    # Tap on 'current thermostat'
    # def current_thermostat(self):

    # Tap on 'Add a New Thermostat'
    def add_a_new_thermostat(self):
        self.tap("Add a New Thermostat")

    ######## 'Notification Preferences' navigation ########
    # To get here:
    # Main Screen -> Side drawer -> tap icon gear for 'Location settings' -> Notification Preferences
    # Tap selections available:
    #     Filter reminder
    #     Shortcuts
    #     Tips & Recommendations

    def notifications_tap_filter_reminder(self):
        self.tap("Filter reminder")

    def notifications_tap_shortcuts(self):
        self.tap("Shortcuts")

    # TODO: do this correctly
    def notifications_toggle_tips_and_recommendations(self):
        self.app.find_by_type("Switch").tap()
        pass

    ######## Users navigation ########
    # To get here:
    # Main Screen -> Side drawer -> tap icon gear for 'Location settings' -> Users
    # Tap selections available:
    #     'My Account'
    #     + ADD USER
    def users_tap_my_account(self):
        self.tap("My Account")
        pass

    def users_tap_add_user(self):
        self.tap("+ ADD USER")

    ######## 'Geofence Size' navigation ########
    # To get here:
    # Main Screen -> Side drawer -> tap icon gear for 'Location settings' -> Geofence Size
    #
    # **[Note]**:
    #     The existence of this screen is dependent if the user has already set-up geofence

    #-Close Tutorial toaster/pop-ups (2 of them)
    def geofence_size_close_tour(self):
        self.tap_safe("tour_close", timeout=1)
        self.tap_safe("tour_close", timeout=1)
