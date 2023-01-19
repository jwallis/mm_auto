# This is the main file that each test case will include, sometimes this is called a "require farm"
# This file is very project-specific but should probably be used as a template for each new project setup

################### externals ###################
from generic_flow import *

from lyric_library import *

################### our libs ###################
from api import *
from devices import *
from geofence import *
from login import *
from navigation import *
from one_touch_buttons import *

def get_flow(**kwargs):
    flow=Flow(**kwargs)
    device=flow.device
    data  =flow.data
    return flow, device, data

# list GenericFlow LAST here so that any methods in GenericFlow can be overridded by the methods from THIS project
class Flow(OneTouchButtonsFlow, commonFlow, DeviceFlow, GeofenceFlow, LoginFlow, NavigationFlow, GenericFlow):
    #see GenericFlow for __init__ and others...
    ########################################################################################
    # todo: this whole method needs to be externalized.  this is just a placeholder until we get a testdata repository working
    def setup_data(self):
        self.data = AttrDict()
        if (self.ios):
            self.data.language = 'en_US'
        elif (self.android):
            self.data.language = 'en_US'

        #log into TCC
        #https://ecc.alarmnet.com/TrueHomeStage/
        #https://ecc.alarmnet.com/TrueHomeStage/Admin/User/LogOn
        #  username: mm.mats.automation@gmail.com
        #  password: Lyric1234Lyric1234
        #  answer to all password recovery questions: mutualmobile

        # http://lyric.alarmnet.com/CHAPIQAStage/api
        #   username: AppTeam@MutualMobile.com
        #   password: Password1



        #log into the app:
        self.data.env                   =  AttrDict()
        self.data.env.android           = 'CHAPI QA STAGE'
        self.data.env.ios               = 'Backup (Stage)'

        self.data.api                   = AttrDict()
        self.data.api.language          = 'en-US'
        self.data.api.base_url          = 'http://lyric.alarmnet.com/CHAPIQAStage/api'

        ######################################
        # mm.mats.automation@gmail.com is in an invalid state on TCC.  do not use
        # self.data.user01                = AttrDict()
        # self.data.user01.username       = 'mm.mats.automation@gmail.com'
        # self.data.user01.password       = 'Lyric1234'
        # self.data.user01.first_name     = "Mats01"
        # self.data.user01.last_name      = "Automation01"
        ######################################

        self.data.user02                            = AttrDict()
        self.data.user02.user_id                    = '5750'
        self.data.user02.username                   = 'mm.mats.automation+02@gmail.com'
        self.data.user02.password                   = 'Lyric1234'
        self.data.user02.first_name                 = "Mats02"
        self.data.user02.last_name                  = "Automation02"
        self.data.user02.loc01                      = AttrDict()
        self.data.user02.loc01.id                   = '7991'
        self.data.user02.loc01.name                 = 'location01'
        self.data.user02.loc01.dev01                = AttrDict()
        self.data.user02.loc01.dev01.loc            = self.data.user02.loc01  # convenience pointer back to parent
        self.data.user02.loc01.dev01.id             = 'TCC-29247'
        self.data.user02.loc01.dev01.name           = 'Thermostat_9e6d'
        self.data.user02.loc01.dev01.mac_id         = '00D02D55BCDA'
        self.data.user02.loc01.dev01.home_cool      = '78'  # in device Preferences page.
        self.data.user02.loc01.dev01.home_heat      = '70'
        self.data.user02.loc01.dev01.away_cool      = '95'
        self.data.user02.loc01.dev01.away_heat      = '60'

        self.data.user03                            = AttrDict()
        self.data.user03.user_id                    = '7144'
        self.data.user03.username                   = 'mm.mats.automation+03@gmail.com'
        self.data.user03.password                   = 'Lyric1234'
        self.data.user03.first_name                 = "Mats03"
        self.data.user03.last_name                  = "Automation03"
        self.data.user03.loc01                      = self.data.user02.loc01

        self.data.user04                            = AttrDict()
        self.data.user04.username                   = 'mm.mats.automation+04@gmail.com'
        self.data.user04.password                   = 'Lyric1234'
        self.data.user04.first_name                 = "Mats04"
        self.data.user04.last_name                  = "Automation04"


################################################################################################################################
# development user (probably temporary) - associated with the stat we borrowed from Priya
################################################################################################################################
        self.data.user05                            = AttrDict()
        self.data.user05.user_id                    = '9504'
        self.data.user05.username                   = 'joshua.wallis+111@mutualmobile.com'
        self.data.user05.password                   = 'Lyric1234'
        self.data.user05.first_name                 = "Tester"
        self.data.user05.last_name                  = "Mm"
        self.data.user05.loc01                      = AttrDict()
        self.data.user05.loc01.id                   = '11393'
        self.data.user05.loc01.name                 = 'At MM'
        self.data.user05.loc01.dev01                = AttrDict()
        self.data.user05.loc01.dev01.loc            = self.data.user02.loc01  # convenience pointer back to parent
        self.data.user05.loc01.dev01.id             = 'TCC-29261'
        self.data.user05.loc01.dev01.name           = 'Josh desk'
        self.data.user05.loc01.dev01.mac_id         = '00D02D55BCDA'
        self.data.user05.loc01.dev01.home_cool      = '78'  # in device Preferences page.
        self.data.user05.loc01.dev01.home_heat      = '70'
        self.data.user05.loc01.dev01.away_cool      = '95'
        self.data.user05.loc01.dev01.away_heat      = '60'
################################################################################################################################
################################################################################################################################


        self.data.user98                    = AttrDict()
        self.data.user98.username           = 'sergio.escoto@mutualmobile.com'
        self.data.user98.password           = 'Lyric1234'
        self.data.user98.first_name         = "Sergio"
        self.data.user98.last_name          = "Escoto"

        self.data.user99                    = AttrDict()
        self.data.user99.username           = 'joshua.wallis@mutualmobile.com'
        self.data.user99.password           = 'Lyric1234'
        self.data.user99.first_name         = "Mats01"
        self.data.user99.last_name          = "Automation01"


        # https://play.google.com/store/apps/details?id=com.fakegps.mock or http://10.194.146.250/fakegps.apk
        # https://www.google.com/maps/d/edit?mid=z5e_rKYMKnXE.khDQV8R12Iwk
        # http://www.gps-coordinates.net
        self.data.geo_loc01a                 = AttrDict()
        self.data.geo_loc01a.name            = 'loc01a'     # android
        self.data.geo_loc01a.lat             = 30.2705679   # ios
        self.data.geo_loc01a.long            = -97.7399109  # ios

        self.data.geo_loc01b                 = AttrDict()
        self.data.geo_loc01b.name            = 'loc01b'
        self.data.geo_loc01b.lat             = 30.271899
        self.data.geo_loc01b.long            = -97.744398

        self.data.geo_loc01c                 = AttrDict()
        self.data.geo_loc01c.name            = 'loc01c'
        self.data.geo_loc01c.lat             = 30.269001
        self.data.geo_loc01c.long            = -97.735072

        self.data.geo_loc02a                 = AttrDict()
        self.data.geo_loc02a.name            = 'loc02a'
        self.data.geo_loc02a.lat             = 30.2498
        self.data.geo_loc02a.long            = -97.749599

        self.data.geo_loc02b                 = AttrDict()
        self.data.geo_loc02b.name            = 'loc02b'
        self.data.geo_loc02b.lat             = 30.251005
        self.data.geo_loc02b.long            = -97.754341

        self.data.geo_loc02c                 = AttrDict()
        self.data.geo_loc02c.name            = 'loc02c'
        self.data.geo_loc02c.lat             = 30.248372
        self.data.geo_loc02c.long            = -97.746209

        self.data.geo_loc03a                 = AttrDict()
        self.data.geo_loc03a.name            = 'loc03a'
        self.data.geo_loc03a.lat             = 30.167837
        self.data.geo_loc03a.long            = -97.793748

        self.data.geo_loc03b                 = AttrDict()
        self.data.geo_loc03b.name            = 'loc03b'
        self.data.geo_loc03b.lat             = 30.170805
        self.data.geo_loc03b.long            = -97.797396

        self.data.geo_loc03c                 = AttrDict()
        self.data.geo_loc03c.name            = 'loc03c'
        self.data.geo_loc03c.lat             = 30.167169
        self.data.geo_loc03c.long            = -97.789156

        self.data.geofence01a                = AttrDict()
        self.data.geofence01a.loc            = self.data.geo_loc01a
        self.data.geofence01a.radius         = "small"                  #small, only contains loc01a, loc01b, loc01c

        self.data.geofence01b                = AttrDict()
        self.data.geofence01b.loc            = self.data.geo_loc01a
        self.data.geofence01b.radius         = "medium"                 #medium, contains loc01a, loc01b, loc01c, loc02a, loc02b, loc02c

        self.data.geofence01c                = AttrDict()
        self.data.geofence01c.loc            = self.data.geo_loc01a
        self.data.geofence01c.radius         = "large"                   #large, contains loc01a, loc01b, loc01c, loc02a, loc02b, loc02c, loc03a, loc03b, loc03c

        self.data.geofence02a                = AttrDict()
        self.data.geofence02a.loc            = self.data.geo_loc02a
        self.data.geofence02a.radius         = "small"                  #small, only contains loc02a, loc02b, loc02c

        self.data.geofence02b                = AttrDict()
        self.data.geofence02b.loc            = self.data.geo_loc02a
        self.data.geofence02b.radius         = "large"                 #large, contains loc01a, loc01b, loc01c, loc02a, loc02b, loc02c, loc03a, loc03b, loc03c

        self.data.geofence03a               = AttrDict()
        self.data.geofence03a.loc           = self.data.geo_loc03a
        self.data.geofence03a.radius        = "small"                  #small

        self.data.geofence03b               = AttrDict()
        self.data.geofence03b.loc           = self.data.geo_loc03a
        self.data.geofence03b.radius        = "medium"                 #medium








        #production:
        # http://lyric.alarmnet.com/CHAPI/api
        # self.data.produser01            = AttrDict()
        # self.data.produser01.username   = 'mm.mats.automation@gmail.com'
        # self.data.produser01.password   = 'Lyric1234'
        # self.data.produser01.first_name = "Mats01"
        # self.data.produser01.last_name  = "Automation01"

        self.data.language_list = ['en_US']

        #self.data.orientation = 'PORTRAIT'

    def get_api(self, user=None):
        """
        returns the api
        """
        if (user == None):
            # the UndefinedElement part is used when doing this in ipython
            if (self.current_user == None or type(self.current_user) == mats.appium.ui.elements.UndefinedElement):
                raise RuntimeError("You called get_api() without specifying a user.  This is only allowed if you are currently logged into the app (logging in sets 'current user')")
            user = self.current_user

        # the UndefinedElement part is used when doing this in ipython
        if (not self.api or type(self.api) == mats.appium.ui.elements.UndefinedElement):
            self.api = CHAPI(self.data)
            self.api.login(user)

        return self.api

####################################################################################
# Honeywell-specific stuff below...
    def hw_lyric_setup(self):
        """
        A test should include either BOTH or NEITHER of hw_lyric_setup & hw_lyric_teardown
        """
        self.log.debug('hw_lyric_setup()...')
        #self.device.orientation = self.data.orientation
        self.geofence_notifications_on  = False

        # use these in teardown.  If true, make sure it's set back.
        # these mirror things in teardown.
        self.airplane_mode_has_been_set = False
        self.wifi_mode_has_been_set     = False
        self.location_services_has_been_set = False

        self.api                        = None
        self.current_user               = None

        if self.android:
            #clears out logcat
            self.device.reset_device_log()

            #SE: Fixes issue I had when starting runner. Needed to let app load before using TouchAction
            self.sleep(2)

    def hw_lyric_teardown(self):
        """
        1.takes a screenshot on failure
        2.turns off airplane mode if it was toggled AT ALL during the test
        3.turns on wifi mode if it was toggled AT ALL during the test
        4.self.logout()
        5.self.quit_driver()
        """
        self.log.debug('hw_lyric_teardown()...')

        if self.status == 'fail':
            self.log.fatal('test failed.  logging page source: ')
            self.page_source(full=True, print_to_console=False)
            self.device.screenshot(self.filename[:-3])

            #turn off airplane mode (if we used airplane mode at all in the test, we can't guarantee what state it's currently in without checking)
            try:
                if (self.airplane_mode_has_been_set):
                    self.set_airplane_mode('off')
            except:
                pass

            #turn on wifi (if we used wifi_mode at all in the test, we can't guarantee what state it's currently in without checking)
            try:
                if (self.wifi_mode_has_been_set):
                    self.set_wifi_mode('on')
            except:
                pass

            # turn on location_services - if script ever turned off location services, make sure we set it back on
            try:
                if self.location_services_has_been_set:
                    self.set_location_services("on")
            except:
                pass

            # set lang back to english
            # self.current_language is set in GenericFlow.setup_strings()
            try:
                if (self.current_language_code != 'en_US'):
                    self.set_language('en_US')
            except:
                pass

            self.device.dump_device_log(self.filename)

        if (self.api and not type(self.api) == mats.appium.ui.elements.UndefinedElement):
            self.api.logout()

        self.quit_driver()