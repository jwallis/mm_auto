################################################################################
#
# NAME: one_touch_buttons02 - Verify that correct options exist within OTB settings pages
# ID: 40472 40473 40474 40475 40476 40477 40483 40485 40487 40488 40489
# DESCRIPTION: Verify OTB Test Cases 40472 40474 40475 40476 40477 40483 40485 40487 40488 40489
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    #[TC: C40472 ] - Verify that tapping on Choose a Trigger opens the dropdown options
    #[TC: C40473 ] - Verify that user can scroll through all the available shortcut options
    #   iOS Only
    #[TC: C40474 ] - Verify OK button is present bottom of the screen when dropdown options are present so that
    # user can tap on it to choose the focused option
    #   iOS Only
    flow.tap("home_screen_new_otb_button")
w
    assert(flow.on_new_otb_screen()), "Expected to be in the New OTB screen but we are not"

    flow.tap("new_shortcut_trigger_type_spinner")
    if flow.ios:
        assert(flow.exists_and_visible(flow.strings.new_otb_press_shortcut, timeout=3)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_press_shortcut)
        assert (flow.exists_and_visible(flow.strings.OK)), "FAILED TC 40474: OK button was not present when dropdown options are present"

        # Scroll through the spinner to check existence of all options
        flow.device.tap(0.5, 0.8)
        assert(flow.exists_and_visible(flow.strings.new_otb_specific_time, timeout=3)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_specific_time)
        assert (flow.exists_and_visible(flow.strings.OK)), "FAILED TC 40474: OK button was not present when dropdown options are present"

        flow.device.tap(0.5, 0.8)
        assert(flow.exists_and_visible(flow.strings.new_otb_house_empty, timeout=3)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_house_empty)
        assert (flow.exists_and_visible(flow.strings.OK)), "FAILED TC 40474: OK button was not present when dropdown options are present"

        flow.device.tap(0.5, 0.8)
        assert(flow.exists_and_visible(flow.strings.new_otb_someone_home, timeout=3)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_someone_home)
        assert (flow.exists_and_visible(flow.strings.OK)), "FAILED TC 40474: OK button was not present when dropdown options are present"

        # Accept selection
        flow.tap(flow.strings.OK)
    elif flow.android:
        assert(flow.exists_and_visible_on_page(flow.strings.new_otb_press_shortcut)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_press_shortcut)
        assert(flow.exists_and_visible(flow.strings.new_otb_specific_time)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_specific_time)
        assert(flow.exists_and_visible(flow.strings.new_otb_house_empty)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_house_empty)
        assert(flow.exists_and_visible_on_page(flow.strings.new_otb_someone_home)), "FAILED TC 40472: Dropdown option %s was not present" % (flow.strings.new_otb_someone_home)
        flow.device.back()

    #[TC: C40475 ] - Verify that user is able to modify the selection
    # by tapping on the dropdown any time before tapping on the Next button
    if flow.ios:
        # Tap on drop-down
        flow.tap(flow.strings.new_otb_someone_home)

        flow.device.tap(0.5, 0.7)
        assert (flow.exists_and_visible(flow.strings.new_otb_house_empty, timeout=3)), "FAILED TC 40475: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_house_empty)

        flow.tap(flow.strings.OK)
        assert(flow.exists(flow.strings.new_otb_house_empty)), "FAILED TC 40475: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_house_empty)
    elif flow.android:
        current_selection = flow.find("new_shortcut_trigger_type_spinner").statictext().text
        flow.tap("new_shortcut_trigger_type_spinner")

        flow.tap(flow.strings.new_otb_someone_home)
        assert (flow.find("new_shortcut_trigger_type_spinner").statictext().text != current_selection), "FAILED TC 40475:"

    # When I Press a Shortcut

    #[TC: C40476 ] - Verify that when choosed "When I press a shortcut" then user is displayed with correct options
    '''
    "When I press a shortcut" option is displayed with below options:
    - Your Thermostat will: label
    - Use Home Settings
    - Make it x degree cooler
    - Make it x degree warmer
    - User Eco Mode
    - Use Away Settings
    - Circulate the Air
    - Next button
    '''
    if flow.ios:
        #TODO: iOS
        flow.tap(flow.strings.new_otb_house_empty)

        flow.device.tap(0.5, 0.7)
        flow.sleep(1)
        flow.device.tap(0.5, 0.7)
        assert(flow.exists_and_visible(flow.strings.new_otb_press_shortcut, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_press_shortcut)
        flow.tap(flow.strings.OK)

        assert (flow.exists_and_visible(flow.strings.new_otb_use_home_settings, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_use_home_settings)
        assert (flow.exists_and_visible(flow.strings.new_otb_make_it___cooler, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_make_it___cooler)
        assert (flow.exists_and_visible(flow.strings.new_otb_make_it___warmer, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_make_it___warmer)
        assert (flow.exists_and_visible(flow.strings.new_otb_use_eco_mode, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_use_eco_mode)
        assert (flow.exists_and_visible(flow.strings.new_otb_use_away_settings, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_use_away_settings)

        #           TODO:
        #       iOS swiping doesnt work here, so we cannot find this element
        # assert (flow.exists_and_visible_on_page(flow.strings.new_otb_circulate_my_air, timeout=3)), "FAILED TC 40476: Tapped on drop-down, expected %s to be visible but it was not" % (flow.strings.new_otb_circulate_my_air)
    elif flow.android:
        flow.tap("new_shortcut_trigger_type_spinner")
        flow.tap(flow.strings.new_otb_press_shortcut)

        assert(flow.exists_and_visible(flow.strings.new_otb_use_home_settings)), "Error"
        assert(flow.exists_and_visible(flow.strings.new_otb_make_it___cooler)), "Error"
        assert(flow.exists_and_visible(flow.strings.new_otb_make_it___warmer)), "Error"
        assert (flow.exists_and_visible(flow.strings.new_otb_use_eco_mode)), "Error"
        assert (flow.exists_and_visible(flow.strings.new_otb_use_away_settings)), "Error"
        assert (flow.exists_and_visible_on_page(flow.strings.new_otb_circulate_my_air)), "Error"


    #[TC: C40477 ] - Verify when user taps the Cancel button the new shortcut page is dismissed and the home page is displayed
    flow.go_back()
    assert (flow.on_home_screen()), "Failed TC: C40477: Tried to return to the home screen but it never occurred."


    #TODO [TC: C40480 ] - (For a Non-geofence shortcut) Verify that tapping on second option
    # will activate the "Make it 5 degree cooler" radio button
    # flow.tap("home_screen_new_otb_button")
    #
    # flow.new_shortcut_pick_trigger(flow.strings.new_otb_press_shortcut)
    # if flow.ios:
    #     flow.find_all("new_shortcut_trigger_type_label")[1].tap()


    # [TC: C40483 ] - Verify user selects "Make it 5 degree cooler", then click on ">" icon next to
    # "Make it 5 degree cooler" takes user to Cooler Setting page
    flow.tap("home_screen_new_otb_button")

    flow.new_shortcut_pick_trigger(flow.strings.new_otb_press_shortcut)
    flow.tap("new_shortcut_custom_make_it_cooler_button")

    # on iOS: Press twice. Once to select the option, twice to customize the shortcut
    if flow.ios:
        flow.sleep(0.5)
        flow.tap("new_shortcut_custom_make_it_cooler_button")

    assert (flow.on_how_much_cooler_screen()), "FAILED TC 40483 : After tapping the first \'>\' icon, " \
                                               "We are not on the \"How Much Cooler\" Settings screen"

    # otb_actions = flow.find_all("new_shortcut_trigger_type_labels")
    # for otb_cooler in (x for x in otb_actions if x.statictext().text == flow.strings.new_otb_make_it___cooler): break

    setpoints = flow.get_api().get_setpoints()

    # [TC: C40488 ] - The default "When heating" value is the result of home settings heat set point deducting 5

    assert(flow.get_when_heating() == (int(setpoints[0]) - 5)), \
        "Failed TC 40488: The default \"When heating\" value should be home settings heat set point minus 5"

    # [TC: C40489 ] - The default "When cooling" value is the result of home settings cool set point deducting 5

    assert(flow.get_when_cooling() == (int(setpoints[1]) - 5)), \
        "Failed TC 40489: The default \"When cooling\" value should be home settings cool set point minus 5"

    # [TC: C40485 ] - Verify that sliding to an option will update the Heating and Cooling values
    if flow.ios:
        range_picker = flow.find("new_shortcut_custom_temp_range_picker").pickerwheel()

        flow.picker_select(range_picker, u'-10\xb0', direction="up")

        original_heating = flow.get_when_heating()
        original_cooling = flow.get_when_cooling()
        picker_yoffset = range_picker.size["height"] * 0.15
        for i in range(1, 10):
            range_picker.tap_by_location(yoffset=picker_yoffset)
            assert (flow.get_when_heating() == (i + original_heating)), "FAILED TC 40485: %d != %d" % (flow.get_when_heating(), (i + original_heating))
            assert (flow.get_when_cooling() == (i + original_cooling)), "FAILED TC 40485: %d != %d" % (flow.get_when_cooling(), (i + original_cooling))
    elif flow.android:
        flow.tap("new_shortcut_trigger_type_spinner")

        selections = [u'-1\xb0',  u'-2\xb0',  u'-3\xb0',  u'-4\xb0',  u'-5\xb0',  u'-6\xb0',  u'-7\xb0',  u'-8\xb0',  u'-9\xb0',  u'-10\xb0']

        options = flow.statictexts()

        #TODO: refactor, hide low-level details
        # Scroll the spinner selection to the top to find the "-1" and tap it
        flow.driver.scroll(options[0], options[-1])
        options = flow.statictexts()
        flow.tap(options[0].text)

        original_heating = flow.get_when_heating()
        original_cooling = flow.get_when_cooling()
        for i in range(1,11):
            flow.tap("new_shortcut_trigger_type_spinner")
            # print u' '.join(("Tapping on", (selections[i-1]))).encode('utf-8').strip()
            flow.tap(selections[i-1])
            # print str(i) + ": %d vs %d" % (flow.get_when_heating(), (original_heating-i+1))
            # print str(i) + ": %d vs %d" % (flow.get_when_cooling(), (original_cooling-i+1))
            assert (flow.get_when_heating() == (original_heating-i+1)), "FAILED TC 40485: %d != %d" % (flow.get_when_heating(), (original_heating-i+1))
            assert (flow.get_when_cooling() == (original_cooling-i+1)), "FAILED TC 40485: %d != %d" % (flow.get_when_cooling(), (original_cooling-i+1))

    # [TC: C40487] - Verify that Cancel button navigates to the New Shortcut screen without saving the modifications
    #   iOS Only
    if flow.ios:
        flow.tap("CANCEL")

        assert(flow.on_new_otb_screen()), "FAILED TC 40487: Cancel button should navigate us back to the New OTB screen but it did not."
        assert(flow.exists_and_visible(flow.strings.new_otb_make_it___cooler)), \
            "FAILED TC 40487: Cancel button should navigate back to the New Shortcut screen without causing any modifications"


try:
    flow, device, data = get_flow()
    flow.hw_lyric_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    try:
        flow.hw_lyric_teardown()
    except:
        pass