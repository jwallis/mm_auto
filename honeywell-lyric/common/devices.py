from generic_flow import *

class DeviceFlow(object):

###################################################################################################
# Thermostat...

    def set_heat_cool(self, mode, device=None):
        assert (mode in ["cool", "heat", "off"]), "common/devices/set_heat_cool(): Invalid argument: %s" % mode

        self.goto_device_card(device)
        if (self.ios):
            try:
                #bad
                if (mode == 'cool'):
                    self.tap("device_card_cool_button")
                    self.tap("device_card_cool_button")
                elif (mode == 'heat'):
                    self.tap("device_card_heat_button")
                    self.tap("device_card_heat_button")
                elif (mode == 'off'):
                    self.tap("device_card_desired_temperature_button")
                    self.tap("device_card_off_button")
            except NoSuchElementException:
                pass
        else:
            self.tap("device_card_current_temp_box")
            if (mode == 'cool'):
                self.tap("device_card_cool_button")
            elif (mode == 'heat'):
                self.tap("device_card_heat_button")
            elif (mode == 'off'):
                self.tap('device_card_off_button')

            else:
                raise RuntimeError('must be "heat" or "cool" or "off"')

    def temperature_swipe(self, direction):
        assert direction in ["increase", "decrease"], "Invalid argument \"%s\". Use \"increase\" or \"decrease\"" % direction

        if direction == "increase":
            if (self.ios and self.device_model in ['sim iphone 5s']):
                from_x = 0.3
                to_x   = 0.99
                from_y = to_y = 0.9
            elif (self.android and self.device_model in ['moto x', 'moto g', 'nexus 6']):
                from_x = 0.3
                to_x   = 0.99
                from_y = to_y = 0.9
            else:
                raise RuntimeError("increase_temperature() not supported with this device")
        elif direction == "decrease":
            if (self.ios and self.device_model in ['sim iphone 5s']):
                from_x = 0.99
                to_x   = 0.3
                from_y = to_y = 0.9
            elif (self.android and self.device_model in ['moto x', 'moto g']):
                from_x = 0.99
                to_x   = 0.3
                from_y = to_y = 0.9
            elif (self.android and self.device_model in ['nexus 6']):
                from_x = 0.9
                to_x = 0.3
                from_y = to_y = 0.9
            else:
                raise RuntimeError("increase_temperature() not supported with this device")

        self.driver.swipe(from_x, from_y, to_x, to_y)

    def increase_temperature(self, current_screen, timeout=5):
        assert current_screen in ["device_card", "home","away"], \
            "Invalid argument \"%s\". Use \"device_card\", \"home\" or \"away\" as arguments." % current_screen
        self.log.debug("increase_temperature()")

        getter_method = None
        if current_screen == "device_card":
            getter_method = self.get_ui_set_temperature
        elif current_screen in ["home", "away"]:
            getter_method = self.get_ui_setpoint_temperature

        self.call_and_verify_change(lambda: self.temperature_swipe("increase"), getter_method, timeout)

    def decrease_temperature(self, current_screen, timeout=5):
        assert current_screen in ["device_card", "home","away"], \
            "Invalid argument \"%s\". Use \"device_card\", \"home\" or \"away\" as arguments." % current_screen
        self.log.debug("decrease_temperature()")

        getter_method = None
        if current_screen == "device_card":
            getter_method = self.get_ui_set_temperature
        elif current_screen in ["home", "away"]:
            getter_method = self.get_ui_setpoint_temperature

        self.call_and_verify_change(lambda: self.temperature_swipe("decrease"), getter_method, timeout)

    # For this button to appear, you must tap on either the cool icon or the heat icon until OFF appears,
    #   then it becomes visible.
    def device_card_tap_off(self):
        if(self.exists_and_visible("device_card_off_button")):
            self.tap("device_card_off_button")

    def device_card_tap_heat(self):
        self.tap("device_card_heat_button")

    # Shows the current weather
    def device_card_tap_weather(self):
        self.tap("device_card_weather_button")

    # Triggers the 'How long will you be gone ?' menu
    def device_card_tap_smartaway(self):
        self.tap("device_card_away_button")

    def set_fan_mode(self, new_mode):
        if self.ios:
            self.tap("secondary_card_fan_mode_button")
            self.tap(new_mode, timeout=1)
            self.go_back()
        elif self.android:
            self.tap("secondary_card_fan_mode_spinner")
            self.tap(new_mode, timeout=1)

    def brightness_swipe(self, current, new):
        # TODO: Add/test more devices to add to array
        if (self.device_model in ['sim iphone 5s']):
            self.driver.swipe(0.25 + 0.1 * (current / 2), 0.3, 0.25 + 0.1 * (new/2), 0.3)
        elif (self.device_model in ["moto x", "moto g", "nexus 6"]):
            self.driver.swipe(0.2 + 0.146 * (current / 2), 0.5, 0.2 + 0.146 * (new/2), 0.5)
        # Genymotion: Moto X 720x1280
        elif (self.device_model in ["genymotion"]):
            self.driver.swipe(0.07 + 0.1721 * (current / 2), 0.5, 0.07 + 0.1721 * (new/2), 0.5)
        else:
            raise RuntimeError("set_brightness() not supported with this device")

    def set_brightness(self, current, new):
        assert (0 <= current) and (current <= 10)
        assert (0 <= new) and (new <= 10)

        if self.on_secondary_card_screen():
            self.tap_on_page("secondary_card_sleep_brightness_mode_button")
        else:
            raise RuntimeError("set_brightness(): We are not on Secondary Card screen")
        self.sleep(1)

        self.brightness_swipe(current, new)

        # Android: Needs to return all the way back to device card for settings to update to CHAPI
        # iOS: Will do the same for the sake of consistency
        if self.android:
            self.tap("OK")
        elif self.ios:
            self.go_back()
        self.go_back()

        self.sleep(0.5)
        assert self.on_device_card_screen(), "We are not on device card screen"

    # Gets the current temperature read by the thermostat
    def get_ui_current_temperature(self):
        if self.on_device_card_screen():
            if self.ios:
                current_temp = self.find("The current temperature is", partial=True).text
                regexp = "The current temperature is ([0-9]+) degrees"
                match = re.search(regexp, current_temp)
                current_temp = match.group(1)
            else:
                current_temp = self.find("device_card_current_temp_box").text
            return current_temp
        else:
            raise RuntimeError("get_ui_current_temperature(): Not on the device card screen to adjust the temperature")

    # Gets the temperature (desired) set or programmed by the user
    def get_ui_set_temperature(self):
        if self.on_device_card_screen():
            if self.ios:
                set_temp = self.find("The thermostat is set to", partial=True).text
                regexp = "The thermostat is set to ([0-9]+) degrees"
                match = re.search(regexp, set_temp)
                set_temp = match.group(1)
            else:
                set_temp = self.find("device_card_change_dialed_button").text
            return set_temp
        else:
            raise RuntimeError("get_ui_set_temperature(): Not on the device card screen to adjust the temperature")

    # Gets the current temperature from the home/away setpoint dial thermostat screen
    def get_ui_setpoint_temperature(self):
        if self.ios:
            if self.exists_and_visible(["icon_cool", "icon_heat"]):
                current_temp = self.find("degrees", partial=True).text
                regexp = "([0-9]+) degrees"
                match = re.search(regexp, current_temp)
                current_temp = match.group(1)
            else:
                raise RuntimeError("get_ui_setpoint_temperature(): Not on the dial screen where you adjust the temperature")
        else:
            # There's no guaranteed way to check if we are looking at
            # the dial change temperature screen on Android as of now (4/10/2015)
            current_temp = self.statictext().text
        return current_temp

    def set_thermostat_volume(self, vol):
        assert (self.on_secondary_card_screen()), "set_thermostat_volume(): We are not on the secondary card screen"

        if(self.ios):
            self.tap_on_page("secondary_card_sound_button")
        elif self.android:
            self.tap_on_page("secondary_card_sound_spinner")
        self.tap_safe(vol, timeout=1)

        # On Android, we need to return to the secondary card screen to refresh changes to CHAPI. We'll
        # keep that behavior on iOS for the sake of consistency
        self.go_back()
        if self.ios:
            self.go_back()

    def set_ventilation(self, option):
        self.tap("Ventilation")
        self.tap(option)
        self.tap("Back")

    def wait_for_value_update(self, method, old_value, timeout=5):
        '''
        wait_for_value_update():
            This method will call a method, check the return value under an elapsed amount of time
        If the return value of the method is equal to current_value, then it will continue calling the method for x seconds
        If the return value of the method differs from current_value, it will stop calling the method and return the value
        After the elapsed time, it will timeout and return current_value
           Useful for api/network-related use cases

        Method takes in a method binding, the current value after calling that method, and a timeout in seconds

        You can use it like this:
        For a function with no arguments: (Notice there are no parentheses after the method name)
            wait_for_value_update(method_to_call, current_value, 10, timeout=10)

        For a function with arguments you have to use the lambda syntax:
            wait_for_value_update(lambda: method_to_call(argument1, argument2), current_value, 10, timeout=10)

        '''
        start_time = time.time()
        new_value = old_value

        while(old_value == new_value):
            new_value = method()
            if((time.time() - start_time) > timeout):
                break
            self.sleep(1)
        return new_value

    def call_and_verify_change(self, action_method, getter_method, timeout=5):
        '''
        call_and_verify_change():
            This method is similar to wait_for_value_update; but this time it will take in two methods: one is
        the "action method" and the other is the "getter method". Under an elapsed amount of time, it will
        call a method that performs an action or some change. The getter method should reflect that change.
        Like wait_for_value_update(), this waits for a change after performing an action, the difference is that this
        method continuously performs an action (calls a method), and polls the getter method to see whether a change has
        occurred.

        You can use it like this:
        For a function with no arguments (Notice there are no parentheses after the method name)
            call_and_verify_change(action_method, getter_method, timeout=10)

        For a function with arguments you have to use the lambda syntax:
            call_and_verify_change(lambda: action_method(arg1, arg2), lambda: getter_method(arg1, etc), timeout=10)

        '''
        start_time = time.time()
        original_value = new_value = getter_method()

        while(original_value == new_value):
            action_method()
            new_value = getter_method()
            if((time.time() - start_time) > timeout):
                break
            self.sleep(1)
        return new_value
