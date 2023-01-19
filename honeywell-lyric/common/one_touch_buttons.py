from generic_flow import *

class OneTouchButtonsFlow(object):
    def get_all_shortcuts(self):
        assert (self.on_home_screen()), "Not on the \"Home Screen\""

        if self.ios:
            return [label.text for label in self.find_all("home_screen_shortcut_label")]
        elif self.android:
            return [label.statictext().text for label in self.find_all("home_screen_shortcut_label")]
        else:
            raise RuntimeError("Unknown platform")

    def get_when_heating(self):
        assert (self.on_how_much_cooler_screen() or self.on_how_much_warmer_screen()), \
            "Not on the \"How Much Cooler\" or \"How Much Warmer\" screen."

        heat_value = None
        if self.ios:
            regexp = "([0-9]{1,3}) degrees"
            heat_circle_label = self.find("new_shortcut_custom_when_heating_label").text
            heat_value = int(re.search(regexp, heat_circle_label).group(1))
        elif self.android:
            heat_value = int(self.find("new_shortcut_custom_when_heating_label").text)
        return heat_value

    def get_when_cooling(self):
        assert (self.on_how_much_cooler_screen() or self.on_how_much_warmer_screen()), \
            "Not on the \"How Much Cooler\" or \"How Much Warmer\" screen."

        cool_value = None
        if self.ios:
            regexp = "([0-9]{1,3}) degrees"
            cool_circle_label = self.find("new_shortcut_custom_when_cooling_label").text
            cool_value = int(re.search(regexp, cool_circle_label).group(1))
        elif self.android:
            cool_value = int(self.find("new_shortcut_custom_when_cooling_label").text)
        return cool_value

    # New OTB -> Pick a trigger
    def new_shortcut_pick_trigger(self, desired_selection, direction="down"):
        assert (self.on_new_otb_screen()), "new_shortcut_choose_trigger(): Must be on the New OTB/shortcut screen"

        assert (desired_selection in [self.strings.new_otb_press_shortcut,
                                 self.strings.new_otb_specific_time,
                                 self.strings.new_otb_house_empty,
                                 self.strings.new_otb_someone_home]), \
                                "new_shortcut_choose_trigger(): Invalid argument for desired_selection: %s" % (desired_selection)

        self.tap("new_shortcut_trigger_type_spinner")
        if self.ios:
            otb_picker = self.pickerwheel()
            self.picker_select(otb_picker, desired_selection, direction)

            self.tap(self.strings.OK)
        elif self.android:
            self.tap(desired_selection)
