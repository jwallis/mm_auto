# This file holds methods that every automation project will use...
# This file will likely grow and be split into multiple files...

from _external import *
from strings_generic import *
from ..strings_specific import *

from system import System

class GenericFlow(System, object):

####################################### setup kinda stuff #######################################
    def __init__(self, **kwargs):
        #logging...
        self.filename = os.path.basename(inspect.stack()[2][1])
        self.log = logging.getLogger("mats.test.%s.%s" % ( self.__class__.__name__, self.filename))
        self.log.debug('Setting up the test...')

        #setup internal structures...
        self.session = mats.get_session(**kwargs)
        self.settings, self.config = mats.get_settings()
        self.app = self.session.app()
        self.driver = self.app.driver
        self.device = self.session.device()
        self.platform = self.session.platform

        #just to make test scripts a little easier to read
        self.ios = (self.platform == 'ios')
        self.android = (self.platform == 'android')
        self.selendroid = (self.driver.capabilities['browserName'] == 'selendroid')


        #are we on hardware?
        self.hardware = self.session.settings.getboolean('general', 'use_hardware')
        self.simulator = not self.hardware

        #device model and os version
        self.set_device_info()

        #datums...
        self.setup_data()
        self.setup_strings() # sets self.current_language which looks like 'en_US'
        self.status = 'fail'

    def __getattr__(self, item):
        """
        what's happening here is if we call 'my_flow.some_method()' we'll actually end up calling 'my_flow.app.some_method()'
        """
        return getattr(self.app, item)

    def setup_strings(self, lang=True):
        """
        For internationalization.
        All this method does is set a ton of variables (such as my_flow.strings.system_settings)
        optional param (defaults to self.data.language) should be something like 'en_US' or 'de_DE'
        """
        if (lang==True):
            lang = self.data.language

        #we're creating a member variable and then passing it to the methods for them to modify...
        self.strings = AttrDict()

        #self.current_language looks something like "English"
        #self.current_language_code looks something like "en_US"
        self.current_language, self.current_language_code = set_strings_generic(lang, self.strings, self.platform)
        set_strings_project_specific(lang, self.strings, self.platform)

    def set_device_info(self):
        #tested:
        #mma-iphone-f7 white iphone5
        #
        #mma-p-and-42 white s4 with cover
        #...20 galaxy s2
        #...58 pregnant s3
        #...73 moto g
        #...74 moto g
        #...75 s5
        #...76 moto x
        #...53 gal nex
        #...51 s4

        # device_os_version for ios sim comes from the .json (sdk_version)
        self.device_os_version = self.session.device_os_version
        device_model = self.session.device_model.lower()

        if (self.ios):
            ################## phone ##################
            #for some reason, iDeviceInfo reports some iphone4 as iphone3
            if (device_model in ["iphone4,1", "iphone3,1"]):
                self.device_model = "iphone 4"
            elif (device_model == "iphone5,1"):
                self.device_model = "iphone 5"

            #simulators
            elif (device_model == 'iphone 4s'):
                self.device_model = 'sim iphone 4s'
            elif (device_model == 'iphone 5'):
                self.device_model = 'sim iphone 5'
            elif (device_model == 'iphone 5s'):
                self.device_model = 'sim iphone 5s'
            elif (device_model == 'iphone 6'):
                self.device_model = 'sim iphone 6'
            elif (device_model == 'iphone 6 plus'):
                self.device_model = 'sim iphone 6 plus'


            ################## tablet ##################


            elif (device_model == 'ipad 2'):
                self.device_model = 'sim ipad 2'
            elif (device_model == 'ipad retina'):
                self.device_model = 'sim ipad retina'
            elif (device_model == 'ipad air'):
                self.device_model = 'sim ipad air'




            else:
                raise RuntimeError("unknown device model: %s" % device_model)

        else:

            # do this and look for ro.product.model:
            # adb shell getprop

            # all names LOWERCASE !!!

            ################## phone ##################
            if (device_model in ['xt1053', 'xt1060', 'xt1056']):
                self.device_model = 'moto x'
            elif (device_model == 'xt1045'):
                self.device_model = 'moto g'

            elif (device_model in ['sgh-t989', 'gt-i9100']):
                self.device_model = 'galaxy s2'
            elif (device_model in ['samsung-sgh-i747', 'sch-i535']):
                self.device_model = 'galaxy s3'
            elif (device_model in ['gt-i9500', 'gt-i9505g']):
                self.device_model = 'galaxy s4'
            elif (device_model == 'sm-g900v'):
                self.device_model = 'galaxy s5'

            elif (device_model == 'samsung-sgh-i717'):
                self.device_model = 'galaxy note'

            elif (device_model == 'galaxy nexus'):
                self.device_model = 'galaxy nexus'
            elif (device_model == 'nexus 4'):
                self.device_model = 'nexus 4'
            elif (device_model == 'nexus 5'):
                self.device_model = 'nexus 5'
            elif (device_model == 'nexus 6'):
                self.device_model = 'nexus 6'


            elif (device_model == 'htc one'):
                self.device_model = 'htc one'

            ################## tablet ##################



            else:
                print "GenericFlow.set_device_info() warning: unknown device model: %s" % device_model

        self.device.set_device_info(self.device_os_version, self.device_model)





###################### pass/fail/blacked ######################
    def fail(self, message):
        """
        Quits the testcase with Failed status
        :param message: the message that is sent with the Blocked status
        """
        raise Exception("Fail: " + message)

    def blocked(self, message):
        """
        Quits the testcase with Blocked status
        :param message: the message that is sent with the Blocked status
        """
        self.status = 'blocked'
        raise Exception("Blocked: " + message)

    def blocked_on_android(self, message):
        """
        Quits the testcase with Blocked status if platform = android
        :param message: the message that is sent with the Blocked status
        """
        if (self.android):
            self.blocked("blocked_on_android: " + message)

    def blocked_on_ios(self, message):
        """
        Quits the testcase with Blocked status if platform = ios
        :param message: the message that is sent with the Blocked status
        """
        if (self.ios):
            self.blocked("blocked_on_ios: " + message)

    def blocked_on_ios_sim(self, message):
        """
        Quits the testcase with Blocked status if platform = ios and on simulator
        :param message: the message that is sent with the Blocked status
        """
        if (self.ios):
            self.blocked("blocked_on_ios_sim: " + message)


    def blocked_unless_android(self, message):
        """
        Quits the testcase with Blocked status unless platform = android, otherwise the test continues
        :param message: the message that is sent with the Blocked status
        """
        if (not self.android):
            self.blocked("blocked_unless_android: " + message)

    def blocked_unless_ios(self, message):
        """
        Quits the testcase with Blocked status unless platform = ios, otherwise the test continues
        :param message: the message that is sent with the Blocked status
        """
        if (not self.ios):
            self.blocked("blocked_unless_ios: " + message)

    def blocked_on_devices(self, device_array, message):
        """
        Quits the testcase with Blocked status if the current device is in the specified device list
        :param device_array: the list of devices that should block this test
        :param message: the message that is sent with the Blocked status

        """
        if (self.device_model in device_array):
            self.blocked("blocked_on_devices: " + message)

    def blocked_on_android_version_lower_than(self, lowest_acceptable_version, message):
        """
        Quits the testcase with Blocked status if:
        1-we're using android
        2-the version level is lower than "lowest_acceptable_version"
        :param lowest_acceptable_version: the lowest acceptable version, for example '4.0.4'
        :param message: the message that is sent with the Blocked status
        """
        if (self.android and self.device_os_version < lowest_acceptable_version):
            self.blocked("blocked_on_android_version_lower_than %s: " % lowest_acceptable_version + message)

###################### assertions #########################
    def flow_assert(self, true_false, message):
        """
        haven't found a need for this yet.
        """
        assert true_false, message

    def assert_element_text(self, element_or_element_label, correct_text):
        """
        Asserts that the
        :param element_or_element_label:
        :param correct_text:
        """

              # I don't think this is a good idea.  JUST for ios, sometimes we'd have to check element.name
              # and sometimes we'd have to check element.text just depending on which variables of the element are populated
        if self.android:
            if (type(element_or_element_label) == str):
                actual_text = self.find(element_or_element_label).text
                assert (actual_text == correct_text), 'text of element "%s" should be "%s" but was "%s"' % (element_or_element_label, correct_text, actual_text)
            else:
                actual_text = element_or_element_label.text
                assert (actual_text == correct_text), 'text of element "%s" should be "%s" but was "%s"' % (element_or_element_label.name, correct_text, actual_text)
        elif self.ios:
            if (type(element_or_element_label) == str):
                elem_text = self.find(element_or_element_label).name
                assert (elem_text == correct_text), 'text of element %s should be: %s but was: %s' % (
                    element_or_element_label, correct_text, elem_text)
            else:
                assert (e.name == correct_text), 'text of element should be: %s but was: %s' % (correct_text, e.name)
        else:
            raise RuntimeError('bad platform')


    ###################### simple wrapped methods #########################
    def sleep(self, sleep_time=1):
        self.log.info('sleeping for %s' % sleep_time)
        time.sleep(sleep_time)

    def page_source(self, full=False, print_to_console=True):
        self.device.page_source(full, print_to_console)

###################### helpful methods #########################
    def random_string(self, length=10):
        """
        Generates random string of numbers
        length length of string to return (default == 10)
        """
        length = int(length)
        s = str(random.random())[2:]
        s = s*(length / len(s) + 1)
        return s[0:length]

    def which_string_appears_first(self, string_a, string_b, element_type='statictexts'):
        """
        Pass in two strings, we will return whichever appears FIRST (or None if neither ever appear).
        Helpful for testing ordering
        :param string_a: first string to search for
        :param string_b: second string to search for
        :param element_type: PLURAL version of what we're looking for: 'texts','buttons','images'....
        """
        elems = eval('self.' + element_type + "()")

        for e in elems:
            if (e.text == string_a):
                return string_a
            if (e.text == string_b):
                return string_b

        return None

    def make_safe(self, method): #binary method,  method can't have any arguments for now.
        '''
        Given a method name, the function will return True if method was successfully executed.
        False, otherwise.
        :param method:
        :return True if method successfully executed, False otherwise:
        '''
        try:
            method()
            return True
        except (NoSuchElementException, WebDriverException, RuntimeError):
            return False

##################################################################
# alerts


##################################################################
# ios only stuff
    def does_alert_exist(self):
        return self.has_a('alert')

    def does_keyboard_exist(self):
        """
        IOS ONLY
        :return: True iff a keyboard is present
        """
        self.blocked_on_android("not implemented for android")
        return self.exists_and_visible(element_type='keyboard', timeout=3)

    is_keyboard_visible = does_keyboard_exist

    def iphone_or_ipad(self):
        # self.device_model will look something like "iPhone5,1"
        if (self.device_model.find('iphone') > -1):
            return 'iphone'
        elif (self.device_model.find('ipad') > -1):
            return 'ipad'
        else:
            return False


##################################################################
# webview stuff
# (Selendroid/iOS only)

    def switch_to_webview(self):
        for context in self.driver.contexts:
            if (context.lower().find("web") > -1):
                self.driver.switch_to.context(context)
                return

        raise RuntimeError('Could not find a webview to switch to.  Aborting.')


    def switch_to_native(self):
        for context in self.driver.contexts:
            if (context.lower().find("native") > -1):
                self.driver.switch_to.context(context)
                return

        raise RuntimeError('Could not find the native app to switch to.  Aborting.')


###################### tap/set/get/etc. #########################
########   !!!!!!!!!!!!! ?????????????????
###### should these be defined on MobileApp?

    def check(self, label):
        """
        Check a checkbox
        :param label: The accessibility label (or other tag) of the checkbox
        """
        self.find(label).check()

    def uncheck(self, label):
        """
        Uncheck a checkbox
        :param label: The accessibility label (or other tag) of the checkbox
        """
        self.find(label).uncheck()

    def tap(self, label='', element_type=None, partial=False, timeout=3, duration=0.1, count=1):
        """
        Tap an element
        :param label: The accessibility label (or other tag) of the element
        :param timeout: Optional (default=3 sec), tries to tap for up to 'wait' seconds before failing.
        """
        self.wait_for_element(label, element_type=element_type, partial=partial, timeout=timeout).tap(duration=duration, count=count)

    def double_tap(self, label, timeout=3, count=2):
        self.tap(label=label, timeout=timeout, count=count)

    def long_tap(self, label, timeout=3, duration=1):
        self.tap(label=label, timeout=timeout, duration=duration)

    def tap_safe(self, label, timeout=3, duration=0.1, count=1):
        """
        Tap an element, return False if element does not exist instead of throwing exception
        :param label: The accessibility label (or other tag) of the element
        """
        try:
            #success, we tapped
            self.tap(label=label, timeout=timeout, duration=duration, count=count)
            return True

        # Sometimes tapping gives us an exception.  Mainly this will happen if the element exists but not visible, we try to tap and get an exception.
        except WebDriverException, e:
            if (not self.exists_and_visible(label)):
                # If the element is not visible, it's probably acceptable to just say "we couldn't tap" and return False
                return False
            else:
                # If the element is visible, it's probably a legit error.  Throw it back to the user.
                raise e

    def tap_on_page(self, label, max_scrolls=3, duration=0.1, count=1):
        """
        Tap an element, look for it down the page.
        Unlike tap(), there is NO WAITING FOR the element to exist in this method.
        :param label: The accessibility label (or other tag) of the element
        """
        self.find_on_page(search_term=label, max_scrolls=max_scrolls).tap(duration=duration, count=count)

    def tap_safe_on_page(self, label, max_scrolls=3, duration=0.1, count=1):
        """
        Tap an element, return False if element does not exist instead of throwing exception
        Unlike tap(), there is NO WAITING FOR the element to exist in this method.
        :param label: The accessibility label (or other tag) of the element
        """
        e = self.find_safe_on_page(search_term=label, max_scrolls=max_scrolls)

        if (e):
            e.tap(duration=duration, count=count)
            return True
        else:
            return False

    def tap_by_location(self, label, timeout=3, duration=0.1, count=1, xoffset=0, yoffset=0):
        """
        Tap an element that exists but is not visible.  This is a workaround for an ios bug in which
        we can see the element on the screen but tapping throws a WebDriverException: Message: u'An unknown server-side error occurred while processing the command.'

        :xoffset: If you want to tap something NEAR what we're tapping, use x/y offset.  can be > or < 0.  defaults to 0
        :yoffset: If you want to tap something NEAR what we're tapping, use x/y offset.  can be > or < 0.  defaults to 0

        :param label: The accessibility label (or other tag) of the element
        :param timeout: Optional (default=3 sec), tries to tap for up to 'wait' seconds before failing.
        """


        e = self.wait_for_element_to_exist(label, timeout=timeout)
        e.tap_by_location(duration=duration, count=count, xoffset=xoffset, yoffset=yoffset)

    def get_text(self, label, timeout=3):
        """
        Get text of an element.  Tested for element types: text, button, textfield
        :param label: The acc
        """
        return self.wait_for_element(label, timeout=timeout).text

    def set_text(self, label, txt, element_type=None, timeout=3):
        """
        Set a textfield (or anything else that can accept "send_keys")

        android: uses normal "element.send_keys()"
        ios: uses the "typestring" quick method, which works the same as "send_keys" at the Instruments level, so it
             should be safe to use.  Now what's different about this is that in this method we're doing a TAP on the
             element before doing the "typestring."  This is necessary because the object we're calling the "typestring"
             method on is not the element itself, but the DRIVER.  see the code below...

        :param label: The accessibility label (or other tag) of the textfield
        :param txt: The text to enter in the textfield
        :param element_type: Element type such as 'textfield' useful when your textfield is in a container such as a tableCell
        """
        if (self.android):
            self.wait_for_element(label, element_type, timeout=timeout).send_keys(txt)
        elif (self.ios):
            self.tap(label, element_type, timeout=timeout)
            self.driver.execute_script("target.frontMostApp().keyboard().typeString(\'" + txt + "\')")

    def set_text_fast(self, label, txt, element_type=None, timeout=3):
        """
        Set a textfield the quick way.  Be very cautious with this.

        android: there is no quick way, so this just redirects to set_text()
        ios: uses "set_value" which is very fast but may have weird side effects.  It does NOT simulate tapping the ios keyboard,
             so be SURE to test this, and do NOT use in a situation where you really want to simulate user input

        :param label: The accessibility label (or other tag) of the textfield
        :param txt: The text to enter in the textfield
        :param element_type: Element type such as 'textfield' useful when your textfield is in a container such as a tableCell
        """
        if (self.android):
            self.set_text(label, txt, element_type, timeout)
        elif (self.ios):
            self.wait_for_element(label, element_type, timeout=timeout).set_value(txt)
        else:
            raise RuntimeError("bad platform")

    def set_text_slow(self, label, txt, element_type=None, timeout=3):
        """
        Set a textfield in the traditional "send_keys()" way for ios and android

        android: there is no slow way, so this just redirects to set_text()
        ios: calls the traditional, slow "send_keys()" method

        :param label: The accessibility label (or other tag) of the textfield
        :param txt: The text to enter in the textfield
        :param element_type: Element type such as 'textfield' useful when your textfield is in a container such as a tableCell
        """
        if (self.android):
            self.set_text(label, txt, element_type, timeout)
        elif (self.ios):
            self.wait_for_element(label, element_type, timeout=timeout).send_keys(txt)
        else:
            raise RuntimeError("bad platform")

    def picker_select(self, picker, desired_selection, direction="down"):
        if (picker.tag_name == "UIAPickerWheel"):
            picker_offset = int(picker.size['height']*0.15)
            if(direction=="up"):
                picker_offset = (-1) * picker_offset

            current_selection = picker.text
            loops = 0
            while(current_selection != desired_selection):
                picker.tap_by_location(yoffset=picker_offset)
                # This sleep timer is critical or next_selection will grab the text too fast
                time.sleep(0.5)

                next_selection = picker.text

                if(desired_selection in next_selection):
                    # Found our selection
                    break

                # If we're at the end of the list, go the opposite way
                if(current_selection == next_selection):
                    loops = loops + 1
                    if (loops == 2):
                        raise RuntimeError("picker_select(): Could not find option: " + desired_selection)
                    picker_offset = -1 * picker_offset
                current_selection = next_selection
        else:
            raise RuntimeError("picker_select(): Can only be used on a Pickerwheel element.")

#################################################################
# simple wrappers, makes coding a little easier (code completion, yay!)

    def exists(self, search_term='', element_type=None, partial=False, timeout=0):
        """
        Look for an element, waiting a max of 'timeout' seconds for element JUST TO EXIST (does not have to be visible)
        Returns element if it ever finds it, returns False if not
        """
        return self.app.exists(search_term, element_type, partial, timeout)

    def exists_and_visible(self, search_term='', element_type=None, partial=False, timeout=0):
        """
        Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE
        Returns element if it ever finds it, returns False if not
        """
        return self.app.exists_and_visible(search_term, element_type, partial, timeout)

    def exists_and_visible_on_page(self, search_term='', element_type=None, partial=False, max_scrolls=3, timeout=0):
        """
        1.Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE on the current visible screen
        2.Then (after timeout has expired), starts swiping down the page for the element to exist and be visible.  No more waiting.
        Returns element if it ever finds it, returns False if not
        """
        return self.app.exists_and_visible_on_page(search_term, element_type, partial, max_scrolls, timeout)

    def wait_for_element(self, search_term='', element_type=None, partial=False, timeout=10):
        """
        Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE
        Returns element if it ever finds it, throws NoSuchElementException if not
        """
        return self.app.wait_for_element(search_term, element_type, partial, timeout)

    def wait_for_element_to_exist(self, search_term='', element_type=None, partial=False, timeout=10):
        """
        This is exactly the same as "exists()" but with a default timeout of 10s
        Look for an element, waiting a max of 'timeout' seconds for element JUST TO EXIST
        Returns element if it ever finds it, throws NoSuchElementException if not
        """
        return self.app.wait_for_element_to_exist(search_term, element_type, partial, timeout)

    def wait_for_element_safe(self, search_term='', element_type=None, partial=False, timeout=10):
        """
        This is exactly the same as "exists_and_visible()" but with a default timeout of 10s
        Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE
        Returns element if it ever finds it, returns False if not
        """
        return self.app.wait_for_element_safe(search_term, element_type, partial, timeout)



##################################################################
# development methods (for use in iPython while developing scripts

    def _show_all(self, element_type='all'):
        """
        useful for UIAutomator, which doesn't seem to want to show elements and their properties
        """
        not_found=[]

        if self.ios:

            if (element_type=='all'):
                elems = ["button","checkbox","checked","cell","datepicker","drawer","expandable","frame","gesture","grid","gridlayout","horizontal","image","imagebutton","keyboard","list","media","numberpicker","pagetabstrip","pagetitlestrip","progress","radio","radiogroup","relative","row","scroll","search","seek","space","spinner","switch","table","statictext","textswitcher","texture","textfield","textview","timepicker","toggle","video","viewanimator","viewflipper","viewgroup","viewpager","web","window"]
            else:
                elems = [element_type]

            for etype in elems:
                try:
                    found=[]
                    for e in self.find_all(element_type=etype):
                        found.append((e))

                    print "---%s" % etype
                    for elem in found:
                        name = elem.name
                        txt = elem.text
                        value = elem.value
                        if (name or txt or value):
                            print "   name : %s" % name
                            print "   value: %s" % value
                            print "   text : %s" % txt
                            print "   visible: %s, enabled: %s, selected: %s\n" % (e.visible, e.enabled, e.selected)

                except:
                    not_found.append(etype)

            print "---NOT FOUND:\n%s" % not_found
        elif self.android:
            if (element_type=='all'):
                elems = ["abslist","absseek","absspinner","absolute","adapterview","adapterviewanimator","adapterviewflipper","analogclock","appwidgethost","autocomplete","button","breadcrumbs","calendar","cell","checkbox","checked","chronometer","compound","datepicker","dialerfilter","digitalclock","drawer","expandable","extract","fragmenttabhost","frame","gallery","gesture","glsurface","grid","gridlayout","horizontal","image","imagebutton","imageswitcher","keyboard","linear","list","media","mediaroutebutton","multiautocomplete","numberpicker","pagetabstrip","pagetitlestrip","progress","quickcontactbadge","radio","radiogroup","rating","relative","row","rssurface","rstexture","scroll","search","seek","space","spinner","stack","surface","switch","tabhost","tabwidget","table","statictext","textclock","textswitcher","texture","textfield","timepicker","toggle","twolinelistitem","video","viewanimator","viewflipper","viewgroup","viewpager","viewstub","viewswitcher","web","window","zoom","zoomcontrols",]
            else:
                elems = [element_type]

            for etype in elems:
                try:
                    found=[]
                    for e in self.find_all(element_type=etype):
                        found.append((e))

                    print "---%s" % etype
                    for elem in found:
                        name = elem.name
                        txt = elem.text
                        if (name or txt):
                            print "   name : %s" % name
                            print "   text : %s" % txt
                            print "   visible: %s, enabled: %s, selected: %s\n" % (e.visible, e.enabled, e.selected)

                except:
                    not_found.append(etype)

            print "---NOT FOUND:\n%s" % not_found
        else:
            raise RuntimeError('bad platform')


