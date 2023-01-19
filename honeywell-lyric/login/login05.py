################################################################################
#
# NAME: login05 - Forgot Password screen : behavior of UI Elements
# ID: 43148 43149 43151 43152 43153 43154 43156
# DESCRIPTION: Verify correct behavior of UI elements in Forgot Password screen
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.tap("login_forgot_password_button")

    #[TC: 43148 ] - iOS Only: Tapping on the email address field will bring up the keyboard
    if flow.ios:
        flow.tap("forgot_password_email_textfield")
        assert(flow.keyboard().visible), "FAILED TC 43148:  tapping on the email address field on Forgot my password does not bring up the keyboard"

    #[TC: 43149 ] - Tapping on "Cancel" / Android: [Back] takes the user to the sign-in page
    flow.go_back()
    assert(flow.on_login_screen()), "FAILED TC 43149: tapping back should have taken us back to login screen but DID NOT"

    #[TC: 43151 ] - Verify that tapping on Send without e-mail will display an error message
    # iOS Only? How to verify a toast message in android version
    if flow.ios:
        flow.tap("login_forgot_password_button")
        flow.tap("forgot_password_send_button")
        assert(flow.exists_and_visible(flow.strings.You_must_enter_a_valid_email_address, timeout=30)), "FAILED TC 43151: Tapping on Send without e-mail should display an error message but there was not any"
        flow.go_back()

    #[TC: 43151 ] - Verify that on the Forgot my Password screen, an error message like 'You must enter valid...'
    # will be displayed if user submits the invalid email address formats
    # Eg: abc@gmail,  abc.gmail.com, abc@gmailcom
    flow.tap("login_forgot_password_button")
    error_msg = "FAILED TC 43151: No error message found after inputting the invalid email address"
    if flow.ios:
        input_text = "acb@gmail"
        flow.set_text("forgot_password_email_textfield", input_text)
        flow.tap("forgot_password_send_button")
        assert (flow.exists_and_visible(flow.strings.You_must_enter_a_valid_email_address)), ("%s: %s") % (error_msg, input_text)

        flow.go_back()
        flow.tap("login_forgot_password_button")

        input_text = "abc.gmail.com"
        flow.set_text("forgot_password_email_textfield", input_text)
        flow.tap("forgot_password_send_button")
        assert (flow.exists_and_visible(flow.strings.You_must_enter_a_valid_email_address)), ("%s: %s") % (error_msg, input_text)

        flow.go_back()
        flow.tap("login_forgot_password_button")

        input_text = "acb@gmail"
        flow.set_text("forgot_password_email_textfield", input_text)
        flow.tap("forgot_password_send_button")
        assert (flow.exists_and_visible(flow.strings.You_must_enter_a_valid_email_address)), ("%s: %s") % (error_msg, input_text)

    elif flow.android:
        # As of 4/1/2015, we cannot capture a toast message with Appium
        #Android will display a toast message, unlike ios where it it will display a red error text
        pass
    flow.go_back()

    #[TC: 43152 ] - Verify that An alert like 'error resetting your password.....'
    # will be displayed if user submits an Un-registered email address
    # iOS Only
    flow.tap("login_forgot_password_button")
    flow.set_text("forgot_password_email_textfield", "doe@john.com")

    #keyboard shows for nexus 6 (Lollipop), we must dismiss it
    if (flow.device_model == 'nexus 6'):
        flow.go_back()

    flow.tap("forgot_password_send_button")
    if flow.ios:
        assert(flow.exists_and_visible(flow.strings.There_was_an_error__, timeout=30)), "FAILED TC 43152: No alert appears after submitting an unregistered email address"
    elif flow.android:
        #TODO: Toast message appears here. No way to verify if it appears for now...
        pass

    ## iOS Only
    #[TC: 43153 ] - Verify that the alert will be closed when tapping on 'OKAY' button
    if flow.ios:
        flow.tap("OKAY")
        assert(not flow.exists_and_visible(flow.strings.There_was_an_error__)), "FAILED TC 43153: The alert is not closed when tapping on 'OKAY' button"

    #[TC: 43154 ] - Verify that the data entered into the email address will persist when the alert is closed
    #TODO: For Android: Leave the wait_for_element_to_exist, sometimes the transition animation will make
    # forgot_password email textfield be hidden for half a second or so.
    flow.wait_for_element_to_exist("forgot_password_email_textfield")
    assert(flow.find("forgot_password_email_textfield").text == "doe@john.com"), "FAILED TC 43154: Data entered into the email address does not persist when the alert is closed"

    flow.go_back()

    flow.clear_textfield('login_username_textfield', flow.strings.default_email_text)
    flow.clear_textfield('login_password_textfield', flow.strings.default_password_text)

    #[TC: 43156 ] - Verify that The email address entered in the sign in page will appear on the Forgot Password
    flow.set_text("login_username_textfield", "john+02@doe.com")
    flow.tap("login_forgot_password_button")
    assert(flow.find("forgot_password_email_textfield").text == "john+02@doe.com"), "FAILED TC 43156: Email entered on sign in page does not appear on Forgot Password textfield"
    flow.go_back()

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