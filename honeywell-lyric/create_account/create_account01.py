################################################################################
#
# NAME: create_account01 -
# ID: 43728
# DESCRIPTION: Verify
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.blocked("Refactor in progress. (\"Create Account\" Flow has changed)")

    #[TC: 43728 ] - Verify that Create Account option is present on
    # the Login page and is as per VD
    #TODO: iOS accIDS
    error = "TC: 43728: Create Account option NOT visible"
    assert(flow.exists("login_create_account_button")), error

    # TODO: Does not take to EULA anymore
    #[TC: 43729 ] - Verify that tapping on Create Account option
    # navigates to create account screen
    error = "TC: 43729: Tap on Create Account option does not navigate to Create Account Page"
    flow.tap("login_create_account_button")
    assert (flow.on_create_account_screen()), error

    #[TC: create_account-08 ] - Verify that Create Account screen
    # displays Cancel & Accept buttons at the bottom of the page
    #TODO: iOS accIDS
    error = "TC: create-account-08: Create Account screen does not contain a CANCEL or an ACCEPT button"
    if flow.ios:
        assert (flow.exists_and_visible("create_account_cancel_button")), error
        assert (flow.exists_and_visible("create_account_next_button")), error
    elif flow.android:
        assert (flow.exists_and_visible("CANCEL")), error
        assert (flow.exists_and_visible("NEXT")), error

    #[TC: create_account-10 ] - Verify that tapping on the Cancel button user
    # is navigated  back to the Login page
    #TODO: iOS accIDs
    error = "TC: create-account-10: Tapping on CANCEL does not take you to the login page"
    flow.tap("CANCEL")
    assert (flow.on_login_screen()), error

    #TODO
    #[TC: create_account-11 ] - Verify that tapping on the Accept button without
    # network displays the network error message
    error = "TC: create-account-11: Tapping on ACCEPT without network DOES NOT display a network error message"
    if flow.ios:
        pass
    elif flow.android:
        pass

    # # TODO: INVALID
    # #[TC: create_account-12 ] - Verify that tapping on the Accept button
    # # will take user to the Create Your Lyric Account screen
    # error = "TC: create-account-12: Tapping on ACCEPT does not take user to create your lyric account screen"
    # if flow.ios:
    #     flow.tap("ACCEPT")
    #     assert(flow.on_create_account_screen()), error
    # elif flow.android:
    #     flow.tap("create_account_accept_button")
    #     assert (flow.on_create_account_screen()), error

    ####
    # [ Create Your Account screen]
    ####

    # Depends on previous test case
    # #[TC: create_account-16 ] - Verify that tapping on the Cancel button takes user to the Login screen
    # #TODO: iOS accIDS
    # error = "TC: create-account-16: Tapping on CANCEL/pressing back Does not take user to the login screen"
    # if flow.ios:
    #     flow.tap("CANCEL")
    #     assert(flow.on_login_screen()), error
    # elif flow.android:
    #     # There is no "Cancel" button on Android version, just OS "Go back"
    #     flow.device.back()
    #     assert (flow.on_login_screen()), error

    #[TC: create_account-18 ] - Verify that tapping on any field on the Create your account screen brings up the keypad
    # iOS Only
    #TODO: Failures after password tapping
    error = "TC: create-account-18: Tapping on any field does not bring up the keyboard"
    if flow.ios:
        flow.tap("First Name")
        assert(flow.is_keyboard_visible() != False), error
        flow.device.hide_keyboard()

        flow.tap("Last Name")
        assert(flow.is_keyboard_visible() != False), error
        flow.device.hide_keyboard()

        flow.tap("Password")
        assert(flow.is_keyboard_visible() != False), error

        flow.tap("Verify Password")
        assert(flow.is_keyboard_visible() != False), error

    #[TC: create_account-19 ] - Verify that keypad has Next button and
    # on tapping it will take focus to the next field in the flow
    # iOS Only
    #TODO: How to detect which element is in focus
    error = "TC: create-account-19: Keyboard does not show a Next button and Next does not take focus to the next field"
    if flow.ios:
        assert (flow.exists_and_visible("Next")), error
        flow.tap("Next")

    #[TC: create_account-20] - Verify that Keypad displays Done button
    # when the focus is on the last field in the flow
    # iOS Only
    error = "TC: create-account-20: Keypad Does not display Done button on last field in the flow"
    if flow.ios:
        flow.exists_and_visible_on_page("Verify Password").tap()
        assert(flow.exists_and_visible("Done")), error

    #[TC: create_account-21] - Verify that tapping on the Done button closes the keypad
    # iOS Only
    error = "TC: create-account-21: Tapping on the Done button does not close the keypad"
    if flow.ios:
        flow.tap("Done")
        assert(flow.is_keyboard_visible() == False), error

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