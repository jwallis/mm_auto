# -*- coding: utf-8 -*-
# holds string constants of different languages, date formats, etc.
from _external import *

def set_strings_generic(language, strings, platform):

    strings.supported_languages = ['en_US', 'de_DE', 'hr_HR', 'en_GB', 'fr_FR', 'it_IT', 'es_ES', 'es_MX', 'id_ID', 'el_GR', 'ms_MY', 'nl_NL', 'ru_RU', 'pt_BR', 'th_TH', 'tr_TR', 'pl_PL', 'ja_JP', 'ko_KR']

    if (language == 'en_US'):
        en_us_generic(strings, platform)
        current_language                        = ['English (United States)', 'English']
    elif (language == 'de_DE'):
        de_de_generic(strings, platform)
        current_language                        = ['Deutsch (Deutschland)', 'Deutsch']
    elif (language == 'hr_HR'):
        hr_hr_generic(strings, platform)
        current_language                        = ['Hrvatski (Hrvatska)', 'Hrvatski']
    elif (language == 'en_GB'):
        en_gb_generic(strings, platform)
        current_language                        = ['English (United Kingdom)']
    elif (language == 'fr_FR'):
        fr_fr_generic(strings, platform)
        current_language                        = ['Français (France)', 'Français']
    elif (language == 'it_IT'):
        it_it_generic(strings, platform)
        current_language                        = ['Italiano (Italia)', 'Italiano']
    elif (language == 'es_ES'):
        es_es_generic(strings, platform)
        current_language                        = ['Español (España)']
    elif (language == 'es_MX'):
        es_mx_generic(strings, platform)
        current_language                        = ['Español (Estados Unidos)', 'Español']
    elif (language == 'id_ID'):
        id_id_generic(strings, platform)
        current_language                        = ['Bahasa Indonesia (Indonesia)', 'Bahasa Indonesia']
    elif (language == 'el_GR'):
        el_gr_generic(strings, platform)
        current_language                        = ["Ελληνικά (Ελλάδα)", "Ελληνικά",u'\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac']
    elif (language == 'ms_MY'):
        ms_my_generic(strings, platform)
        current_language                        = ['Bahasa Melayu (Malaysia)', 'Bahasa Melayu']
    elif (language == 'nl_NL'):
        nl_nl_generic(strings, platform)
        current_language                        = ['Nederlands (Nederland)', 'Nederlands']
    elif (language == 'ru_RU'):
        ru_ru_generic(strings, platform)
        current_language                        = ["Русский (Россия)", 'Русский', u'\u042f\u0437\u044b\u043a'] # russian
    elif (language == 'pt_BR'):
        pt_br_generic(strings, platform)
        current_language                        = ['Português (Brasil)', 'Português']
    elif (language == 'th_TH'):
        th_th_generic(strings, platform)
        current_language                        = ["ไทย (ไทย)", "ไทย", u'\u0e44\u0e17\u0e22']  # thai
    elif (language == 'tr_TR'):
        tr_tr_generic(strings, platform)
        current_language                        = ["Türkçe (Türkiye)", 'Türkçe']  # turkish
    elif (language == 'pl_PL'):
        pl_pl_generic(strings, platform)
        current_language                        = ['Polski (Polska)', 'Polski'] # polish
    elif (language == 'ja_JP'):
        ja_jp_generic(strings, platform)
        current_language                        = ["日本語 (日本)", '日本語'] # japanese
    elif (language == 'ko_KR'):
        ko_kr_generic(strings, platform)
        current_language                        = ["한국어 (대한민국)", '한국어'] # korean
    else:
        raise RuntimeError("In strings_generic.py: language not supported: %s" % language)
    return current_language, language


####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################

def en_us_generic(strings, platform):
    #########################################
    #all projects all platforms:
    strings.Email                               = 'Email'
    strings.OK                                  = 'OK'
    strings.misspelled_wrong                    = 'misspelledd'
    strings.misspelled_corrected                = 'misspelled'
    strings.Wi_Fi                               = ['Wi-Fi', 'Wi‑Fi'] #believe it or not, those dash characters are different



    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Airplane_mode                   = 'Airplane mode'
        strings.Apps                            = ['Apps', 'Applications'] # system settings, Apps
        strings.all_characters                  = u'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-~!@#$%^&*()_+[]=\\{}|;:",./<>?' # missing ' because appium can't handle it.  issues with xpath.  it's fine
        strings.Cancel                          = 'Cancel' #on system settings turn on/off airplane mode
        strings.Clear_all_notifications_        = 'Clear all notifications.' # system notifications
        strings.Clear_cache                     = 'Clear cache' #system settings, Apps
        strings.Clear_data                      = 'Clear data' #system settings, Apps
        strings.Copy_to_clipboard               = 'Copy to clipboard' #invite friends
        strings.Gmail                           = 'Gmail' #popup listview of intents when you try to share something (share sheet)
        strings.Language                        = 'Language' #the "Language" menu choice on system settings page.  We tap this to see the list of system language choices
        strings.Language_and_input              = ['Language and input', 'Language & input'] # system settings main page
        strings.Location                        = 'Location'
        strings.More_networks                   = ['More networks',"More…", "More"] # on system settings main page (instead of More...)
        strings.My_device                       = 'My device' # system settings
        strings.Search                          = ['Search', 'Search, or say Google', 'Search, or say "Ok Google"', 'Search, or say “Ok Google”'] #system search box.  quote chars are different in some of these
        strings.System_settings                 = ["Settings","System settings"] # on system home menu
    elif (platform == 'ios'):
        strings.all_characters                  = u'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-~!@#$%^&*()_+[]{}|;:",./<>?€£¥' # missing ' and \\ because appium does not handle correctly. see
        strings.Cancel                          = 'Cancel' #on system settings, invite friends
        strings.Copy                            = 'Copy' #system clipboard copy
        strings.Copy_to_clipboard               = 'Copy' #invite friends pop up
        strings.Cut                             = 'Cut' #system clipboard copy
        strings.Delete                          = 'Delete' #system delete element (not key or button)
        strings.Delete_draft                    = 'Delete Draft' # after cancel email
        strings.Done                            = 'Done' # completing a web form
        strings.Mail                            = 'Mail'
        strings.Next                            = 'Next' # entering data into a web form
        strings.Next_keyboard_key               = 'Next keyboard' #switch to emoji keyboard or back to regular keyboard
        strings.Paste                           = 'Paste' #system clipboard paste
        strings.Select_All                      = 'Select All' #system clipboard select all
        strings.Settings                        = 'Settings' #Settings app on iOS home screen
        strings.Show_more_items                 = 'Show more items' #system clipboard > (right arrow) that shows when there are too many options to fit onscreen
        strings.Show_previous_items             = 'Show previous items' #system clipboard < (left arrow) that shows when there are too many options to fit onscreen
        strings.space_key                       = 'space' #ios (sim at least) keyboard char for ' '
    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def de_de_generic(strings, platform):
    #########################################
    #all projects all platforms:
    strings.OK                                  = 'OKEE'
    strings.misspelled_wrong                    = 'misspelledd'
    strings.misspelled_corrected                = 'misspelled'
    strings.Wi_Fi                               = 'Wi-Fi'



    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Airplane_mode                   = 'El modo del aeroplano'
        strings.all_characters                  = u'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-~!@#$%^&*()_+[\\{}|;\':",./<>?' # missing ] and = because appium can't handle it.  there may be a bug open
        strings.Cancel                          = 'Cancelo' #on system settings turn on/off airplane mode
        strings.Language                        = 'Sprache' #the "Language" menu choice on system settings page.  We tap this to see the list of system language choices
        strings.Language_and_input              = ['Sprache und Eingabe', 'Sprache & Eingabe'] # system settings main page
        strings.More_networks                   = ['Mehr...'] # on system settings main page (instead of More...)
        strings.My_device                       = u'Mein Ger\xe4t' # system settings
        strings.Search                          = ['digame', 'digame Google', 'digame "Ok Google"'] #system search box
        strings.System_settings                 = ['Systemeinstellungen','Einstellungen'] # on system home menu
    elif (platform == 'ios'):
        #strings.all_characters                  = u'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-~!@#$%^&*()_+[\\{}|;\':",./<>?€£¥' # missing ` and ] and = because appium can't handle it.  there may be a bug open
        strings.all_characters                  = u'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-~!@#$%^&*()_+[\\{}|;\':",./<>?' # missing ` and ] and = because appium can't handle it.  there may be a bug open.  IOS can't handle €£¥ so I took them off.  Maybe this ALL Chars screen should be project-specific
        strings.Copy                            = 'Copy' #system clipboard copy
        strings.Cut                             = 'Cut' #system clipboard copy
        strings.Delete                          = 'Delete' #system delete element (not key or button)
        strings.Paste                           = 'Paste' #system clipboard paste
        strings.Select_All                      = 'Select All' #system clipboard select all
        strings.Show_more_items                 = 'Show more items' #system clipboard > (right arrow) that shows when there are too many options to fit onscreen
        strings.Show_previous_items             = 'Show previous items' #system clipboard < (left arrow) that shows when there are too many options to fit onscreen
    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def hr_hr_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Jezik'
        strings.Language_and_input              = [u'Jezik i ulaz',u'Jezik i unos']
        strings.My_device                       = u'Moj ure\u0111aj'
        strings.System_settings                 = [u'Postavke', 'Postavke sustava']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################



def en_gb_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = 'Language'
        strings.Language_and_input              = ['Language and input', 'Language & input']
        strings.My_device                       = 'My device'
        strings.System_settings                 = ['System settings', 'Settings']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

#############################################


def fr_fr_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Langue'
        strings.Language_and_input              = u'Langue et saisie'
        strings.My_device                       = 'Mon appareil'
        strings.System_settings                 = [u'Param\xe8tres syst\xe8me', u'Param\xe8tres']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def it_it_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Lingua'
        strings.Language_and_input              = ['Lingua e immissione', 'Lingua e inserimento', 'Lingua e input']
        strings.My_device                       = ['Dispositivo personale', 'Dispositivo']
        strings.System_settings                 = [u'Impostazioni sistema', u'Impostazioni']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def es_es_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Idioma'
        strings.Language_and_input              = [u'Idioma y entrada de texto', 'Idioma y entrada', u'Idioma e introducción de texto', 'Idioma e introducción']
        strings.My_device                       = 'Mi dispositivo'
        strings.System_settings                 = [u'Ajustes del sistema', u'Ajustes', u'Configuraci\xf3n del sistema']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def es_mx_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Idioma'
        strings.Language_and_input              = [u'Teclado e idioma', u'Idioma e introducci\xf3n']
        strings.My_device                       = 'Mi dispositivo'
        strings.System_settings                 = [u'Configuraci\xf3n del sistema', u'Configuraci\xf3n', 'Config.']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def id_id_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = 'Bahasa'
        strings.Language_and_input              = ['Bahasa & masukan', 'Bahasa dan masukan']
        strings.My_device                       = 'Perangkat saya'
        strings.System_settings                 = ['Setelan', 'Pengaturan']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def el_gr_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'\u0393\u03bb\u03ce\u03c3\u03c3\u03b1'
        strings.Language_and_input              = [u'\u0393\u03bb\u03ce\u03c3\u03c3\u03b1 \u03ba\u03b1\u03b9 \u03b5\u03b9\u03c3\u03b1\u03b3\u03c9\u03b3\u03ae', u'\u0393\u03bb\u03ce\u03c3\u03c3\u03b1 \u03ba\u03b1\u03b9 \u03b5\u03af\u03c3\u03bf\u03b4\u03bf\u03c2']
        strings.My_device                       = u'\u0397 \u03c3\u03c5\u03c3\u03ba\u03b5\u03c5\u03ae \u03bc\u03bf\u03c5'
        strings.System_settings                 = [u'\u03a1\u03c5\u03b8\u03bc\u03af\u03c3\u03b5\u03b9\u03c2', u'\u03a1\u03c5\u03b8\u03bc\u03af\u03c3\u03b5\u03b9\u03c2 \u03c3\u03c5\u03c3\u03c4\u03ae\u03bc\u03b1\u03c4\u03bf\u03c2']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def ms_my_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = 'Bahasa'
        strings.Language_and_input              = [u'Bahasa & input','Bahasa dan input']
        strings.My_device                       = 'Alatan saya'
        strings.System_settings                 = ['Tetapan', 'Aturan']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def nl_nl_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Taal'
        strings.Language_and_input              = u'Taal en invoer'
        strings.My_device                       = u'Mijn apparaat'
        strings.System_settings                 = [u'Systeeminstellingen', u'Instellingen']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def ru_ru_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'\u042f\u0437\u044b\u043a'
        strings.Language_and_input              = u'\u042f\u0437\u044b\u043a \u0438 \u0432\u0432\u043e\u0434'
        strings.My_device                       = u'\u041c\u043e\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e'
        strings.System_settings                 = [u'\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def pt_br_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Idioma'
        strings.Language_and_input              = [u'Idioma e entrada', 'Idioma e texto', u'Idioma e inser\xe7\xe3o']
        strings.My_device                       = u'Meu dispositivo'
        strings.System_settings                 = [u'Configura\xe7\xf5es do sistema', 'Config.']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def th_th_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'\u0e20\u0e32\u0e29\u0e32'
        strings.Language_and_input              = [u'\u0e20\u0e32\u0e29\u0e32\u0e41\u0e25\u0e30\u0e01\u0e32\u0e23\u0e1b\u0e49\u0e2d\u0e19\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25', u'\u0e20\u0e32\u0e29\u0e32\u200b\u0e41\u0e25\u0e30\u200b\u0e01\u0e32\u0e23\u200b\u0e43\u0e2a\u0e48\u200b\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25']
        strings.My_device                       = u'\u0e2d\u0e38\u0e1b\u0e01\u0e23\u0e13\u0e4c\u0e2a\u0e48\u0e27\u0e19\u0e15\u0e31\u0e27'
        strings.System_settings                 = [u'\u0e01\u0e32\u0e23\u0e15\u0e31\u0e49\u0e07\u0e04\u0e48\u0e32', u'\u0e01\u0e32\u0e23\u200b\u0e15\u0e31\u0e49\u0e07\u200b\u0e04\u0e48\u0e32']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def tr_tr_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'Dil'
        strings.Language_and_input              = u'Dil ve giri\u015f'
        strings.My_device                       = u'Cihaz\u0131m'
        strings.System_settings                 = [u'Sistem ayarlar\u0131', u'Ayarlar']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def pl_pl_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'J\u0119zyk'
        strings.Language_and_input              = [u'J\u0119zyk, klawiatura, g\u0142os', u'J\u0119zyk i wprowadzanie']
        strings.My_device                       = u'Moje urz\u0105dzenie'
        strings.System_settings                 = [u'Ustawienia systemu',u'Ustawienia']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def ja_jp_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = [u'\u8a00\u8a9e', u'\u65e5\u672c\u8a9e']
        strings.Language_and_input              = [u'\u8a00\u8a9e\u3068\u5165\u529b', u'\u8a00\u8a9e\u3068\u6587\u5b57\u5165\u529b']
        strings.My_device                       = u'\u30de\u30a4\u30c7\u30d0\u30a4\u30b9'
        strings.System_settings                 = [u'\u30b7\u30b9\u30c6\u30e0\u8a2d\u5b9a', u'\u8a2d\u5b9a']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

####################################################################################################################################################################

def ko_kr_generic(strings, platform):
    #########################################
    #all projects all platforms:

    #########################################
    #all projects platform-specific:
    if (platform == 'android'):
        strings.Language                        = u'\uc5b8\uc5b4'
        strings.Language_and_input              = [u'\uc5b8\uc5b4 \ubc0f \ud0a4\ubcf4\ub4dc', u'\uc5b8\uc5b4 \ubc0f \uc785\ub825']
        strings.My_device                       = u'\ub0b4 \ub514\ubc14\uc774\uc2a4'
        strings.System_settings                 = [u'\uc2dc\uc2a4\ud15c \uc124\uc815', u'\uc124\uc815', u'\ud658\uacbd\uc124\uc815']

    elif (platform == 'ios'):
        pass

    else:
        raise RuntimeError("In strings_generic.py: platform not supported")

