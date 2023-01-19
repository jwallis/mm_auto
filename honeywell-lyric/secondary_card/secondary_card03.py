################################################################################
#
# NAME: secondary_card03 - device preferences - Change brightness
# ID: 40341
# DESCRIPTION: Verify that changing the brightness in the app is reflected in the server
#
################################################################################

from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    #Refactor flow so api is set when logging the user in?
    flow.get_api()

    flow.goto_device_card(data.user02.loc01.dev01)
    flow.goto_secondary_card(data.user02.loc01.dev01)

    current_brightness = flow.get_api().get_brightness()
    flow.set_brightness(current_brightness, 10)
    new_brightness = flow.get_api().get_brightness()
    assert (new_brightness == 10), "Set-up: Tried to set Brightness to max but it never occurred"

    # [ TC 40341 ] - Verify that sleep brightness mode can be modified from the default value
    flow.goto_secondary_card(data.user02.loc01.dev01)
    current_brightness = 10
    flow.set_brightness(current_brightness, 0)
    new_brightness = flow.wait_for_value_update(flow.get_api().get_brightness, current_brightness, timeout=30)
    assert (new_brightness < current_brightness), "Failed TC 40341: Tried to lower the brightness but it never occurred"

    flow.goto_secondary_card(data.user02.loc01.dev01)
    current_brightness = 0
    flow.set_brightness(current_brightness, 4)
    new_brightness = flow.wait_for_value_update(flow.get_api().get_brightness, current_brightness, timeout=30)
    assert (new_brightness > current_brightness), "Failed TC 40341: Tried to increase the brightness but it never occurred"

    flow.goto_secondary_card(data.user02.loc01.dev01)
    current_brightness = 4
    flow.set_brightness(current_brightness, 10)
    new_brightness = flow.wait_for_value_update(flow.get_api().get_brightness, current_brightness, timeout=30)
    assert (new_brightness > current_brightness), "Failed TC 40341: Tried to set Brightness to max but it never occurred"

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