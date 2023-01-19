# -*- coding: utf-8 -*-
from generic_flow._external import *

class GeofenceFlow(object):

    def set_geofence(self, geofence, loc=None, recenter=True):

        #set location before viewing the map page.  moving location once we're on map page doesn't seem to work for ios
        if (recenter):
            self.set_geo_location(geofence.loc)
            self.sleep(2)

        self.goto_location_settings(loc)
        self.sleep(1)
        self.tap("location_settings_geofence_settings_button")
        self.set_geofence_size(geofence.radius, recenter)
        self.tap(self.strings.SAVE, timeout=15)
        if (self.ios):
            pass
            # do NOT do anything after tapping SAVE.  Some scripts will try to capture the Notification
            # so we have to return control to the script right after tapping SAVE
        else:
            self.wait_for_element(["location_settings_geofence_settings_button", "Geofence Settings"], timeout=60)
            self.goto_home()

    def recenter_geofence(self):

        # if error, try again, should work
        if (self.ios):
            self.sleep(8)
            self.device.tap(.9, .05)  # tap the (+) in the upper right to recenter on our location

            if (self.wait_for_element_safe(self.strings.we_can_t_determine_your_location__, timeout=2)):
                self.tap("OK")
                self.sleep(2)
                self.device.tap(.9, .05)
                self.sleep(.8)

            if (self.tap_safe(self.strings.Update)):
                self.sleep(1)
                return
            else:
                self.blocked("iOS simulator is screwed up. Trying to set location but not seeing '%s'" % self.strings.Update)
        else:
            self.sleep(2)
            self.device.tap(.9, .05)  # tap the (+) in the upper right to recenter on our location
            self.sleep(.8)
            self.tap(self.strings.Update)
            self.sleep(1)


    def set_geofence_size(self, size, recenter=True):

        lookup_dict                                 = AttrDict()
        lookup_dict.sim_iphone_4                    = AttrDict()
        lookup_dict.sim_iphone_4s                   = lookup_dict.sim_iphone_4

        lookup_dict.sim_iphone_5                    = AttrDict()
        lookup_dict.sim_iphone_5.small              = 0
        lookup_dict.sim_iphone_5.medium             = 2
        lookup_dict.sim_iphone_5.large              = 5
        lookup_dict.sim_iphone_5.start_y            = 262
        lookup_dict.sim_iphone_5.end_y              = 0    # the "end" positions for ios are OFFSETS, NOT the pixel you want to end on!
        lookup_dict.sim_iphone_5.start_x            = 240
        lookup_dict.sim_iphone_5.end_x_shrinking    = -100
        lookup_dict.sim_iphone_5.end_x_enlarging    = 80
        lookup_dict.sim_iphone_5s                   = lookup_dict.sim_iphone_5

        lookup_dict.sim_iphone_6                    = AttrDict()
        lookup_dict.sim_iphone_6_plus               = AttrDict()

        lookup_dict.moto_x                          = AttrDict()
        lookup_dict.moto_x.small                    = 0
        lookup_dict.moto_x.medium                   = 2
        lookup_dict.moto_x.large                    = 5
        lookup_dict.moto_x.start_y                  = 710
        lookup_dict.moto_x.end_y                    = 710
        lookup_dict.moto_x.end_x_shrinking          = 400
        lookup_dict.moto_x.end_x_enlarging          = 680

        #TODO: Modify these to be more accurate
        lookup_dict.moto_g                          = AttrDict()
        lookup_dict.moto_g.small                    = 0
        lookup_dict.moto_g.medium                   = 2
        lookup_dict.moto_g.large                    = 5
        lookup_dict.moto_g.start_y                  = 710
        lookup_dict.moto_g.end_y                    = 710
        lookup_dict.moto_g.end_x_shrinking          = 400
        lookup_dict.moto_g.end_x_enlarging          = 700

        lookup_dict.nexus_6                         = AttrDict()
        lookup_dict.nexus_6.small                   = 0
        lookup_dict.nexus_6.medium                  = 2
        lookup_dict.nexus_6.large                   = 5
        lookup_dict.nexus_6.start_y                 = 1320
        lookup_dict.nexus_6.end_y                   = 1320
        lookup_dict.nexus_6.end_x_shrinking         = 860
        lookup_dict.nexus_6.end_x_enlarging         = 1260


        #changes "moto x" to "moto_x" or "sim iphone 4" to "sim_iphone_4"
        model = self.device_model.replace(' ', '_')
        if (lookup_dict.has_key(model)):
            d = lookup_dict[model]
        else:
            raise RuntimeError("model not found in set_geofence_size()")

        #############################################
        # ok, now we can actually start doing some work...

        if (recenter):
            #skip tapping tour close buttons
            self.recenter_geofence()
        else:
            # on android, buttons have labels but page_source does not show correctly at all :(
            if (self.ios):
                self.tap_safe("tutorial_close_button", timeout=10)
                self.sleep(.75)
                self.tap_safe("tutorial_close_button", timeout=5)
                self.sleep(.75)
                self.tap_safe("tutorial_close_button", timeout=2) # sometimes the second tap doesn't correctly tap...

        #this is a guess at how long it'll take to draw the map.  we'll see if we can do intelligently later
        if (self.android):
            self.sleep(2)
        else:
            self.sleep(2)

        # minimize size based on the maximum size it could be...
        if (self.ios):
            for i in range(d.large):
                ta = TouchAction(self.driver)
                ta.press(x=d.start_x, y=d.start_y).move_to(x=d.end_x_shrinking, y=d.end_y).release().perform()
                self.sleep(3.5)

            # now increase size...
            for i in range(d[size]):
                ta = TouchAction(self.driver)
                ta.press(x=d.start_x, y=d.start_y).move_to(x=d.end_x_enlarging, y=d.end_y).release().perform()
                self.sleep(3.5)

        else:
            for i in range(d.large):
                self.geofence_size_decrease_radius(d)
                self.sleep(1.5)

            # now increase size...
            for i in range(d[size]):
                self.geofence_size_increase_radius(d)
                self.sleep(1.5)




    # Simulates dragging the black dot to the right to [IN]CREASE the geofence radius
    def geofence_size_increase_radius(self, d):
        # Increase radius of geolocation by dragging the black dot

        if (self.ios):
            # X = from 0.77 -> 0.99 (left to right)
            # Y = Keep at 0.53
            x = 0.77
            y = 0.53

            # TODO: Add/test more devices to add to array
            if (self.device_model in ['sim iphone 5s']):
                self.device.swipe(x, y, x + 0.22, y)
            else:
                raise RuntimeError("geofence_size_increase_radius() not supported with this device")
        else:
            # here's our hack due to not knowing where the black dot is.  we'll swipe to the right several times, with our starting point
            # starting from the center and slowly moving outward so we'll eventually grab the black button and pull it outward
            width = int(self.driver.get_window_size()['width'])
            start_x = width-11
            increment = width / 36
            while start_x > width / 2:

                ta = TouchAction(self.driver)
                ta.press(x=start_x, y=d.start_y).move_to(x=d.end_x_enlarging, y=d.end_y).release().perform()

                start_x -= increment

    # Simulates dragging the black dot to the left to [DE]CREASE the geofence radius
    def geofence_size_decrease_radius(self, d):
        # Increase radius of geolocation by dragging the black dot

        if (self.ios):
            # X = from 0.77 -> 0.99 (left to right)
            # Y = Keep at 0.53
            x = 0.77
            y = 0.53

            # TODO: Add/test more devices to add to array
            if (self.device_model in ['sim iphone 5s']):
                self.device.swipe(x, y, x - 0.22, y)
            else:
                raise RuntimeError("geofence_size_decrease_radius() not supported with this device")
        else:
            # here's our hack due to not knowing where the black dot is.  we'll swipe to the left several times, with our starting point
            # starting from the right edge and slowly moving inward so we'll eventually grab the black button and pull it toward the center
            width = int(self.driver.get_window_size()['width'])
            start_x = width / 2
            increment = width / 36
            while start_x < width - 11:
                ta = TouchAction(self.driver)
                ta.press(x=start_x, y=d.start_y).move_to(x=d.end_x_shrinking, y=d.end_y).release().perform()

                start_x += increment

    # Saves geofence size changes, if any.
    def geofence_size_tap_save(self):
        self.tap(self.strings.SAVE)

    # Cancel any changes made to geofence
    def geofence_size_tap_cancel(self):
        self.tap(self.strings.CANCEL)
        self.tap_safe(self.strings.YES)

    def verify_loc(self, home_away, device=None, timeout=None):
        """
        Creates some strings based on the stat's setpoints and looks for them on the screen
        """

        home_heat, home_cool, away_heat, away_cool = self.get_api().get_setpoints()

        if (self.ios):
            if (timeout==None):
                timeout = 140

            if (home_away == 'home'):
                temp_arr = ["The thermostat is set to %s degrees fahrenheit." % home_heat,
                            "The thermostat is set to %s degrees fahrenheit." % home_cool]
            else:
                temp_arr = ["The thermostat is set to %s degrees fahrenheit." % away_heat,
                            "The thermostat is set to %s degrees fahrenheit." % away_cool]

        elif (self.android):
            if (timeout == None):
                timeout = 300

            if (home_away == 'home'):
                temp_arr = [home_heat, home_cool]
            else:
                temp_arr = [away_heat, away_cool]

        self.goto_device_card(device)
        self.sleep(2) #sometimes the screen has the old value cached, so let's sleep a couple seconds to make sure we get the updated value.

        start_time = time.time()

        while True:
            if (self.android):
                current_temp = self.get_text('device_card_change_dialed_button')
            else:
                current_temp = self.get_text('device_card_desired_temperature_button')

            if (current_temp in temp_arr):
                return True

            if (time.time() - start_time > timeout):
                return False

            self.sleep(1)



#########################################################################################################
# notification stuff...

    def verify_push_notification(self, type=None, location=None, action=None, result=None, timeout=140):
        expected_body01, expected_body02 = self.get_notification_strings(type, location, action, result)

        start_time = time.time()

        while True:
            try:
                # actual_body is going to look like
                # 'Lyric, Arrived at location01 via trigger FenceCrossed: The response was "HouseIsOccupied", now, Notification'
                actual_body = self.driver.find_element_by_xpath("//UIAElement[contains(@name, \"%s\")]" % self.strings.Lyric_).text
                break
            except NoSuchElementException:
                pass

            if (time.time() - start_time > timeout):
                self.log.error("in verify_push_notification: never saw \"Lyric\".  Either notification did not show or we failed to trap it.")
                return False

        self.log.debug("verify_background_notification: expected_body01 : %s" % expected_body01)
        self.log.debug("verify_background_notification: expected_body02 : %s" % expected_body02)
        self.log.debug("verify_background_notification: actual_body : %s" % actual_body)

        # DO NOT change the following line to ==
        # sometimes we don't know what the previous state of the app was, so when we modify a fence, we can't
        # be sure if the fence modification is making us occupy the house or if it's "nosignificance"
        # so for example, expected title may == "The response was"
        # and actual title may be any of "The response was "NoSignificance"" or "The response was "HouseIsOccupied"" or "The response was "HouseIsEmpty""
        return (expected_body01 in actual_body and expected_body02 in actual_body)

    def verify_notification(self, type=None, location=None, action=None, result=None, timeout=30):
        if (not self.geofence_notifications_on):
            raise RuntimeError("verify_location(): you called verify_notification() but notifications are not turned on")

        if self.android:
            self.open_notifications()

            actual_lyric_notif      = self.wait_for_element_to_exist(self.strings.Shortcut_was_activated_by_Geofencing_, partial=True).name
            actual_geofence_notif   = self.wait_for_element_to_exist(self.strings.with_event_response, partial=True).name

            expected_lyric_notif, expected_geofence_notif = self.get_notification_strings(type, location, action, result)

            self.log.debug("verify_notification: expected_lyric   : %s" % expected_lyric_notif)
            self.log.debug("verify_notification: actual_lyric     : %s" % actual_lyric_notif)
            self.log.debug("verify_notification: expected_geofence: %s" % expected_geofence_notif)
            self.log.debug("verify_notification: actual_geofence  : %s" % actual_geofence_notif)

            self.clear_all_notifications()
            self.switch_apps()

            # "expected"s are RegExs
            return (expected_lyric_notif.search(actual_lyric_notif) and expected_geofence_notif.search(actual_geofence_notif))

        elif self.ios:
            if (not self.trap_notification(timeout)):
                self.log.error("in verify_notification: never saw the DETAILS button.  Either notification did not show or we failed to trap it.")
                return False

            self.sleep(1)

            actual_title = self.wait_for_element_to_exist(self.strings.via_trigger, partial=True).text
            actual_body  = self.wait_for_element_to_exist(self.strings.The_response_was, partial=True).text

            expected_title, expected_body = self.get_notification_strings(type, location, action, result)

            self.log.debug("verify_notification: expected_title: %s" % expected_title)
            self.log.debug("verify_notification: actual_title  : %s" % actual_title)
            self.log.debug("verify_notification: expected_body : %s" % expected_body)
            self.log.debug("verify_notification: actual_body   : %s" % actual_body)

            self.tap(self.strings.OK)

            # DO NOT change the following line to ==
            # sometimes we don't know what the previous state of the app was, so when we modify a fence, we can't
            # be sure if the fence modification is making us occupy the house or if it's "nosignificance"
            # so for example, expected title may == "The response was"
            # and actual title may be any of "The response was "NoSignificance"" or "The response was "HouseIsOccupied"" or "The response was "HouseIsEmpty""
            return expected_title in actual_title and expected_body in actual_body

    def get_latest_notification(self, notification_type):
        """
        @type  notification_type: string
        @param notification_type: Retrieve either Geofence or Lyric notifications
        @rtype:                   AttrDict, bool
        @return:                  If found: a dictionary of the latest notification with keys for trigger type, location, action, and result
                                        Lyric: location, shortcut_name, trigger
                                        Geofence: types, action, location, response
                                  Else: False
        """
        self.blocked_on_ios("get_latest_geo_notification(): Method is not for iOS")
        assert (notification_type in ["Lyric", "Geofence"]), "get_latest_notification() -> Invalid argument supplied: %s" % notification_type

        self.open_notifications()

        notif_text = ""
        if notification_type == "Lyric":
            notif_text = self.wait_for_element_safe("Shortcut was activated by", element_type="statictext", partial=True)
            # Match this pattern:
            # At ''location01'' the 'geo_away' Shortcut was activated by Geofencing.
            regexp = "At \'\'(\w+)\'\' the \'\'(\w+)\'\' Shortcut was activated by (\w+)"
        elif notification_type == "Geofence":
            notif_text = self.wait_for_element_safe(self.strings.with_event_response, element_type="statictext", partial=True)
            # Match this pattern:
            # [LoggedIn] triggered (UserArrived|UserDeparted) at "location" with event response (NoSignificance|HouseIsOccupied|HouseIsEmpty)
            # [LoggedIn, HomeAwayStatusChange] triggered (UserArrived|UserDeparted) at "location" with event response (NoSignificance|HouseIsOccupied|HouseIsEmpty)
            regexp = "\[(.*)\] triggered (\w+) at (.+) with event response (\w+)"
        if notif_text:
            notif_text = notif_text.text
            matches = re.search(regexp, notif_text)

            notification = AttrDict()
            if notification_type == "Lyric":
                notification.location      = matches.group(1).lower()
                notification.shortcut_name = matches.group(2).lower()
                notification.result        = matches.group(3).lower()
            elif notification_type == "Geofence":
                notification.types         = matches.group(1).lower().split(", ")
                notification.action        = matches.group(2).lower()
                notification.location      = matches.group(3).lower()
                notification.result        = matches.group(4).lower()
        else:
            notification = False

        self.switch_apps()
        return notification

    def trap_notification(self, timeout):
        """
        This kind of sucks because we're circumventing our whole "find" scheme, but we have to make this
        work extremely fast so we're going right to Flow.driver
        So why is "find" slower you ask?  Because it does all three of the following (making scripting much easier):
            find_elements_by_accessibility_id()
            find_elements_by_xpath("value=")
            find_elements_by_xpath("text=")
        """
        if (self.android):
            print "Android: This method should not be used. You must check the notification center to view the notification"
        else:
            start_time = time.time()

            while True:
                #if you use the plural version of find you don't have to worry about exception handling...
                elems = self.driver.find_elements_by_accessibility_id(self.strings.DETAILS)

                if (elems):

                    # If there are multiple notifs that pop up quickly the first one may disappear (so when we try to click we'll get a WDException)
                    # so do a find/click again.  This has been a successful strategy so far.
                    for i in range(5):
                        try:
                            self.driver.find_elements_by_accessibility_id(self.strings.DETAILS)[0].click()
                            return True
                        except (IndexError, WebDriverException):
                            pass
                    raise RuntimeError("saw DETAILS but failed to tap it...")

                if (time.time() - start_time > timeout):
                    return False

    def trap_push_notification(self, timeout):
        """
        This kind of sucks because we're circumventing our whole "find" scheme, but we have to make this
        work extremely fast so we're going right to Flow.driver
        So why is "find" slower you ask?  Because it does all three of the following (making scripting much easier):
            find_elements_by_accessibility_id()
            find_elements_by_xpath("value=")
            find_elements_by_xpath("text=")
        """
        if (self.android):
            pass
        else:
            start_time = time.time()

            while True:
                #if you use the plural version of find you don't have to worry about exception handling...
                elems = self.driver.find_elements_by_xpath("//*[contains(@name, \"Lyric\")]")

                if (elems):
                    txt = elems[0].text

                    #tap very top center of the screen
                    self.device.tap(.5,.1)
                    return txt

                if (time.time() - start_time > timeout):
                    return False

    def get_notification_strings(self, type, location, action, result):

        if (self.ios):
            # Departed location01 via trigger FenceCrossed
            # Arrived at location01 via trigger FenceCrossed
            if (type.lower() == 'fencecrossed'):
                type = 'FenceCrossed'

            # Departed location01 via trigger GeofenceModified
            # Arrived at location01 via trigger GeofenceModified
            elif (type.lower() == 'geofencemodified'):
                type = 'GeofenceModified'

            elif (type.lower() in ['login','loggedin']):
                type = 'LoggedIn'
            else:
                raise RuntimeError ("in get_notification_strings(). received bad 'type' argument: %s" % type)


            if (action.lower() in ['arrive', 'arrived', 'arrived at']):
                action = 'Arrived at'
            elif (action.lower() in ['depart', 'departed']):
                action = 'Departed at'
            else:
                raise RuntimeError ("in get_notification_strings(). received bad 'action' argument: %s" % action)

            if (result.lower() in ['occupied', 'houseoccupied', 'houseisoccupied']):
                result = '"HouseIsOccupied"'
            elif (result.lower() in ['empty', 'houseempty', 'houseisempty']):
                result = '"HouseIsEmpty"'
            elif (result.lower() in ['none', 'no', 'nosignificance']):
                result = '"NoSignificance"'

            # This is for the case where we don't know the previous state of the user/app so we're not sure if we're creating a significant event or not
            elif (result.lower() == '?'):
                result = ''
            else:
                raise RuntimeError ("in get_notification_strings(). received bad 'result' argument: %s" % result)

            return ("%s %s %s %s" % (action, location.name, self.strings.via_trigger, type),
                    "%s %s" % (self.strings.The_response_was, result))
        #android
        else:
            #[GeofenceModified, FenceCrossedIn] triggered UserArrived at location01 with event response NoSignificance
            #[GeofenceModified, FenceCrossedIn] triggered UserArrived at location01 with event response HouseIsOccupied
            #[FenceCrossedOut] triggered UserDeparted at location01 with event response HouseIsEmpty

            if (action.lower() in ['arrive', 'arrived', 'arrived at']):
                action = 'UserArrived at'
            elif (action.lower() in ['depart', 'departed']):
                action = 'UserDeparted at'
            else:
                raise RuntimeError ("in get_notification_strings(). received bad 'action' argument: %s" % action)

            if (type.lower() == 'fencecrossed'):
                if (action == 'UserArrived at'):
                    type = 'FenceCrossedIn'
                elif (action == 'UserDeparted at'):
                    type = 'FenceCrossedOut'

            elif (type.lower() == 'geofencemodified'):
                type = 'GeofenceModified'

            elif (type.lower() in ['login', 'loggedin']):
                type = 'LoggedIn'
            else:
                raise RuntimeError("in get_notification_strings(). received bad 'type' argument: %s" % type)

            if (result.lower() in ['occupied', 'houseoccupied', 'houseisoccupied']):
                result = 'HouseIsOccupied'
            elif (result.lower() in ['empty', 'houseempty', 'houseisempty']):
                result = 'HouseIsEmpty'
            elif (result.lower() in ['none', 'no', 'nosignificance']):
                result = 'NoSignificance'

            # This is for the case where we don't know the previous state of the user/app so we're not sure if we're creating a significant event or not
            elif (result.lower() == '?'):
                result = ''
            else:
                raise RuntimeError("in get_notification_strings(). received bad 'result' argument: %s" % result)

            re_string_lyric = '.*%s.* %s %s %s %s %s' % (type, self.strings.triggered, action, location.name, self.strings.with_event_response, result)
            re_string_lyric = re.compile(re_string_lyric)

            #At ''location01'' the ''geo_away'' Shortcut was activated by Geofencing. 3/23/2015 2:07:03 AM
            re_string_geo   = ".*%s.*%s.*%s" % (location.name, ".*", self.strings.Shortcut_was_activated_by_Geofencing_)
            re_string_geo   = re.compile(re_string_geo)

            return (re_string_lyric, re_string_geo)




