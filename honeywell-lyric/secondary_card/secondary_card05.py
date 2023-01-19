################################################################################
#
# NAME: secondary_card05 - Adjust temperature for Home Settings
# ID: 40256 40258 40260 40261 40263 40264 40265
# DESCRIPTION: Verify that temperature changes CHAPI reflects Home temperature changes made in the app
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
    original_cool = int(original_setpoints[1])
    original_heat = int(original_setpoints[0])

    assert(flow.on_secondary_card_screen()), "We are not on the secondary card screen"
    flow.tap("secondary_card_home_settings_button")

    # [TC 40256 ] - Verify that tapping on the Home Settings option on secondary card takes user to the Home settings screen
    assert(flow.exists_and_visible('home_settings_when_cooling_button', timeout=1)), "Failed TC 40256: Tapping on Home Settings option does not take us to Home Settings screen"

    # [TC 40258 ] - Verify that back button takes user to the Secondary card landing screen
    flow.go_back()
    assert(flow.on_secondary_card_screen()), "Failed TC 40258: Verify that back button takes user to the Secondary card landing screen"

    #[Home Settings]
    #-----------------[ When Cooling ]-----------------
    flow.tap("secondary_card_home_settings_button")
    flow.tap("home_settings_when_cooling_button")

    #Change the Home Setpoint Cooling temperature
    flow.increase_temperature("home")


    #[TC 40261] - Verify that tapping on the done button (or going Back on Android) on the temperature adjust screen
    # takes user to the Home Settings screen
    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    assert(flow.on_home_settings_screen()), "Failed TC 40261: tapping on the done button (or going Back on Android) on the temperature adjust screen takes user to the Home Settings screen"

    flow.go_back()

    # [TC 40260 ] - Verify that user is able to swipe the meter and change the temperature values
    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_cool = int(new_setpoints[1])
    assert (new_cool > original_cool), " Failed TC 40260: Home settings, when cooling. Temperature should have increased, but this was not true: %d > %d" % (new_cool, original_cool)

    original_setpoints = new_setpoints
    original_cool = new_cool

    flow.tap("secondary_card_home_settings_button")

    assert(flow.on_home_settings_screen())

    # Tap on 'When Cooling'
    flow.tap("home_settings_when_cooling_button")

    #Change the Temp
    # Make sure the method swipes a couple of times IF it doesn't change the temperature on the first try
    flow.decrease_temperature("home")

    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    flow.go_back()

    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_cool = int(new_setpoints[1])
    assert (new_cool < original_cool), " Home settings, when cooling. Temperature should have decreased, but this was not true: %d < %d" % (new_cool, original_cool)

    original_setpoints = new_setpoints

    '''----------------[ When Heating ]-----------------'''
    flow.tap("secondary_card_home_settings_button")

    assert(flow.on_home_settings_screen())

    # Tap on 'When Heating'
    flow.tap("home_settings_when_heating_button")

    #Change the Temp
    # Make sure the method swipes a couple of times IF it doesn't change the temperature on the first try
    flow.increase_temperature("home")

    # [TC 40265 ] - Verify that tapping on the done button on the temperature adjust screen takes user to the Home Settings screen
    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    assert(flow.on_home_settings_screen())

    flow.go_back()

    # [ TC 40263 ] - Verify that when user taps on When Heating option takes user to the screen where user can set the temperature
    # [ TC 40264 ] - Verify that user is able to swipe the meter and change the temperature values
    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_heat = int(new_setpoints[0])
    assert (new_heat > original_heat), "Failed TC 40263: Home settings, when heating. Temperature should have increased, but this was not true: %d > %d" % (new_heat, original_heat)

    original_setpoints = new_setpoints
    original_heat = new_heat

    flow.tap("secondary_card_home_settings_button")

    assert(flow.on_home_settings_screen()), "Failed TC 40256: Tapping on Home Settings option does not take us to Home Settings screen"

    # Tap on 'When Heating'
    flow.tap("home_settings_when_heating_button")

    #Change the Temp
    # Make sure the method swipes a couple of times IF it doesn't change the temperature on the first try
    flow.decrease_temperature("home")

    if flow.ios:
        flow.tap("DONE")
    elif flow.android:
        flow.go_back()
    flow.go_back()

    # Check if CHAPI reflects the changes done
    new_setpoints = flow.wait_for_value_update(flow.get_api().get_setpoints, original_setpoints, timeout=30)
    new_heat = int(new_setpoints[0])
    assert (new_heat < original_heat), " Home settings, when heating. Temperature should have decreased, but this was not true: %d < %d" % (new_heat, original_heat)

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