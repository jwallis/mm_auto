################################################################################
#
# NAME: secondary_card04 - device preferences - change volume adjustment
# ID: 40344
# DESCRIPTION: Verify that CHAPI reflects changes to thermostat volume adjustment
#
################################################################################

from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    flow.get_api()

    flow.goto_device_card(data.user02.loc01.dev01)
    flow.goto_secondary_card(data.user02.loc01.dev01)

    flow.set_thermostat_volume(flow.strings.Normal)
    old_volume = 10

    flow.goto_secondary_card(data.user02.loc01.dev01)
    flow.set_thermostat_volume(flow.strings.Off)
    current_vol = flow.wait_for_value_update(flow.get_api().get_thermostat_volume, old_volume, timeout=30)
    assert (current_vol == 0), "Failed TC 40344: expected volume Off"

    # The if statements below are needed to have script consistent with Android since
    # it has to return to the device card to update the changes to CHAPI
    flow.goto_secondary_card(data.user02.loc01.dev01)
    flow.set_thermostat_volume(flow.strings.Low)
    current_vol = flow.wait_for_value_update(flow.get_api().get_thermostat_volume, 0, timeout=30)
    assert (current_vol == 5), "Failed TC 40344: expected volume Low"

    flow.goto_secondary_card(data.user02.loc01.dev01)
    flow.set_thermostat_volume(flow.strings.Normal)
    current_vol = flow.wait_for_value_update(flow.get_api().get_thermostat_volume, 5, timeout=30)
    assert (current_vol == 10), "Failed TC 40344: expected volume of Normal"

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