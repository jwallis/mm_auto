
import os.path
import time
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from mats.utils import SourceParser
from mats.utils import operating_system
from mats.decorators import trace
from mats.appium.ui.errors import NoSuchElementException, WebDriverException
import logging


class UIDevice(object):
    def __init__(self, session):
        self.log = logging.getLogger("mats.appium." + self.__class__.__name__)
        self.session = session
        self.driver = session.driver
        self.platform = session.platform
        self.height = self.width = -1
        self.device_os_version = None
        self.device_model = None
        self.screenshot_fn_prefix = ''

        #just to make methods a little easier to read
        self.ios = (self.platform == 'ios')
        self.android = (self.platform == 'android')
        self.selendroid = (self.driver.capabilities['browserName'] == 'selendroid')

        #are we on hardware?
        self.hardware = self.session.settings.getboolean('general', 'use_hardware')
        self.simulator = not self.hardware

    def set_device_info(self, device_os_version, device_model):
        # see GenericFlow.__init__ and GenericFlow.set_device_info
        # device_os_version for ios sim comes from the .json (sdk_version)
        self.device_os_version = device_os_version
        self.device_model = device_model

    @trace
    def page_source(self, full=False, print_to_console=True):
        parser = SourceParser(self.platform, self.driver)
        parser.parse(full)

        if (not print_to_console):
            return

        print parser.out_str

        if (not full):
            print "\ntry page_source('full') for more"
        return parser

    @trace
    def tap_ios_temp(self, x=0.5, y=0.5, duration=0.1, count=1, x2=None, y2=None, x3=None, y3=None):
        self.log.debug('complex devce.tap()')


        #handle x/y args < 1 (percentages)
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']

        positions = []
        for coord_tuple in [(x, y), (x2, y2), (x3, y3)]:
            temp_x = coord_tuple[0]
            temp_y = coord_tuple[1]

            if (temp_x != None):
                if (temp_x < 1):
                    temp_x = coord_tuple[0] * width
                if (temp_y < 1):
                    temp_y = coord_tuple[1] * height
                coord_tuple = (temp_x, temp_y)
                positions.append(coord_tuple)
            else:
                break

        #simple tap with 1 finger.  use "tap" it's a little faster
        if (duration == 0.1 and x2 == None and count == 1):
            self.log.debug('simple tap at: (%f,%f), duration: %f, count: %s' % (x, y, duration, count))
            return self.driver.tap(positions)


        #for appium 1.0 upgrade.  duration was changed for seconds to milliseconds.  We need to multiply by 1000
        duration = duration * 1000


        TAs = []
        for pos in positions:
            ta = TouchAction(self.driver)
            if (count > 1):
                ta = ta.tap(x=pos[0], y=pos[1], count=count)
            else:
                ta = ta.long_press(x=pos[0], y=pos[1]).wait(duration).release()
            TAs.append(ta)

        if (len(TAs) == 1):
            return TAs[0].perform()
        elif (len(TAs) == 2):
            ma = MultiAction(self.driver)
            ma.add(TAs[0], TAs[1])
            self.log.debug('multi-tap at: (%f,%f), (%f,%f), duration: %f, count: %s' % (x, y, x2, y2, duration, count))
            ma.perform()
        elif (len(TAs) == 3):
            ma = MultiAction(self.driver)
            ma.add(TAs[0], TAs[1], TAs[2])
            self.log.debug('multi-tap at: (%f,%f), (%f,%f), (%f,%f), duration: %f, count: %s' % (x, y, x2, y2, x3, y3, duration, count))
            ma.perform()

    @trace
    def tap(self, x=0.5, y=0.5, duration=0.1, count=1, x2=None, y2=None, x3=None, y3=None):
        if (self.platform=='ios'):
            return self.tap_ios_temp(x=x,y=y,duration=duration,count=count,x2=x2,y2=y2,x3=x3,y3=y3)

        self.log.debug('complex devce.tap()')
        self.log.debug('tapping at: %f,%f, duration: %f, count: %s' % (x, y, duration, count))

        if (count > 1):
            raise RuntimeError("multi-tapping is not yet supported. can probably do using multi-touch action chain beginning with 'press'.  see https://github.com/appium/python-client")


        #
        #
        # for appium 1.0 upgrade.  duration was changed for seconds to milliseconds.  We need to multiply by 1000
        duration = duration * 1000
        #
        #
        #


        #simple tap with 1 finger
        if (duration==100 and x2 == None and count==1):
            positions = [(x, y)]
            self.driver.tap(positions)

        if (x2!=None):
            if (duration > 100):
                self.log.debug("seems to be a bug where simultaneous multi-finger tap does not work with a long duration.  we'll call it with your long duration but it may not work...")

            self.log.debug("seems to be a bug where if you do simultaneous multi-finger tap, it needs x,y coordinates like 200, 450 (not .3, .5).  Converting now.")

            size=self.driver.get_window_size()
            width =size['width']
            height=size['height']

            positions=[]
            for coord_tuple in [(x, y), (x2, y2), (x3, y3)]:
                temp_x = coord_tuple[0]
                temp_y = coord_tuple[1]

                if (temp_x!=None):
                    if (temp_x < 1):
                        temp_x = coord_tuple[0] * width
                    if (temp_y < 1):
                        temp_y = coord_tuple[1] * height
                    coord_tuple = (temp_x, temp_y)
                    positions.append(coord_tuple)
                else:
                    break

            self.log.debug('fancy tapping at: %s, duration: %f, count: %s' % (positions, duration, count))
        else:
            positions = [(x, y)]

        self.driver.tap(positions, duration)


    def set_screenshot_path(self, path):
        self.screenshot_path = path

    def set_screenshot_filename_prefix(self, fn_prefix):
        self.screenshot_fn_prefix = fn_prefix

    def _get_screenshot_filename(self, path, identifier):
        timestamp = time.asctime(time.localtime(time.time()))

        if identifier:
            if (identifier[-3:] == '.py'):
                identifier = identifier[0:-3]
            fn = identifier + '_' + timestamp + ".png"
        else:
            fn = 'ss_' + timestamp + ".png"

        fn = self.screenshot_fn_prefix + fn

        time.asctime(time.localtime(time.time()))

        #change possible unicode to string
        fn = str(fn)
        fn = str.replace(fn, ':', '-')

        filename = path + fn

        if (os.path.exists(filename)):
            #not DRY but will keep us out of infinite loop, which SHOULD never happen I realize, but stranger things have
            time.sleep(1)
            time.asctime(time.localtime(time.time()))

            #change possible unicode to string
            fn = str(fn)
            fn = str.replace(fn, ':', '-')

            filename = path + fn

        return filename

    @trace
    def screenshot(self, identifier=None, path=None):
        """
        Captures a screenshot of the current screen and saves it
        to the file system

        :param identifier: A "project & testcase unique" id to save the screenshot as.  Example: "CompanyX_ProjectY_2.0_Android_45983"
        :param path: The path to the filename.  Should typically not be used.
        """

        # this is wrapped because an error here would hide an exception thrown during actual test execution
        # so we basically have to die just with logging if screenshot fails...
        try:
            #first see if path was passed in
            #2nd check if someone's called set_screenshot_path
            #3rd use default
            if (not path):
                if hasattr(self,'screenshot_path'):
                    path = self.screenshot_path + '/'
                else:
                    path = self.session.settings.get('appium', 'screenshot_path') + '/'

            if (path[-1:] != '/'):
                path = path + '/'

            if not os.path.exists(path):
                os.makedirs(path)

            filename = self._get_screenshot_filename(path, identifier)

            self.log.debug('creating screenshot at: %s' % os.path.abspath(filename))

            i = 3 # try this many times...
            while True:
                i-=1
                try:
                    self.driver.get_screenshot_as_file(os.path.abspath(filename))
                    break
                except WebDriverException, e:
                    if (i == 0):
                        raise e

        except Exception, e:
            self.log.error('device.screenshot failed: %s' % e)

    def reset_device_log(self):
        """
        Android: calls get_log in order to clear the buffer of logcat stuff.  Call this during setup for your script.
        iOS: nothing yet
        """
        if (self.android):
            self.driver.get_log('logcat')

    def dump_device_log(self, filename):
        """
        Android: dumps "adb logcat" to a log
        iOS: nothing yet
        """
        if (self.android):
            path = self.session.settings.get('appium', 'screenshot_path') + '/'
            outfilename = path + filename[:-3] + '_' + time.asctime(time.localtime(time.time())) + ".logcat"
            outfilename = str.replace(str(outfilename), ':', '-')
            outfile = open(outfilename, 'w')

            for line in self.driver.get_log('logcat'):
                timestampA = line['timestamp'] / 1000
                timestampB = line['timestamp'] % 1000

                timestampA = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestampA))

                # will look like
                # 2015-04-20 13:36:50,466
                msg = "%s,%s" % (timestampA, timestampB)

                for k in line.keys():
                    if (k == 'timestamp'):
                        continue

                    msg += ' [%s]: %s' % (k, line[k])

                outfile.write(str(msg) + '\n')

            outfile.close()


    @trace
    def flick(self, startx, starty, endx, endy, fingers=1):
        """
        Flick the screen.
        """
        self.log.debug('device: flicking %d %d %d %d %d' % (startx, starty, endx, endy, fingers))
        self.driver.flick({
            "touchCount": fingers,
            "startX": startx,
            "startY": starty,
            "endX": endx,
            "endY": endy
        })

    @property
    def orientation(self):
        """
        Returns the current orientation of the device.  Possible values
        are: LANDSCAPE or PORTRAIT.
        """
        return self.driver.orientation

    @orientation.setter
    def orientation(self, orientation):
        """
        Sets the current orientation of the device.
        :param orientation: LANDSCAPE or PORTRAIT.
        """
        self.log.debug('setting orientation to: %s' % (orientation))

        current = self.driver.orientation
        if (current != orientation):
            self.driver.orientation = orientation

    #################################################################################
    # End hardware keys...
    
    #################################################################################

    def swipe_ios_sim(self, startx, starty, endx, endy, duration):
        self.log.debug('device: swipe_ios_sim: %s, %s, %s, %s, %s' % (startx, starty, endx, endy, duration))

        #see _generic.py
        if (self.device_model=='sim iphone 4'):
            #reported by device.get_window_size(): 320/480
            window_width = '320'
            window_height = '502'
        elif (self.device_model in ['sim iphone 5', 'sim iphone 5s']):
            #reported by device.get_window_size(): 320/568
            window_width = '320'
            window_height = '590'
        elif (self.device_model=='sim iphone 6'):
            #reported by device.get_window_size(): 375/667
            window_width = '375'
            window_height = '689'
        elif (self.device_model == 'sim iphone 6 plus'):
            #reported by device.get_window_size(): 414/736
            window_width = '372'
            window_height = '684'
        else:
            raise RuntimeError('invalid device name: %s' % self.device_model)

        from subprocess import call
        call(['/usr/bin/python', '/usr/bin/swipeInWindow.py', 'iOS Simulator', str(startx), str(starty), str(endx), str(endy), str(duration), window_width, window_height])

    @trace
    def swipe(self, startx, starty, endx, endy, duration=.5, element=None):
        """
        Swipe across the screen or element.
        If phone rotates, x and y rotate with it.

        For the start and end points, if the values are less than one,
        then it is taken as a proportion of the element or screen.
        For example, 0.5 would be considered the center of the element or screen.

        duration is time in seconds.  appium 1.0 changed to milliseconds, but we'll do the conversion for you.

        :param startx: Starting position on the horizontal axis.
        :param starty: Starting position on the vertical axis.
        :param endx: Ending position on the horizontal axis.
        :param endy: Ending position on the vertical axis.
        :param duration: (optional) Number of seconds to do the swipe (shorter is faster).
        :param element: (optional) The element to start in.

        """
        self.log.debug('device: swipe: %s, %s, %s, %s, %s' % (startx, starty, endx, endy, duration))

        if (element != None):
            raise RuntimeError("swipe on an element not yet supported.  Not sure if we can do this as of appium 1.0. see https://github.com/appium/python-client")

        #hack for xcode 5/ios 7 sim
        if ((not self.hardware) and self.session.platform == 'ios' and self.device_os_version in ['7.0', '7.1', "8.1"]):
            return self.swipe_ios_sim(startx, starty, endx, endy, duration)

        args = {
            "touchCount": "1",
            "startX": startx,
            "startY": starty,
            "endX": endx,
            "endY": endy,
            "duration": duration
        }

        self.log.debug('device: swiping: %s' % args)


        if (self.driver.capabilities['browserName'].lower() == 'selendroid'):
            if (element):
                raise RuntimeError("swiping on a specific element in selendroid is not yet supported by MATS")

            h,w = self.get_window_size()
            if (startx < 1.0): startx = w * startx
            if (starty < 1.0): starty = h * starty
            if (endx < 1.0): endx = w * endx
            if (endy < 1.0): endy = h * endy

            self.log.debug('device: swiping: updated coords: %s, %s, %s, %s' % (startx, starty, endx, endy))

            ta = TouchActions(self.driver).tap_and_hold(startx, starty)
            ta.move(endx, endy)
            ta.release(endx, endy)
            ta.perform()
        elif (self.platform == 'android'):
            try:
                #for appium 1.0 upgrade.  duration was changed for seconds to milliseconds.  We need to multiply by 1000
                self.driver.swipe(startx, starty, endx, endy, duration * 1000)
            except WebDriverException, e:
                self.log.debug("in device.swipe(). caught and swallowed exception: %s" % e)

        elif (self.platform == 'ios'):
            #for appium 1.0 upgrade.  duration was changed for seconds to milliseconds.  We need to multiply by 1000
            self.driver.swipe(startx, starty, endx, endy, duration * 1000)

        else:
            raise RuntimeError("invalid platform: %s" % self.platform)

        #do a sleep because if we do a really fast swipe we want to wait for the inertial movement to stop
        if (duration <= .2):
            time.sleep(2)
        elif (duration <= .4):
            time.sleep(1)
        elif (duration <= .8):
            time.sleep(.8-duration)

    @trace
    def scroll(self, startx, starty, endx, endy, duration=.5, element=None):
        """
        IOS ONLY!
        Workaround for xcode 5.0 breaking swipe. Works on scrolling in listviews, scrollviews and possibly other places.

        Not sure if this works for horizontal "scrolls" or if vertical only.

        Swipe the screen or element.
        If phone rotates, not sure if x and y rotate with it.

        For the start and end points, if the values are less then one,
        then it is taken as a proportion of the element or screen.
        For example, 0.5 would be considered the center of the element
        or screen.

        :param startx: Starting position on the horizontal axis.
        :param starty: Starting position on the vertical axis.
        :param endx: Ending position on the horizontal axis.
        :param endy: Ending position on the vertical axis.
        :param duration: (optional) Number of seconds to do the swipe (shorter is faster).
        :param element: (optional) The element to start in.
        """
        args = {
            "touchCount": "1",
            "startX": startx,
            "startY": starty,
            "endX": endx,
            "endY": endy,
            "duration": duration
        }

        if element:
            args["element"] = element.id

        self.log.debug('device: scrolling: %s' % args)

        if (self.platform == 'ios'):
            self.driver.scroll(args)
        else:
            raise RuntimeError("this only works on ios, sorry.  Try swipe()")

    def get_window_size(self):
        """
        Gets window size.  If already called in this session, will use locally cashed results
        :return: tuple of (height,width)
        """
        if (self.height != -1):
            return (self.height, self.width)

        s=self.driver.get_window_size()
        self.height=s['height']
        self.width =s['width']

        return (self.height, self.width)

    def bezel_swipe_left(self, starty=None, endy=None):
        """
        swipes in from left, halfway down the screen
        optional params: you can include starty to do a straight across swipe at that Y coord
          or you can include starty and endy to do a diagonal bezel swipe
        """
        if (starty==None):
            starty=endy=.5
        elif (endy==None):
            endy=starty

        self.swipe(0.001, starty, .8, endy)

    def bezel_swipe_right(self, starty=None, endy=None):
        """
        swipes in from right, halfway down the screen
        optional params: you can include starty to do a straight across swipe at that Y coord
          or you can include starty and endy to do a diagonal bezel swipe
        """
        if (starty==None):
            starty=endy=.5
        elif (endy==None):
            endy=starty

        self.swipe(.9999, starty, .2, endy)

    def bezel_swipe_top(self, startx=None, endx=None):
        """
        swipes in from top, halfway across top of the screen
        optional params: you can include startx to do a straight vertical swipe at that x coord
          or you can include startx and endx to do a diagonal bezel swipe
        """
        if (startx==None):
            startx=endx=.5
        elif (endx==None):
            endx=startx

        self.swipe(startx, 0.001, endx, .8)

    def bezel_swipe_bottom(self, startx=None, endx=None):
        """
        swipes in from bottom, halfway across top of the screen
        optional params: you can include startx to do a straight vertical swipe at that x coord
          or you can include startx and endx to do a diagonal bezel swipe
        """
        if (startx==None):
            startx=endx=.5
        elif (endx==None):
            endx=startx

        self.swipe(startx, .9999, endx, .2)

    def scroll_to_top(self, max_scrolls=5):
        for i in range(max_scrolls):
            self.swipe(.5, .2, .5, .8, 1)

    def scroll_to_bottom(self, max_scrolls=5):
        for i in range(max_scrolls):
            self.swipe(.5, .8, .5, .2, 1)

    def move_cursor_to_end(self):
        if (self.platform == 'android'):
            self.driver.press_keycode(123)
        elif (self.platform == 'ios'):
            self.driver.press_keycode(20)
        else:
            raise RuntimeError("invalid platform: %s" % self.platform)

    @trace
    def lock_and_unlock(self, seconds=1):
        self.log.debug('device: lock_and_unlock')
        if (self.session.platform == 'ios'):
            self.driver.lock(seconds)
            for i in range(2):
                try:
                    # on the ios sim, the UNLOCK part of mobile: lock doesn't work, we have to swipe across manually (twice sometimes, apparently).
                    # if the SlideToUnlock element exists, we need to do the manual swipe
                    self.driver.find_element_by_name('SlideToUnlock')
                    self.swipe(.1, .8, .9, .8)
                except NoSuchElementException:
                    #success!
                    pass

            time.sleep(2)

        elif (self.session.platform == 'android'):
            self.power()
            time.sleep(seconds)
            self.power()
            time.sleep(1)
            if (self.device_model in ['moto x','moto g', 'nexus 6']):
                self.swipe(.5, .85, .5, .5)
            else:
                raise RuntimeError("in mats/appium/ui.py: lock_and_unlock() does not yet support %s" % self.device_model)
            time.sleep(2)

        else:
            raise RuntimeError("invalid platform: %s" % self.platform)


    def hide_keyboard(self):
        if self.ios:
            raise RuntimeError("Method not implemented for iOS")
        elif self.android:
            self.driver.hide_keyboard()



########## hardware keys... ##########
# some specific to ios, some specific to android, a few that work on both...
# see also:
# http://developer.android.com/reference/android/view/KeyEvent.html
# http://developer.android.com/tools/help/uiautomator/UiDevice.html


    @trace
    def reset(self):
        """
        Reset the app.
        For both platforms this will force quit, uninstall, reinstall, launch the app.
        """
        self.log.debug('device: reset')
        self.driver.reset()

    @trace
    def shake(self):
        self.log.debug('device: shake')
        self.driver.shake()
        time.sleep(2)

    def bring_sim_window_to_front(self):
        """
        Brings the ios or android simulator window to the foreground, probably so we can do sneaky stuff...
        """
        if (not self.simulator):
            raise RuntimeError("bring_sim_window_to_front() is only for the simulator")

        if (self.ios):
            window_name = 'iOS Simulator'
        elif (self.android):
            window_name = 'emulator64-x86'
        else:
            raise RuntimeError("bad platform")

        operating_system.bring_osx_window_to_front(window_name)

    def set_lat_long(self, lat, long):
        self.driver.set_location(lat, long)


class UIIOSDevice(UIDevice):
    def __init__(self, session):
        super(UIIOSDevice, self).__init__(session)


    @trace
    def app_switch(self):
        self.bring_sim_window_to_front()
        time.sleep(.2)

        operating_system.send_keys_to_osx('h', shift=True, command=True)
        operating_system.send_keys_to_osx('h', shift=True, command=True)
        time.sleep(.2)

    @trace
    def background(self, seconds=1):
        self.log.debug('device: backgrounding')
        self.driver.background_app(seconds)
        time.sleep(2)

    @trace
    def home(self):
        self.bring_sim_window_to_front()
        time.sleep(.5)

        operating_system.send_keys_to_osx('h', shift=True, command=True)
        time.sleep(1)


class UIAndroidDevice(UIDevice):
    def __init__(self, session):
        super(UIAndroidDevice, self).__init__(session)

    @trace
    def app_switch(self):
        self.log.debug('device: app_switch')
        self.driver.press_keycode(187)
        time.sleep(.5)

    @trace
    def back(self):
        self.log.debug('device: back')
        self.driver.press_keycode(4)
        # did not want to do this, but sometimes if you do a:

        # device.back()
        # find('something')

        # the find() will execute before the phone actually completes the "back" animation, so the find() will execute on the wrong screen
        time.sleep(.5)

    @trace
    def calculator(self):
        self.log.debug('device: calculator')
        self.driver.press_keycode(210)

    @trace
    def calendar(self):
        self.log.debug('device: calendar')
        self.driver.press_keycode(208)

    @trace
    def call(self):
        self.log.debug('device: call')
        self.driver.press_keycode(5)

    @trace
    def delete(self, count=1):
        self.log.debug("device: delete: %s" % count)
        for i in range(count):
            self.driver.press_keycode(67)

    @trace
    def camera(self):
        self.log.debug('device: camera')
        self.driver.press_keycode(27)

    @trace
    def contacts(self):
        self.log.debug('device: contacts')
        self.driver.press_keycode(207)

    @trace
    def end_call(self):
        self.log.debug('device: end call')
        self.driver.press_keycode(6)

    @trace
    def enter(self):
        self.log.debug('device: enter')
        self.driver.press_keycode(66)

    @trace
    def forward(self):
        self.log.debug('device: forward')
        self.driver.press_keycode(125)

    @trace
    def home(self):
        """goes to homescreen, then to be sure, taps home again so that we're at a known place."""
        self.log.debug('device: home')
        self.driver.press_keycode(3)
        time.sleep(1)
        self.driver.press_keycode(3)
        time.sleep(.5)

    @trace
    def menu(self):
        self.log.debug('device: menu')
        self.driver.press_keycode(82)
        time.sleep(.5)

    @trace
    def mute(self):
        self.log.debug('device: mute')
        self.driver.press_keycode(91)

    @trace
    def open_notifications(self):
        self.log.debug('device: open_notifications')
        self.driver.open_notifications()

    @trace
    def power(self):
        self.log.debug('device: power')
        self.driver.press_keycode(26)

    @trace
    def search(self):
        self.log.debug('device: search')
        self.driver.press_keycode(84)
        time.sleep(1)

    @trace
    def start_activity(self, package, activity):
        """haven't really investigated this yet.  documentation says "Open an activity in the current app or start a new app and open an activity Android only"""
        #example from doc: self.driver.start_activity('com.example.android.apis', '.Foo')
        self.log.debug('device: start_activity: %s, %s' % (package, activity))
        self.driver.start_activity(package, activity)


    #I'm not sure of which of these works and which don't.
    # See also: Flow.switch_to_emoji_keyboard(), Flow.switch_to_alphabet_keyboard()
    # KEYCODE_SWITCH_CHARSET
    # Key code constant: Switch Charset modifier key. Used to switch character sets (Kanji, Katakana).
    # Constant Value: 95
    #
    # KEYCODE_LANGUAGE_SWITCH
    # Key code constant: Language Switch key. Toggles the current input language such as switching between English and Japanese on a QWERTY keyboard. On some devices, the same function may be performed by pressing Shift+Spacebar.
    # Constant Value: 204
    #
    #
    # KEYCODE_PICTSYMBOLS
    # Key code constant: Picture Symbols modifier key. Used to switch symbol sets (Emoji, Kao-moji).
    # Constant Value: 94


    @trace
    def tab(self):
        self.log.debug('device: tab')
        self.driver.press_keycode(61)

    @trace
    def volume_up(self):
        self.log.debug('device: volume up')
        self.driver.press_keycode(18)

    @trace
    def volume_down(self):
        self.log.debug('device: volume down')
        self.driver.press_keycode(19)
