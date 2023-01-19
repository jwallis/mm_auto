################################################################################
#
# NAME: login03 - log in with blank/invalid parameters
# ID: 43120 43121 43122 43127 43130 43131 43132
# DESCRIPTION: Script checks login form with blank/invalid data
#
################################################################################
from common import *

def run_test(flow, device, data):
    # NOTE!!!:
    # See bug HNYDEV-235
    #   Feature Discrepancy between iOS and Android
    #   where iOS validates your email and password format and will disable the Login button if invalid
    #   whereas Android will enable the Login button if you have ANY text on both email and password inputs

    flow.set_env()

    # Test login form with all blank fields
    # If user/pass fields are empty, the Login button should be disabled

    # TODO: Verify the Android implementation of clear_textfield() under _generic.py
    flow.clear_textfield('login_username_textfield', flow.strings.default_email_text)
    flow.clear_textfield('login_password_textfield', flow.strings.default_password_text)

    # [ TC: 43120 ]
    # Verify that user is unable to tap on 'LOGIN' button when email address and password are not entered
    assert flow.verify_login_button_is_disabled(), "43120: Empty e-mail AND password, the LOGIN button should be disabled (%s)" % flow.platform

    #------[ Testing with partially blank fields ]------
    # If some fields are empty, the Login button should be disabled

    # [ TC: 43121 ] - Test login form with blank password
    error = "ERROR TC 43121: Test login form with blank password (" + (flow.platform) + ")"
    flow.set_text("login_username_textfield", "mm.mats.automation+02@gmail.com")
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)
    assert flow.verify_login_button_is_disabled(), error

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # [ TC: 43122 ] - Test login form with blank username, Login Button should be disabled
    error = "ERROR TC 43122: Test login form with blank username (" + (flow.platform) + ")"
    flow.clear_textfield("login_username_textfield", should_be_leftover=flow.strings.default_email_text)
    flow.set_text("login_password_textfield", "Lyric1234")
    assert flow.verify_login_button_is_disabled(), error

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # [ TC: 43127 ] - Verify that an error message is displayed
    # when tapping on the 'LOGIN' button when using an invalid password
    error = "ERROR TC 43127: Test login with incorrect password (" + (flow.platform) + ")"
    flow.set_text("login_username_textfield", "mm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "5Lyric1234")
    flow.tap("login_login_button")
    assert flow.exists_and_visible(flow.strings.invalid_login, timeout=30), error

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # [ TC: 43130 ] - Verify that an error message is displayed
    # login with incorrect username
    error = "ERROR TC 43130: Test login with incorrect username (" + (flow.platform) + ")"
    flow.set_text("login_username_textfield", "mmm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "Lyric1234")
    flow.tap("login_login_button")
    flow.tap("login_login_button")
    assert flow.exists_and_visible(flow.strings.invalid_login, timeout=30), error

    flow.clear_textfield("login_username_textfield", flow.strings.default_email_text)
    flow.clear_textfield("login_password_textfield", flow.strings.default_password_text)

    # [ TC: 43131 ] - Test login with invalid email and an incorrect password in the correct format
    error = "ERROR TC 43131: Test login with invalid email and an incorrect password in the correct format (" + (flow.platform) + ")"
    flow.set_text("login_username_textfield", "mmm.mats.automation+02@gmail.com")
    flow.set_text("login_password_textfield", "5Lyric1234")
    flow.tap("login_login_button")
    assert flow.exists_and_visible(flow.strings.invalid_login, timeout=30), error

    # [ TC: 43132 ] - Test login with invalid email and an incorrect password in the correct format
    # iOS Only
    if flow.ios:
        error = "ERROR TC 43131: Test login with invalid email and an incorrect password in the correct format (" + (flow.platform) + ")"
        flow.set_text("login_username_textfield", "mmm.mats.automation+02@gmail.com")
        flow.set_text("login_password_textfield", "abcd5678")
        flow.tap("login_login_button")
        assert flow.exists_and_visible(flow.strings.invalid_login, timeout=30), error

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