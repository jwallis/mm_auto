# -*- coding: utf-8 -*-

import json, requests
from generic_flow import *

class CHAPI(object):
    """
    Interacts with Honeywell's CHAPI (Connected Home API)
    To play with this in ipython, do your normal
        from ios_ipython_honeywell_lyric import *; flow, device, data=get_flow();

    then
        api = CHAPI(flow.data)
        api.login(data.user02)

        # to play with response as string:
        api.get_eula()                  # returns a Response object
        api.get_eula().text             # returns a text string
        print api.get_eula().text       # prints the text nicely
        print api.get_locs().text
        print api.get_loc(self.data.user02.loc01.id).text
        ...

        # to play with response as a dict:
        xml = json.loads(api.get_locs().text)      # sets xml to an array of dictionaries.  not get_loc(some_loc) returns just a single dict
        print xml                                  # don't do this.  just put the variable on a line by itself and hit enter:
        xml                                        # prints nicely
        xml[0]
        xml[0]['devices'][0]['settings']
        ...
    """
#------------------------------------------------------------------------------
#       initialization-related methods
    def __init__(self, data):
        self.data = data
        self.loc_id = None
        self.dev_id = None
        self.filename = os.path.basename(inspect.stack()[2][1])
        self.log = logging.getLogger("mats.test.%s.%s" % (self.__class__.__name__, self.filename))

    def login(self, user):
        """
        creates the CHAPI session
        """
        self.log.debug("creating API session for: %s" % user.username)
        self.base_url=self.data.api.base_url
        self.headers=None

        #create the session
        self.post_session(user)
        self.set_defaults(user=user)

    def logout(self):
        """
        Deletes the CHAPI session.  Not necessary to call, but a good idea
        """
        try:
            #delete session here: TBD
            pass
        except:
            pass

#------------------------------------------------------
#       business methods for use by tests, etc.
    def get_heat_cool(self, loc_id=None, dev_id=None):
        """
        returns "heat" or "cool"
        """
        loc_id, dev_id = self.get_defaults(loc_id, dev_id)

        resp = self.get_dev(loc_id, dev_id)
        resp = json.loads(resp.text)

        mode = resp['thermostat']['changeableValues']['mode'].lower()
        self.log.debug("get_heat_cool() returning: %s" % mode)
        return mode

    def set_heat_cool(self, heat_cool, loc_id=None, dev_id=None):
        """
        sets stat to heat, cool, or off
        This is really slow to appear on the app!
        """
        loc_id, dev_id = self.get_defaults(loc_id, dev_id)

        self.post_heat_cool(loc_id, dev_id, heat_cool)
        return True

    def verify_heat_cool(self, mode, loc_id=None, dev_id=None, timeout=140):
        """
        uses get_heat_cool() in a loop, returns True/False
        """
        start_time = time.time()

        while True:
            if (self.get_heat_cool(loc_id, dev_id) == mode):
                return True

            if (time.time() - start_time > timeout):
                return False

            self.sleep(1)

    def get_current_setpoint(self, loc_id=None, dev_id=None):
        """
        returns current set point as a 2-character string
        """
        loc_id, dev_id = self.get_defaults(loc_id, dev_id)

        resp = self.get_dev(loc_id, dev_id)
        resp = json.loads(resp.text)

        #get heat or cool mode
        mode = resp['thermostat']['changeableValues']['mode'].lower()

        #get set point based on what mode we're in.  It will look like "99.0"
        setpoint = resp['thermostat']['changeableValues'][mode + 'Setpoint']

        self.log.debug("get_current_setpoint() returning: %s" % setpoint)
        #return it as a string representation of an int
        return str(int(setpoint))

    def set_setpoints(self, home_heat, home_cool, away_heat, away_cool, loc_id=None, dev_id=None):
        """
        sets setpoints
        """
        loc_id, dev_id = self.get_defaults(loc_id, dev_id)

        self.put_home_setpoints(loc_id, dev_id, home_heat, home_cool)
        self.put_away_setpoints(loc_id, dev_id, away_heat, away_cool)

        return True


    def set_default_setpoints(self):
        return self.set_setpoints(self.dev.home_heat, self.dev.home_cool, self.dev.away_heat, self.dev.away_cool)

    def get_setpoints(self, loc_id=None, dev_id=None):
        """
        returns all 4 setpoints as a 2-character strings as tuple:
        (home_heat, home_cool, away_heat, away_cool)
        """
        loc_id, dev_id = self.get_defaults(loc_id, dev_id)

        resp = self.get_dev(loc_id, dev_id)
        resp = json.loads(resp.text)

        #(home_heat, home_cool, away_heat, away_cool)
        setpoints=(str(int(resp['settings']['homeSetPoints']['homeHeatSP'])),
                   str(int(resp['settings']['homeSetPoints']['homeCoolSP'])),
                   str(int(resp['settings']['awaySetPoints']['awayHeatSP'])),
                   str(int(resp['settings']['awaySetPoints']['awayCoolSP'])))

        self.log.debug("get_setpoints() returning (home_heat, home_cool, away_heat, away_cool): %s" % str(setpoints))
        #return it as a string representation of an int
        return setpoints

    def get_device_card_setpoints(self, loc_id=None, dev_id=None):
        """
        returns setpoints reflected from user changes to the dial on the Device Card screen
        """
        loc_id, dev_id = self.get_defaults(loc_id, dev_id)

        resp = self.get_dev(loc_id, dev_id)
        resp = json.loads(resp.text)

        device_card_setpoints = (str(int(resp['thermostat']['changeableValues']['heatSetpoint'])),
                                 str(int(resp['thermostat']['changeableValues']['coolSetpoint'])))

        return device_card_setpoints

    def get_fan_mode(self, user_data=None):
        if(user_data==None):
            user_data = self.user

        device      = user_data.loc01.dev01
        device_id   = device.id
        location_id = user_data.loc01.id

        dev_data = self.get_dev(location_id, device_id).text
        dev_json = json.loads(dev_data)
        return dev_json["settings"]["fan"]["changeableValues"]["mode"]

    def get_autochangeover(self, user_data=None):
        if(user_data==None):
            user_data = self.user

        device      = user_data.loc01.dev01
        device_id   = device.id
        location_id = user_data.loc01.id

        dev_data = self.get_dev(location_id, device_id).text
        dev_json = json.loads(dev_data)
        return dev_json["settings"]["specialMode"]["autoChangeoverActive"]

    # Returns a value from 0 to 10
    #       10 is the max (which is equivalent to 50% brightness setting)
    def get_brightness(self, user_data=None):
        if(user_data==None):
            user_data = self.user

        device      = user_data.loc01.dev01
        device_id   = device.id
        location_id = user_data.loc01.id

        dev_data = self.get_dev(location_id, device_id).text
        dev_json = json.loads(dev_data)
        return (dev_json["settings"]["hardwareSettings"]["brightness"])

    def get_thermostat_volume(self, user_data=None):
        if(user_data==None):
            user_data = self.user

        device      = user_data.loc01.dev01
        device_id   = device.id
        location_id = user_data.loc01.id

        dev_data = self.get_dev(location_id, device_id).text
        dev_json = json.loads(dev_data)
        return dev_json["settings"]["hardwareSettings"]["volume"]

    #TODO: Not yet implemented in CHAPI?
    #  Or depends on thermostat?
    #       So far:
    #       ["settings"]["ventilationModeSettings"]: {}},
    def get_ventilation(self, user_data=None):
        if(user_data==None):
            user_data = self.user

        device      = user_data.loc01.dev01
        device_id   = device.id
        location_id = user_data.loc01.id

        dev_data = self.get_dev(location_id, device_id).text
        dev_json = json.loads(dev_data)
        return "get_ventilation() not implemented"

#------------------------------------------------------------------------
#       Helper methods

    def set_defaults(self, user=None, loc=None, dev=None):
        """
        if we get a user, get the first loc/dev from the user
        else, use the loc and/or dev info
        """

        if (user):
            self.user = user

            if (user.has_key('loc01')):
                self.loc_id = user.loc01.id
                self.loc    = user.loc01

                if (user.loc01.has_key('dev01')):
                    self.dev_id = user.loc01.dev01.id
                    self.dev    = user.loc01.dev01
        else:
            if (loc):
                self.loc_id = loc.id
                self.loc    = loc
            if (dev):
                self.dev_id = dev.id
                self.dev    = dev

    def get_defaults(self, loc=None, dev=None):

        if (not loc):
            loc = self.loc_id
        if (not dev):
            dev = self.dev_id

        return loc,dev

    def get_user_info(self, user):
        """
        This is for YOU THE TESTER to learn about a user you have while you're setting up your data.
        This is not intended to be used by any tests.  Pass in the user (should have a username and password)
        and this will print the API's info about that user and their location and devices.

        Note: you can look in TCC and try to figure out the userID and locationID and stuff like that
        but it is NOT THE SAME as the IDs that the API wants.  Why?  I guess CHAPI has its own IDs that then map to
        TCC's IDs.  You will need to use this method to find the IDs of your user, location and devices
        """
        print "\nHere's the info for: %s" % user.username
        print "This should print your location info as well"
        print "I will pretty print, then dump everything...\n"

        self.base_url = self.data.api.base_url
        self.headers = None

        r1 = self.post_session(user)
        dump = "user & locations:\n" + r1.content + "\n"

        r1 = json.loads(r1.content)
        print "user:"
        print r1['user']['username']
        print r1['userID']
        print r1['user']['firstname']
        print r1['user']['lastname']
        print

        for loc in r1['user']['locationRoleMapping']:
            print "location:"
            print loc['locationName']
            print loc['locationID']
            print

            l = self.get_loc(loc['locationID'])

            dump += "========================================================================================\ndevice:" + l.content

            l = json.loads(l.content)

            for dev in l['devices']:
                print "device:"
                print dev['name']
                print dev['deviceID']
                print dev['macID']
                print



        print "\n" + dump


    def verify_status(self, resp):
        if (resp.status_code not in [200, 201, 202]):
            json_resp = json.loads(resp.content)
            for key in json_resp.keys():
                self.log.debug("%s: %s" % (key, json_resp[key]))
            raise RuntimeError("bad response(%s) see log for more details: %s" % (resp.status_code, resp.reason))


    def sleep(self, sec):
        time.sleep(sec)

####################################################################################################
####################################################################################################
#       generic GET/PUT/...
    def get(self, url, headers=None, timeout=2):
        self.sleep(timeout)

        if (headers == None):
            headers = self.headers

        request_url = self.base_url + url
        self.log.debug("doing a GET on: " + request_url)

        response = requests.get(request_url, data={}, headers=headers)
        self.verify_status(response)
        return response

    def post(self, url, body, headers=None):
        if (headers == None):
            headers = self.headers

        request_url = self.base_url + url
        self.log.debug("doing a POST on: " + request_url)

        response = requests.post(request_url, data=body, headers=headers)
        self.verify_status(response)
        return response

    def put(self, url, body, headers=None):
        if (headers == None):
            headers = self.headers

        request_url = self.base_url + url
        self.log.debug("doing a PUT on: " + request_url)

        response = requests.put(request_url, data=body, headers=headers)
        self.verify_status(response)
        return response

####################################################################################################
####################################################################################################
# specific CHAPI GETs
    def get_dev(self, loc_id, dev_id):
        return self.get("/locations/%s/devices/%s" % (loc_id, dev_id))

    def get_devs(self, loc_id):
        return self.get("/locations/%s/devices" % loc_id)

    def get_eula(self):
        return self.get("/EULA?LanguageLocaleID=en-US")

    def get_humid(self, loc_id, dev_id):
        return self.get("/locations/%s/devices/%s/thermostat" % (loc_id, dev_id))

    def get_loc(self, loc_id):
        return self.get("/locations/%s" % loc_id)

    def get_locs(self):
        return self.get('/Locations/')

    def get_otbs(self, loc_id):
        return self.get('/locations/%s/onetouchbuttons' % loc_id)

    def get_thermostat(self, loc_id, dev_id):
        return self.get("/locations/%s/devices/%s/thermostat" % (loc_id, dev_id))

    def get_thermostat_cv(self, loc_id, dev_id):
        return self.get("/locations/%s/devices/%s/thermostat/changeableValues" % (loc_id, dev_id))

    def get_user(self, user_id):
        return self.get("/user/%s" % user_id)

    def get_weather(self, loc_id):
        return self.get("/locations/%s/Weather" % loc_id)

####################################################################################################
####################################################################################################
# specific CHAPI POSTs

    def post_session(self, user):

        resp_text = self.get_eula().text
        self.eula_id = json.loads(resp_text)['eulaId']


        body = {'username': user.username,
                'password': user.password,
                'language': self.data.api.language,
                'acceptedEULAId': self.eula_id}

        response = self.post("/Session", body)

        response_body = json.loads(response.text)
        response_headers = response.headers

        self.headers={}
        self.headers['Cookie']                   = "___CHAPI_SESSION_ID___=" + response_body['sessionID']
        self.headers['___CHAPI_SESSION_ID___']   = response_body['sessionID']
        self.headers['RequestVerificationToken'] = response_headers['requestverificationtoken'] + ":" + response_body['bodytoken']

        self.headers['Accept-Language']          = "en;q=1, ru;q=0.9, ms;q=0.8, de;q=0.7, pt;q=0.6, es;q=0.5"
        #this broke PUTs self.headers['Content-Type']             = "application/json; charset=utf-8"
        self.headers['User-Agent']               = "Lyric/233 (iPhone Simulator; iOS 7.1; Scale/2.00)"
        self.headers['Accept']                   = 'application/json'
        self.headers['Accept-Encoding']          = "gzip, deflate"
        self.headers['Connection']               = "keep-alive"
        self.headers['Proxy-Connection']         = "keep-alive"
        return response

    def post_heat_cool(self, loc_id, dev_id, heat_cool):
        """
        This method still needs some work.  The setpoints and changeover status could be gotten from the current setpoints or something...
        I would not have included them here but they are necessary per the API's spec
        """

        url = "/locations/%s/devices/%s/thermostat/changeableValues" % (loc_id, dev_id)
        body = {
            "mode": heat_cool,
            "autoChangeoverActive": False,
            "heatSetpoint": "50.0",
            "coolSetpoint": "80.0"
            }

        return self.post(url, body)

####################################################################################################
####################################################################################################
# specific CHAPI PUTs

    def put_home_setpoints(self, loc_id, dev_id, home_heat, home_cool):

        url = "/locations/%s/devices/%s/Settings/HomeSetPoints" % (loc_id, dev_id)
        body = {"homeHeatSP": float(home_heat),
                "homeCoolSP": float(home_cool),
                "units": "Fahrenheit"}

        return self.put(url, body)


    def put_away_setpoints(self, loc_id, dev_id, away_heat, away_cool):

        url = "/locations/%s/devices/%s/Settings/AwaySetPoints" % (loc_id, dev_id)
        body = {"awayHeatSP": float(away_heat),
                "awayCoolSP": float(away_cool),
                "units": "Fahrenheit"}

        return self.put(url, body)
