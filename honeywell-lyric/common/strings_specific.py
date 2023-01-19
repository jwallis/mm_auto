# -*- coding: utf-8 -*-
# holds string constants of different languages, date formats, etc.
from generic_flow import *

def set_strings_project_specific(language, strings, platform):
    #########################################
    #this project all languages, all platforms:

    # This should be the name you see when you go the the Android app switcher or view the name of the app on the desktop.
    # We'll use this to switch back to the app after (for example) turning on airplane mode
    # This may require multiple values such as ['My Cool App', 'My Cool A...'] because the app switcher will sometimes truncate.
    # Try both horizontal and vertical views of the app switcher

    strings.app_name = "Lyric"

    if (language == 'en_US'):
        en_us_project_specific(strings, platform)
    elif (language == 'hr_HR'):
        hr_hr_project_specific(strings, platform)
    elif (language == 'de_DE'):
        de_de_project_specific(strings, platform)
    elif (language == 'en_GB'):
        en_gb_project_specific(strings, platform)
    elif (language == 'fr_FR'):
        fr_fr_project_specific(strings, platform)
    elif (language == 'it_IT'):
        it_it_project_specific(strings, platform)
    elif (language == 'es_ES'):
        es_es_project_specific(strings, platform)
    elif (language == 'es_MX'):
        es_mx_project_specific(strings, platform)
    elif (language == 'id_ID'):
        id_id_project_specific(strings, platform)
    elif (language == 'el_GR'):
        el_gr_project_specific(strings, platform)
    elif (language == 'ms_MY'):
        ms_my_project_specific(strings, platform)
    elif (language == 'nl_NL'):
        nl_nl_project_specific(strings, platform)
    elif (language == 'ru_RU'):
        ru_ru_project_specific(strings, platform)
    elif (language == 'pt_BR'):
        pt_br_project_specific(strings, platform)
    elif (language == 'th_TH'):
        th_th_project_specific(strings, platform)
    elif (language == 'tr_TR'):
        tr_tr_project_specific(strings, platform)
    elif (language == 'pl_PL'):
        pl_pl_project_specific(strings, platform)
    elif (language == 'ja_JP'):
        ja_jp_project_specific(strings, platform)
    elif (language == 'ko_KR'):
        ko_kr_project_specific(strings, platform)
    else:
        raise RuntimeError("In strings_specific.py: language not supported: %s" % language)


####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################

def en_us_project_specific(strings, platform):
    #########################################
    #this project all platforms:
    strings.app_name                                    = "Lyric"
    strings.Auto                                        = "Auto"             #On Fan Mode settings
    strings.Circulate                                   = "Circulate"        #On Fan Mode settings
    strings.default_email_text                          = "Email Address"
    strings.invalid_login                               = 'Your email address or password is invalid'
    strings.location_settings_location_details          = 'Location Details'
    strings.location_settings_notification_preferences  = 'Notification Preferences'
    strings.location_settings_thermostats               = 'Thermostats'
    strings.location_settings_users                     = 'Users'
    strings.How_Much_Cooler_                            = "How Much Cooler?" # On New Shortcut Screen -> Make it Cooler
    strings.How_Much_Warmer_                            = "How Much Warmer?" # On New Shortcut Screen -> Make it Warmer
    strings.Low                                         = 'Low'
    strings.new_otb_house_empty                         = 'Your house is empty'
    strings.new_otb_press_shortcut                      = 'When I press a shortcut'
    strings.new_otb_someone_home                        = 'Someone is at home'
    strings.Normal                                      = "Normal"
    strings.Off                                         = "Off"
    strings.OK                                          = "OK"
    strings.On                                          = "On"               # On Fan Mode settings
    strings.secondary_card_advanced                     = 'Advanced'
    strings.secondary_card_away_settings                = 'Away Settings'
    strings.secondary_card_auto_changeover              = 'Auto Changeover'
    strings.secondary_card_fan_mode                     = 'Fan Mode'
    strings.secondary_card_hardware                     = 'Hardware'
    strings.secondary_card_home_settings                = 'Home Settings'
    strings.thermostat_settings                         = 'Thermostat Settings'
    strings.SAVE                                        = 'SAVE'             # on geofence resize screen
    
    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        strings.default_password_text                   = ""
        strings.Enable_geo_fence_notifications          = "Enable Geo-fence notifications"
        strings.Email_Address                           = "Email Address" # Forgot Password screen, leftover text on email field
        strings.Geo_fence                               = 'Geo-fence'
        strings.invalid_login                           = 'Unable to login. Email or password incorrect.'
        strings.Loading_                                = 'Loading…'
        strings.More_options                            = 'More options' # the "..." button in the upper right on the Home screen
        strings.new_otb_specific_time                   = 'It is a specific time'
        strings.RETRY_                                  = 'RETRY >'
        strings.Shortcut_was_activated_by_Geofencing_   = "Shortcut was activated by Geofencing." # in the "Lyric" notifications
        strings.Shortcut_was_activated_by               = "Shortcut was activated by"
        strings.triggered                               = 'triggered' # in the "geofence" notifications
        strings.Update                                  = 'Update' # system popup when you update the geofence button
        strings.new_otb_circulate_my_air                = "Circulate My Air"
        strings.new_otb_make_it___cooler                = u'Make it 5\xb0 Cooler'
        strings.new_otb_make_it___warmer                = u'Make it 5\xb0 Warmer'
        strings.new_otb_use_away_settings               = "Use Away Settings"
        strings.new_otb_use_eco_mode                    = "Use Eco Mode"
        strings.new_otb_use_home_settings               = "Use Home Settings"
        strings.New_Shortcut                            = "New Shortcut" # New OTB -> Press "Next"
        strings.Settings                                = 'Settings' # in the "..." menu in the upper right on the Home screen
        strings.with_event_response                     = 'with event response' # in the "geofence" notifications
    elif (platform == 'ios'):
        strings.Allow                                   = 'Allow'
        strings.CANCEL                                  = 'CANCEL' # cancel on the alert popup
        strings.default_password_text                   = "Password"
        strings.Do_not_show_geofence_alerts             = "Do not show geofence alerts" # hidden environment menu
        strings.DETAILS                                 = 'DETAILS' # on geofence notification popup
        strings.Environment                             = 'Environment' # on the "secret login page" this is the text in the tablecell right ABOVE the dropdown with the environment names
        strings.John___doe___com                        = "John@doe.com"  # Forgot Password screen, leftover text on email field
        strings.invalid_login                           = 'Your email address or password is invalid'
        strings.Lyric_                                  = 'Lyric, '
        strings.Name_Your_New_Shortcut                  = 'Name Your New Shortcut' # New OTB -> Press "Next"
        strings.new_otb_circulate_my_air                = "Circulate the air"
        strings.new_otb_make_it___cooler                = u'Make it 5\xb0 cooler'
        strings.new_otb_make_it___warmer                = u'Make it 5\xb0 warmer'
        strings.new_otb_specific_time                   = 'It\'s a specific time'
        strings.new_otb_use_away_settings               = "Use Away settings"
        strings.new_otb_use_eco_mode                    = "Use Eco mode"
        strings.new_otb_use_home_settings               = "Use Home settings"
        strings.Retry                                   = 'Retry'
        strings.Show_geofence_alerts                    = 'Show geofence alerts' # hidden environment menu
        strings.The_response_was                        = 'The response was' # on geofence notification
        strings.There_was_an_error__                    = 'There was an error resetting your password. Please try again later or contact Technical Support.' # on Forgot Password screen when you use an unregistered e-mail
        strings.YES                                     = 'YES' # YES on alert popup
        strings.You_must_enter_a_valid_email_address    = "You must enter a valid email address" #On Forgot Password screen
        strings.Update                                  = 'YES, UPDATE' # system popup when you tap the update geofence button
        strings.via_trigger                             = 'via trigger' # on geofence notification
        strings.we_can_t_determine_your_location__      = "We can't determine your location. Please try again later." # error that randomly shows up on geofence resize screen

    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################


def hr_hr_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################


def de_de_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def fr_fr_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################


def en_gb_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def it_it_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def es_es_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def es_mx_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def el_gr_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def id_id_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def ms_my_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def nl_nl_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def ru_ru_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def pt_br_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def th_th_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def tr_tr_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def pl_pl_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def ja_jp_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")


####################################################################################################################################################################

def ko_kr_project_specific(strings, platform):
    #########################################
    #this project all platforms:


    #########################################
    #this project platform-specific:
    if (platform == 'android'):
        pass
    elif (platform == 'ios'):
        pass
    else:
        raise RuntimeError("In strings_specific.py: platform not supported")

