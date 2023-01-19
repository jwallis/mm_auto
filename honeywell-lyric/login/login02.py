################################################################################
#
# NAME: login02 - Check login form with blank and invalidly formatted data
# ID: 43113 43114 43115 43117 43119
# DESCRIPTION: Script checks login form with blank/invalid data
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.blocked_on_android("cannot test on Android")

    #[TC: 43113 ] - Verify that tapping on the 'Email Address' will bring up the alphabet keyboard
    # iOS ONLY
    if flow.ios:
        flow.tap("login_username_textfield")
        assert(flow.keyboard().visible), "TC 43113: keyboard SHOULD be visible but is NOT"

    #[TC: 43114 ] - Verify that when tapping on the 'Next' button on the keyboard, the focus goes to the 'Password' field
    #[TC: 43119 ] - Verify that the data entered into the Password field will be masked
    # iOS Only
    if flow.ios:
        flow.set_text("login_username_textfield", "qwerty")
        assert(flow.find("login_username_textfield").value == "qwerty")
        assert(flow.find("Next"))
        flow.tap("Next")
        flow.tap_keys_on_keyboard("asdfgh")
        password01 = flow.find("login_password_textfield").value
        assert(password01 == u"\u2022" * len("asdfgh")), "TC 43114: The password value should be masked with \'*\'s but the actual value we saw was: %s" % password01

    #[TC: 43115 ] - Verify that tapping on the 'Password' will bring up the alphabet keyboard
    # iOS Only
    if flow.ios:
        flow.tap("login_title_image")
        flow.tap("login_password_textfield")
        assert(flow.does_keyboard_exist() != False)

    #[TC: 43117 ] - Verify that tapping on the 'Done' button will close the keyboard
    # NOTE: on TestRail the TC says for Android but this satisfies iOS version of the TC since we cannot test for
    #   existence of the keyboard on android.
    # iOS Only
    if flow.ios:
        flow.tap("Done")
        assert(flow.does_keyboard_exist() == False)

    #[TC: 43119 ] - Verify that the data entered into the Password field will be masked
    if flow.ios:
        flow.tap("login_password_textfield")
        flow.tap_keys_on_keyboard("asdfgh")
        assert(flow.find("login_password_textfield").value != "asdfgh")
    #TODO: TC doable on Android?

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