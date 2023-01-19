################################################################################
#
# NAME: secondary_card01 - device preferences - change Fan Mode
# ID: 40244 40248 40314 40319
# DESCRIPTION: Verify that CHAPI reflects fan mode setting changes made in the app
#
################################################################################

from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    #Refactor flow so api is set logged in and set up at beginning, or when logging the user in?
    flow.get_api()

    flow.goto_device_card(data.user02.loc01.dev01)
    flow.goto_secondary_card(data.user02.loc01.dev01)

    # [TC 40244 ] - Verify that tapping settings icon from device card takes you to secondary card screen
    assert (flow.on_secondary_card_screen()), "FAILED TC 40244 : Tapping on settings icon from device card DID NOT take us to the secondary card screen"

    # [TC 40314 ] - Verify that Fan Mode option exists
    if flow.ios:
        assert (flow.exists("secondary_card_fan_mode_button")), "FAILED TC 40314 : Fan Mode option was not present on the secondary card screen"
    elif flow.android:
        assert (flow.exists("secondary_card_fan_mode_spinner")), "FAILED TC 40314 : Fan Mode option was not present on the secondary card screen"

    old_value = flow.get_api().get_fan_mode()

    # [TC 40319 ] - Verify that User is able to tap and select all the Fan Mode options
    flow.set_fan_mode(flow.strings.Auto)
    new_fan_mode = flow.wait_for_value_update(flow.get_api().get_fan_mode, old_value, timeout=30)
    assert (new_fan_mode == flow.strings.Auto), "FAILED TC 40319: Fan Mode expected in \"AUTO\" mode but it was never set"

    old_value = flow.strings.Auto

    flow.set_fan_mode(flow.strings.Circulate)
    new_fan_mode = flow.wait_for_value_update(flow.get_api().get_fan_mode, old_value, timeout=30)
    assert (new_fan_mode == flow.strings.Circulate), "FAILED TC 40319: Fan Mode expected in \"Circulate\" mode but it was never set"

    old_value = flow.strings.Circulate

    flow.set_fan_mode(flow.strings.On)
    new_fan_mode = flow.wait_for_value_update(flow.get_api().get_fan_mode, old_value, timeout=30)
    assert (new_fan_mode == flow.strings.On), "FAILED TC 40319: Fan Mode expected in \"On\" mode but it was never set"

    # [TC 40248 ]
    flow.go_back()
    assert (flow.on_device_card_screen()), "FAILED TC 40248 : Tapping back should take us to primary/device card screen but it did not"

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