################################################################################
#
# NAME: one_touch_buttons01 - Check that OTB UI elements exist and exhibit correct behavior
# ID: 40463 40464 40467 40468 40469
# DESCRIPTION: Verify existence of UI elements for OTBs & their correct behavior
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    #[TC: C40463 ]: Verify that there is an option on the Home screen to create shortcuts
    error = "TC: C40463 Failed: Verify that there is an option on the Home screen to create shortcuts"
    assert (flow.exists_and_visible("home_screen_new_otb_button")), error

    # [TC: C40469 (part 1) ]: Verify that Tapping on Cancel button will not create any shortcut
    # SAVE a list of our shortcuts, because we will test this case after TC 40468
    shortcuts = flow.get_all_shortcuts()

    #[TC: C40464 ]: Verify that tapping on the "+" button takes user to the New shortcut screen
    error = "TC: C40464 Failed: Verify that tapping on the \"+\" button takes user to the New shortcut screen"
    flow.tap("home_screen_new_otb_button")
    assert (flow.on_new_otb_screen()), error

    #[TC: C40467 ]: Verify that Next button is disabled until an option from the dropdown is selected
    #   iOS Only
    error = "TC: C40467 Failed: Verify that Next button is disabled until an option from the dropdown is selected"
    if flow.ios:
        assert(flow.button("new_shortcut_next_button").enabled == False), error

    #[TC: C40468 ]: Verify that Cancel button takes user to the Home screen
    error = "TC: C40468 Failed: Verify that Cancel button takes user to the Home screen"
    if flow.ios:
        #TODO: iOS accIDs
        flow.tap("CANCEL")
    elif flow.android:
        flow.device.back()
    assert(flow.on_home_screen(ohs_timeout=30)), error

    # [TC: C40469 (continued) ] : Verify that Tapping on Cancel button will not create any shortcut
    new_shortcuts = flow.get_all_shortcuts()
    # IF we find a shortcut that was not in our original set of shortcuts, something went wrong
    for shortcut in new_shortcuts:
        assert (shortcut in shortcuts), "Failed TC C40469: New shortcut \'%s\' found after cancelling from OTB screen" % (shortcut)


    # #[TC: OTB-10]: Verify that closing the app and reopen on the New shortcut screen will display the same screen with user selected options
    # if flow.ios:
    #     pass
    # elif flow.android:
    #     pass

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