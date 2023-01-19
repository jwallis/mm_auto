################################################################################
#
# NAME: login04 - log in with blank/invalid parameters
# ID: 43123 43124 43125 43136
# DESCRIPTION: Script checks login form with blank/invalid data
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.set_env()

    # TODO: Verify the Android implementation of clear_textfield() under _generic.py
    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    assert (flow.verify_login_button_is_disabled()), "The LOGIN button should be disabled with empty e-mail AND password, but it was enabled"

        #------[ Testing with incorrect formats ]------

    # [TC: 43123 ]
    # Verify that user is unable to tap on 'LOGIN' button when email address is in the wrong format
    error_msg = "The LOGIN button should be disabled with an invalid e-mail format, but it was enabled."
    user_input = "abcde@gmailcom"
    flow.set_text("login_username_textfield", user_input)
    flow.set_text("login_password_textfield", "Lyric1234")
    assert (flow.verify_login_button_is_disabled()), "TC: 43123-1 Failed: Using e-mail \"%s\". %s" % (user_input, error_msg)

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # HNYDEV-235 Defect for Android
    user_input = "abcdegmail.com"
    flow.set_text("login_username_textfield", user_input)
    flow.set_text("login_password_textfield", "Lyric1234")
    assert (flow.verify_login_button_is_disabled()), "TC: 43123-2 Failed: Using e-mail \"%s\". %s" % (user_input, error_msg)

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    user_input = "abcde@.com"
    flow.set_text("login_username_textfield", user_input)
    flow.set_text("login_password_textfield", "Lyric1234")
    assert (flow.verify_login_button_is_disabled()), "TC: 43123-3 Failed: Using e-mail \"%s\". %s" % (user_input, error_msg)

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    user_input = "ab cd@gmail.com"
    flow.set_text("login_username_textfield", user_input)
    flow.set_text("login_password_textfield", "Lyric1234")
    assert (flow.verify_login_button_is_disabled()), "TC: 43123-4 Failed: Using e-mail \"%s\". %s" % (user_input, error_msg)

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    user_input = "abcde@"
    flow.set_text("login_username_textfield", user_input)
    flow.set_text("login_password_textfield", "Lyric1234")
    assert (flow.verify_login_button_is_disabled()), "TC: 43123-5 Failed: Using e-mail \"%s\". %s" % (user_input, error_msg)

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # [TC: 43124 ]
    # Password Format Invalid
    flow.set_text("login_username_textfield", "mm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "12345678")
    assert (flow.verify_login_button_is_disabled()), "TC: 43124-1 Failed: The LOGIN button should be disabled with an invalid Password format, but it was enabled."

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    flow.set_text("login_username_textfield", "mm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "abcd5678")
    assert (flow.verify_login_button_is_disabled()), "TC: 43124-2 Failed: The LOGIN button should be disabled with an invalid Password format, but it was enabled."

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    flow.set_text("login_username_textfield", "mm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "Abcd#6789")
    # 8 If password field is empty, the Login button should be disabled
    assert (flow.verify_login_button_is_disabled()), "TC: 43124-3 Failed: The LOGIN button should be disabled with an invalid Password format, but it was enabled."

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    flow.set_text("login_username_textfield", "mm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "M2abcde")
    assert (flow.verify_login_button_is_disabled()), "TC: 43124-4 Failed: The LOGIN button should be disabled with an invalid Password format, but it was enabled."

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # [ TC: 43125 ]
    # DEFECT: HNYDEV-235 - Honeywell Lyric (Android)
    #   Login button behavior is enabled for ANY email/password, when it should be only for validly formatted email/pwds
    #------[ Testing with CORRECT formats ]------
    flow.set_text("login_username_textfield", data.user02.username)
    flow.set_text("login_password_textfield", data.user02.password)
    assert (flow.find("login_login_button").enabled is True), "TC: 43125 Failed: The LOGIN button should be ENABLED with BOTH valid e-mail and password fields, but it was disabled."

    # [ TC: 43136 ] - Verify that user is successfully signed with valid credentials and displayed
    # a Welcome page after tapping on 'LOGIN'
    # -Precondition: User already set up a thermostat
    flow.tap("login_login_button")
    flow.wait_for_element_to_exist(["Lyric","global_drawer_button", " navigation drawer"], partial=True, timeout=60)
    flow.tap_safe('Allow', timeout=5)
    flow.tap_safe('OK', timeout=2)
    assert(flow.on_home_screen(ohs_timeout=30)), " TC: 43136 Failed: Did not reach the welcome page"

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