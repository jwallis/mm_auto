################################################################################
#
# NAME: secondary_card06 - Adjust temperature for Away Settings
# ID: 40286 40290 40294
# DESCRIPTION: Verify that temperature changes CHAPI reflects Away temperature changes made in the app
#
################################################################################

from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    flow.get_api()

    # Set temperature settings to a known state
    flow.get_api().set_default_setpoints()

    flow.goto_device_card(data.user02.loc01.dev01)
    flow.goto_secondary_card(data.user02.loc01.dev01)

    original_setpoints = flow.get_api().get_setpoints()
    original_cool = int(original_setpoints[3])
    original_heat = int(original_setpoints[2])

    assert(flow.on_secondary_card_screen())

    #[TC 40286 ] - Verify that there is an option of Away settings on the Secondary card landing screen
    assert (flow.exists_and_visible("secondary_card_away_settings_button")), "Failed TC 40286: There is NO Away settings option on the Secondary card landing screen"

    flow.tap("secondary_card_away_settings_button")

    #[TC 40290 ] - Verify that tapping on the Away Settings option user is taken to the Aways settings landing screen
    assert(flow.on_away_settings_screen()), "Failed TC 40290: Tapping on the Away Settings option DOES NOT take us to Away Settings page"


    #[TC 40294] - Verify that tapping on the Manual radio button activates the manual option
    # and disables the Automatic option
    # For some reason, iOS does not like .checked() on these radio elements
    #   WebDriverError "The requested resource could not be found"
    flow.tap("away_settings_automatic_radio")

    if flow.android:
        assert(flow.find("away_settings_manual_radio").checked() == False), "Failed TC 40294: Manual Radio button was not checked after tapping"
        assert(flow.find("away_settings_automatic_radio").checked()), "Failed TC 40294: Automatic Radio button was not disabled after tapping Manual radio button"
    elif flow.ios:
        assert(flow.find("away_settings_manual_radio").selected == False), "Failed TC 40294: Manual Radio button was not checked after tapping"
        assert(flow.find("away_settings_automatic_radio").selected), "Failed TC 40294: Automatic Radio button was not disabled after tapping Manual radio button"

    flow.tap("away_settings_manual_radio")

    if flow.android:
        assert(flow.find("away_settings_manual_radio").checked()), "Failed TC 40294: Manual Radio button was not checked after tapping"
        assert(flow.find("away_settings_automatic_radio").checked() == False), "Failed TC 40294: Automatic Radio button was not disabled after tapping Manual radio button"
    elif flow.ios:
        assert(flow.find("away_settings_manual_radio").selected), "Failed TC 40294: Manual Radio button was not checked after tapping"
        assert(flow.find("away_settings_automatic_radio").selected == False), "Failed TC 40294: Automatic Radio button was not disabled after tapping Manual radio button"
    #   Away Settings
    #----------------[ When Cooling ]-----------------
    # Tap on 'When Cooling'
    flow.tap("away_settings_when_cooling_button")

    #Change the Temp

    # Make sure the method swipes a couple of times IF it doesn't change the temperature on the first try
    flow.increase_temperature("away")

    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    flow.go_back()

    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_cool = int(new_setpoints[3])
    assert (new_cool > original_cool), "Away, When Cooling: Temperature should have increased. %d > %d" % (new_cool, original_cool)

    original_setpoints = new_setpoints
    original_cool = new_cool

    flow.tap("secondary_card_away_settings_button")

    assert(flow.on_away_settings_screen())

    # Tap on 'When Cooling'
    flow.tap("away_settings_when_cooling_button")

    #Decrease the Temp
    flow.decrease_temperature("away")

    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    flow.go_back()

    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_cool = int(new_setpoints[3])
    assert (new_cool < original_cool), "Away, When Cooling: Temperature should have decreased. %d < %d" % (new_cool, original_cool)

    original_setpoints = new_setpoints

    #----------------[ When Heating ]-----------------
    flow.tap("secondary_card_away_settings_button")

    assert(flow.on_away_settings_screen())

    # Tap on 'When Heating'
    flow.tap("away_settings_when_heating_button")

    #Change the Temp
    # Make sure the method swipes a couple of times IF it doesn't change the temperature on the first try
    flow.increase_temperature("away")

    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    flow.go_back()

    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_heat = int(new_setpoints[2])
    assert (new_heat > original_heat), "Away - When Heating: Temperature should have increased. %d > %d" % (new_heat, original_heat)

    original_setpoints = new_setpoints
    original_heat = new_heat

    flow.tap("secondary_card_away_settings_button")

    assert(flow.on_away_settings_screen())

    # Tap on 'When Heating'
    flow.tap("away_settings_when_heating_button")

    # Make sure the method swipes a couple of times IF it doesn't change the temperature on the first try
    flow.decrease_temperature("away")

    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    flow.go_back()

    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_heat = int(new_setpoints[2])
    assert (new_heat < original_heat), "Away - When Heating: Temperature should have decreased %d > %d" % (new_heat, original_heat)

try:
    flow, device, data=get_flow()
    flow.hw_lyric_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    # make sure everything's in a try block so the original exception will not be hidden by any exceptions in this section...
    try:
        flow.hw_lyric_teardown()
    except:
        pass