################################################################################
#
# NAME: secondary_card02 - device preferences - Auto Changeover
# ID: 40331 40333
# DESCRIPTION: Verify that CHAPI reflects 'Auto Changeover' settings changes made in the app
#
################################################################################

from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    #Refactor flow so api is set logged in and set up at beginning, or when logging the user in?
    flow.get_api()

    flow.goto_device_card(data.user02.loc01.dev01)
    flow.goto_secondary_card(data.user02.loc01.dev01)

    # [ TC 40331 ] - Verify that Auto Changeover is present on the Secondary Card screen
    assert (flow.exists_and_visible("secondary_card_auto_changeover_switch", timeout=5)), "FAILED TC 40331 : Auto Changeover was not found on the screen"

    old_setting = flow.get_api().get_autochangeover()
    
    # [ TC 40333 ] - Verify that user can switch toggle Off to On for Auto Changeover mode
    flow.tap("secondary_card_auto_changeover_switch")

    # Refresh to get the new JSON
    new_setting = flow.wait_for_value_update(flow.get_api().get_autochangeover, old_setting, timeout=30)
    assert (new_setting is not old_setting), "FAILED TC 40333 : No change in CHAPI occurred. current setting: %s, old setting: %s.  " % (new_setting, old_setting)
    
    old_setting = new_setting

    flow.tap("secondary_card_auto_changeover_switch")
    new_setting = flow.wait_for_value_update(flow.get_api().get_autochangeover, old_setting, timeout=30)
    assert (new_setting is not old_setting), "FAILED TC 40333 : No change in CHAPI occurred. current setting: %s, old setting: %s.  " % (new_setting, old_setting)

    #TODO: Add more TCs related to Auto Changeover
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