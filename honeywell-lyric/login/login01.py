################################################################################
#
# NAME: login01 - Look & Feel, Basic functionality
# ID: 43096 43097 43098 43099 43100 43101 43102 43104 43105 43106 43107 43108 43109
# DESCRIPTION: Verify existence of elements: Email Address, Password, LOGIN button, that LOGIN is disabled, FORGOT PASSWORD, CREATE ACCOUNT, VIEW DEMO
#
################################################################################
from common import *

def run_test(flow, device, data):

    #[TC: 43096 ] - Verify Email Address field exists
    assert (flow.exists_and_visible("login_username_textfield", timeout=10)), "FAILED TEST CASE: 43096 %s" % flow.platform

    #[TC: 43097 ] - Verify Password field exists
    assert (flow.exists_and_visible("login_password_textfield")), "FAILED TEST CASE: 43097 %s" % flow.platform

    #[TC: 43098 ] - Verify LOGIN button exists
    assert (flow.exists_and_visible("login_login_button")), "FAILED TEST CASE: 43098 %s" % flow.platform

    #[TC: 43099 ] - Verify LOGIN button is disabled
    assert (flow.button("login_login_button").enabled is False), "FAILED TEST CASE: 43099"

    #[TC: 43100 ] - Verify FORGOT PASSWORD exists
    assert (flow.exists_and_visible("login_forgot_password_button")), "FAILED TEST CASE: 43100 %s" % flow.platform

    #[TC: 43101 ] - Verify CREATE ACCOUNT exists
    assert (flow.exists_and_visible("login_create_account_button")), "FAILED TEST CASE: 43101 %s" % flow.platform

    #[TC: 43102 ] - Verify VIEW DEMO exists
    assert (flow.exists_and_visible("login_view_demo_button")), "FAILED TEST CASE: 43102 %s" % flow.platform

    #[TC: 43104 ] - Verify that tap and hold for x seconds on the Lyric logo takes the user to the Special Settings' page
    flow._goto_env_screen()
    if flow.ios:
        assert (flow.exists_and_visible("Special Settings")), "FAILED TEST CASE: 43104 %s" % flow.platform
    elif flow.android:
        assert (flow.exists_and_visible("Web Server Url")), "FAILED TEST CASE: 43104 %s" % flow.platform

    #[TC: 43105 ] - Verify that tapping on 'DONE' button takes the user back to the sign in page
    flow.go_back()
    assert (flow.on_login_screen()), "FAILED TEST CASE: 43105 %s" % flow.platform

    #[TC: 43106 ] - Verify that tapping on the 'FORGOT PASSWORD>' takes to the 'Forgot My Password' page
    flow.tap("login_forgot_password_button")
    assert(flow.on_forgot_password_screen()), "FAILED TEST CASE: 43106 %s" % flow.platform

    #[TC: 43107 ] - Verify that tapping on 'CANCEL' takes the user back to the sign in page
    flow.go_back()
    assert (flow.on_login_screen()), "FAILED TEST CASE: 43107 %s" % flow.platform

    #[TC: 43108 ] - Verify that tapping on 'CREATE ACCOUNT>' takes to the 'Create Your Lyric Account" page ( per New Design)
    flow.tap("login_create_account_button")
    assert (flow.on_create_account_screen()), "FAILED TEST CASE: 43108"

    #[TC: 43109 ] - Verify that tapping on 'CANCEL' takes the user back to the sign in page
    # Go back twice: Once to hide the keyboard, and again to actually go back
    if flow.android:
        #Hide the keyboard
        flow.go_back()
    flow.go_back()
    assert (flow.on_login_screen()), "FAILED TEST CASE: 43109 %s" % flow.platform

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