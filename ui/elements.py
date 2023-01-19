import types
import logging
import time
from mats.decorators import trace
from appium.webdriver.common.touch_action import TouchAction
from mats.errors import NotConnected, FrameworkError
from .errors import InvalidSearchParameters, ElementNotFound, NoSuchElementException, WebDriverException


def get_web_obj_attribute(web_obj, attribute_name):
    """
    Added via _monkey_patch_webelement() to each web_obj.
    For some reason, not all of the attributes of the selenium web_obj are directly accessible
    (ie. web_obj.is_displayed() works, web_obj.text works, but
    web_obj.name does not. For some reason you have to do this Command.GET_ELEMENT_ATTRIBUTE
    to get ahold of the web_obj's name and value.)

    So this get_web_obj_attribute() is used for myTable.name and possibly others (see UIObject's properties for use of this method)
    """
    try:
        resp = web_obj.get_attribute(attribute_name)
    except NoSuchElementException:
        return None

    if (type(resp) is bool):
        return unicode(resp).lower()
    else:
        return unicode(resp)


class UndefinedElement(object):
    """
    The elements we can select are listed in typeShortcuts:
        https://github.com/appium/appium/blob/master/app/uiauto/lib/mechanic.js#L28
    """

    # This is what elements are first created as while we're searching for them, such as when you do a myTable.cell()
    # If nothing is found, you'll get an UndefinedElement back.  If SOMETHING is found, you'll get a UIObject
    def __init__(self, callback, element_type):
        self.cb = callback
        self.element_type = element_type

    def __call__(self, query=None, partial=False):
        return self.cb(query, self.element_type, partial)


class UIFactory(object):
    """
    Base class to UIBase.  Not sure why this is its own class instead of these methods being part of UIBase.
    """
    def __init__(self, session, web_obj=None):
        # both apps (MobileApp) and elements like buttons (UIObjects) derive from this class,
        # so both apps and buttons have to have a "driver" so that when you search for child elements,
        # the correct part of the element hierarchy will be searched.

        # TODO: find out derived classes to determine if we're app or an element (i.e. parent if we're an element)
        self.log = logging.getLogger("mats.appium.ui." + self.__class__.__name__)
        self.session = session
        self.type_name = self.__class__.__name__
        self.classmap = session.classmap

        if web_obj: #the class we're instantiating is probably a UIObject (button, table, etc.)
            self.driver = self.web_obj = self._monkey_patch_webelement(web_obj)
        else: #the class we're instantiating is probably a MobileApp (app)
            self.web_obj = None
            self.driver = session.driver

    def _monkey_patch_webelement(self, web_obj):
        """
        Adds get_web_obj_attribute() to webdriver object
        """
        web_obj.get_web_obj_attribute = types.MethodType(get_web_obj_attribute, self)
        return web_obj

    def ui_factory_element(self, query, element_type, partial):
        # called when the user says "app.text()" with the parentheses
        # by this I mean, if you just do "app.text" you'll get an UndefinedElement object (see the UndefinedElement class above)
        # then when you put the "()" after the "app.text" you'll call the UndefinedElement.__call__ method
        #
        # so... this ui_factory_element method will find the actual Selenium web_obj element and call _create_object
        # to wrap that web_obj in our UIObject class
        #
        # I, Joshua Wallis, did not write any of this code.  I refactored and commented the hell out of it (there were NONE)
        # in hopes that others could understand it.
        options = {
            'element_type': element_type,
            'search_term': query,
            'partial': partial}
        web_obj = self._find_element(**options)

        if not web_obj:
            if query:
                msg = "Element could not be found: %s(%s" % (element_type, query)
                if partial:
                    msg += ", partial=True)"
                else:
                    msg += ")"
            else:
                msg = "Element could not be found: %s" % element_type
            raise ElementNotFound(msg)

        return self._create_object(web_obj)

    def ui_factory_list(self, query, element_type, partial):
        # called from ui_factory.  finds elements and calls _create_object for each
        options = {
            'element_type': element_type,
            'search_term': query,
            'partial': partial}

        elems = self._find_elements(**options)

        if not elems:
            raise ElementNotFound("Element could not be found: %s" % element_type)

        rv = []
        for elem in elems:
            rv.append(self._create_object(elem))
        return rv

    def _create_object(self, web_obj):
        obj = UIObject(self.session, web_obj)
        return obj

    @trace
    def ui_factory(self, element_type, web_obj=None):
        """
        used by find() and UIBase.__getattr__ to create UIObjects
        """
        self.log.debug('ui_factory: {0} {1}'.format(element_type, web_obj))

        # if we already looked up the object, just create the UIObject...
        if web_obj:
            return self._create_object(web_obj)

        unplural_words = ('progress')

        # ...otherwise create an UndefinedElement, then once that UndefinedElement is called
        # it will create a UIObject
        if element_type in unplural_words:
            return UndefinedElement(self.ui_factory_element, element_type)

        elif element_type[-2:] == 'es':
            if element_type[:-1] in self.classmap.appium_aliases:
                element_type = element_type[:-1]
            else:
                element_type = element_type[:-2]
            return UndefinedElement(self.ui_factory_list, element_type)

        elif element_type[-1] == 's':
            element_type = element_type[:-1]
            return UndefinedElement(self.ui_factory_list, element_type)
        return UndefinedElement(self.ui_factory_element, element_type)


class UIBase(UIFactory):
    """
    Base class to the user-facing UIObject and MobileApp classes.  User will never see a UIBase object
    """
    def __init__(self, session, web_obj=None, attributes=[]):
        super(UIBase, self).__init__(session, web_obj)
        self.attributes = ['id'] + attributes

    def __dir__(self):
        # defines the list of attributes (methods and variables) exposed to the user when she calls dir(myObject).
        # we are manually minimizing the list to only show things like ['id','value','web_obj']
        keys = set([x for x in self.__dict__.keys() if not x.startswith("_")])
        hide = {'attributes', 'classmap', 'driver', 'element', 'log', 'parent','send_keys', 'session', 'type_name', 'ui_factory', 'ui_factory_list', 'child_elem_type'}
        return self.attributes + list(keys - hide)


    def __getattr__(self, attr):
        # __getattr__ is called when we dereference an object but the attribute is NOT a
        # defined function or instance variable, so on elements like a table we can call things like
        # app.table()
        # myButton.visible
        # myButton.text
        # myButton.cell()
        # which are not attributes of any subclass, this class, or this class's ancestor classes.
        # Keep reading...

        # Let's say you have an app or an element like a button or checkbox and you dereference that object
        # with attribute xyz.  xyz could be a variable or a function.  Both are called attributes.
        # You call app.xyz or myButton.xyz or myCheckbox.xyz() and here's what happens...

        # Firstly python will look for attributes in the actual class of the object.
        # app is of class MobileApp (subclass of this class UIBase)
        # myButton is of class UIObject (also a subclass of this class UIBase)
        # myCheckbox is of class UICheckBox (a subclass of UIObject, just has a couple extra methods like check and uncheck)
        # Go check out UIObject
        #
        # After looking for attributes in the actual class of the object, python looks in the object's parent classes
        # which would be this class (UIBase) and it's parent class UIFactory.

        # So if the attribute is found in any of these places, this __getattr__ will never be called.
        # __getattr__ is only called if an attribute CANNOT be found in any of these places yet.
        #
        # I just wanted to point that out since it's relevant here.


        # secondly, there may be direct attributes on the web_obj attribute of this UIBase object
        # myButton.text, id, tag_name will be handled by the underlying selenium webElement object here...
        try:
            return getattr(self.web_obj, attr)
        except AttributeError:
            pass
        except WebDriverException:
            #try again
            self.log('caught error calling web_obj attribute "%s", sleeping 3s and trying again...' % attr)
            time.sleep(3)
            return getattr(self.web_obj, attr)

        # this is an exception list that we don't want returning UIElements for...
        if attr in ["iterkey", "_getAttributeNames", "trait_names"]:  # ipython...
            raise AttributeError("Attribute not found: %s" % attr)

        # thirdly, we may be doing something like myTable.cell()
        # myTable is a UIObject (inherits from UIBase), and a child element (the cell) would also be a UIObject,
        # so the last thing we do is use the ui_factory to try to find a child web_object and create a UIObject for it...
        #
        # same thing for app.button()
        # app is a MobileApp (also inherits from UIBase), and a child element would be a UIObject

        # now if we say something that's not defined ANY of these places, and is NOT a child element, such as
        # app.jksdfkjhsdf()
        # this call to ui_factory is why we get "undefined element" error.
        return self.ui_factory(attr)

    def __repr__(self):
        # this just defines the string representation of an object of this class
        out = [self.type_name]
        if self.web_obj and hasattr(self.web_obj, 'id'):
            out.append(self.web_obj.id)
        return "<" + " ".join(out) + ">"

    def exists(self, search_term='', element_type=None, partial=False, timeout=0):
        """
        Look for an element, waiting a max of 'timeout' seconds for element JUST TO EXIST (does not have to be visible)
        Returns element if it ever finds it, returns False if not
        """
        try:
            return self.wait_for_element_to_exist(search_term, element_type, partial, timeout)
        except (NoSuchElementException):
            return False

    def exists_on_page(self, search_term='', element_type=None, partial=False, max_scrolls=3):
        return self.find_safe_on_page(search_term, element_type, partial, max_scrolls)

    def has_a(self, element_type):
        """
        :param element_type: button, UIAButton, table, etc.
        :return: True/False
        """
        if(self.find_safe(element_type=element_type)):
            return True
        else:
            return False

    def wait_for_element_to_exist(self, search_term='', element_type=None, partial=False, timeout=10):
        """
        Look for an element, waiting a max of 'timeout' seconds for element JUST TO EXIST
        Returns element if it ever finds it, throws NoSuchElementException if not
        """
        if (type(element_type) == int):
            raise RuntimeError("Err: you called this method with 'element_type=%s' but I think you meant to say 'timeout=%s'" % (element_type,element_type))

        start_time = time.time()

        if (type(search_term) != list):
            search_term = [search_term]
            sleep_time = 0.3
        else:
            sleep_time = 0.0

        while True:
            for temp_search_term in search_term:
                elem = self.find_safe(temp_search_term, element_type, partial)

                if (elem):
                    return elem

            if (time.time() - start_time > timeout):
                raise NoSuchElementException("Element could not be found: search_term=%s, element_type=%s, partial=%s" % (search_term, element_type, partial))
            time.sleep(sleep_time)

    def wait_for_element(self, search_term='', element_type=None, partial=False, timeout=10):
        """
        Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE
        Returns element if it ever finds it, throws NoSuchElementException if not

        This just got more complicated in appium 1.3.4.  Now (in ios at least) the elements off the screen will appear, including those ABOVE
        the element's on screen.  This means we can no longer just get the first element that matches our search and test it for visibility.
        We now have to get ALL matching elements and test EACH for visibility.  Imagine you're looking at a list of elements that all match our
        search and we're scrolled 1/2 way down the list.  Our results could look like
        elem01 (invisible)
        elem02 (invisible)
        elem03 (visible)
        elem04 (visible)
        elem05 (visible)
        elem06 (invisible)

        And we legitimately need to get that elem03 because that's what exists and is visible onscreen now.
        The only solution I can think of is adding a little time if the list of matching elements is really long...
        """
        if (type(element_type) == int):
            raise RuntimeError("Err: you called this method with 'element_type=%s' but I think you meant to say 'timeout=%s'" % (element_type,element_type))

        start_time = time.time()

        if (type(search_term)!=list):
            search_term = [search_term]

        while True:
            for temp_search_term in search_term:
                elems = self.find_all_safe(temp_search_term, element_type, partial)

                #here's my solution for the 1.3.4 upgrade.  We'll add 1 sec of wait time for every 5 elements we have to query for visibility
                added_time_hack = len(elems)/5
                start_time += added_time_hack

                for elem in elems:
                    if (elem and elem.visible):
                        return elem

            if (time.time() - start_time > timeout):
                raise NoSuchElementException("Element could not be found: search_term=%s, element_type=%s, partial=%s" % (temp_search_term, element_type, partial))


    def wait_for_element_safe(self, search_term='', element_type=None, partial=False, timeout=10):
        """
        Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE
        Returns element if it ever finds it, returns False if not
        """
        try:
            return self.wait_for_element(search_term, element_type, partial, timeout)
        except (NoSuchElementException):
            return False

    def exists_and_visible(self, search_term='', element_type=None, partial=False, timeout=0):
        """
        Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE
        Returns element if it ever finds it, returns False if not
        Major difference between this and wait_for_element_safe is the default timeout...
        """
        try:
            return self.wait_for_element(search_term, element_type, partial, timeout)
        except (NoSuchElementException):
            return False

    def exists_and_visible_on_page(self, search_term='', element_type=None, partial=False, max_scrolls=3, timeout=0):
        """
        1.Look for an element, waiting a max of 'timeout' seconds for element to exist AND BE VISIBLE on the current visible screen
        2.Then (after timeout has expired), starts swiping down the page for the element to exist and be visible.  No more waiting.
        Returns element if it ever finds it, returns False if not
        """
        device = self.session.device()
        try:
            # If it exists on the currently visible screen, return whether it is visible or not.
            # This will take care of our timeout as well.
            return self.wait_for_element(search_term, element_type, partial, timeout)
        except (NoSuchElementException):
            pass
        for i in range(max_scrolls):
            elem = self.find_safe(search_term, element_type, partial)
            if elem and elem.visible:
                return elem
            device.swipe(.5, .8, .5, .2, 1)
            time.sleep(0.7)
        return False

    def parent(self):
        """
        works for android 4.4 at least.  don't know about others.
        :return: the parent UIObject of the object you have
        """
        raise RuntimeError('this doesn\t actually work from what i can tell.')
        web_element = self.driver.parent
        return self.ui_factory('normal object', web_element)

    def find_by_resource_id(self, id):
        """
        android only.  this was useful while automating the gmail app.  page_source looked like this:

        LinearLayout [index=1,resource_id=,enabled]
          TextView [long_clickable,clickable,index=0,resource_id=com.google.android.gm:id/send,enabled,focusable]

        so I did a little:
        f.find_by_resource_id('com.google.android.gm:id/send').tap()
        """

        try:
            web_element = self.driver.find_element_by_id(id)
        except NoSuchElementException, e:
            raise NoSuchElementException("%s: %s" % (e, id))
        return self.ui_factory('normal object', web_element)

    @trace
    def find(self, search_term='', element_type=None, partial=False):
        """
        Find a single element by name (i.e. "Log In", "Submit", etc...) or the first to appear in an array if an array is passed in.
        This will find partial strings (i.e. find("Bob", partial=True) will find elements with "Bob" in the name/text)

        :param search_term: String or array of strings to search for (default of '' will match any string)
        :param element_type(optional): The element type to filter on.
        :param partial(optional): Whether to partially match strings. (default=False)
        """
        if (type(search_term) == list):
            return self._find_one_of(search_term, element_type, partial)
        else:
            return self._find(search_term, element_type, partial)

    def _find(self, search_term, element_type, partial):
        """
        does the work for find()
        """
        web_element = self._find_element(search_term=search_term, element_type=element_type, partial=partial)

        if not web_element:
            raise ElementNotFound("Element could not be found: %s" % search_term)

        if (element_type):
            return self.ui_factory(element_type, web_element)
        else:
            return self.ui_factory('normal object', web_element)

    def _find_one_of(self, search_terms, element_type=None, partial=False):
        """
        Wrapper for find() which takes an array of search terms instead of a single one.
        Useful for things that are a little different across android devices such as "Search" vs "Search, or say Google"
        Throws ElementNotFound exception
        :return: the element
        """
        for term in search_terms:
            element = self.find_safe(term, element_type, partial)
            if (element):
                return element

        raise ElementNotFound("in _find_one_of().  no element in our list could be found:%s, %s" % (search_terms, element_type))

    def find_safe(self, search_term='', element_type=None, partial=False):
        """
        Wrapper for find() which returns False instead of throwing an exception (except on "application died" type exception, then we'll just die)
        :return: the element or False
        """
        try:
            return self.find(search_term, element_type, partial)
        except (ElementNotFound, NoSuchElementException, WebDriverException), e:
            if (str(e).find('died') > -1):
                self.log.debug("In find_safe().  caught and dying on exception: %s" % str(e))
                raise e
            else:
                self.log.debug("In find_safe().  caught and swallowed exception: %s" % str(e))
                return False

    def find_on_page(self, search_term='', element_type=None, partial=False, max_scrolls=3):
        """
        Like a normal find but takes optional max_scrolls param (default=5).
        Searches normally, then does a full-page scroll downward and search again, etc...

        See the documentation in wait_for_element() related to appium 1.3.4
        """

        device = self.session.device()

        #do a find first
        elems = self.find_all_safe(search_term, element_type, partial)
        for elem in elems:
            if elem and elem.visible:
                return elem

        #then do our swipes
        for i in range(max_scrolls):
            # Never INCREASE distance of swipe or DECREASE duration here.
            # This has been calibrated and should only ever get MORE conservative.
            device.swipe(.5, .8, .5, .2, 1)
            time.sleep(0.7)

            elems = self.find_all_safe(search_term, element_type, partial)
            for elem in elems:
                if elem and elem.visible:
                    return elem

        raise ElementNotFound("in find_on_page().  element could not be found: %s, %s" % (search_term, element_type))

    def find_safe_on_page(self, search_term='', element_type=None, partial=False, max_scrolls=3):
        """
        Wrapper for find_on_page() which returns False instead of throwing an exception (except on "application died" type exception, then we'll just die)
        :return: the element or False
        """
        try:
            return self.find_on_page(search_term, element_type, partial, max_scrolls)
        except (ElementNotFound, NoSuchElementException, WebDriverException), e:
            if (str(e).find('died') > -1):
                self.log.debug("In find_safe().  caught and dying on exception: %s" % str(e))
                raise e
            else:
                self.log.debug("In find_safe().  caught and swallowed exception: %s" % str(e))
                return False

    def find_on_page_horizontal(self, search_term='', element_type=None, partial=False, max_scrolls=5, direction='right'):
        """
        Like a normal find but takes optional max_scrolls param and direction to search
        Searches normally, then does a bezel swipe to search one direction or another and search again, etc...
        """

        device = self.session.device()

        for i in range(max_scrolls):
            e = self.find_safe(search_term, element_type, partial)
            if e:
                return e

            # Never INCREASE distance of swipe or DECREASE duration here.
            # This has been calibrated and should only ever get MORE conservative.
            if (direction=='right'):
                device.bezel_swipe_right()
            else:
                device.bezel_swipe_left()
            time.sleep(0.7)

        raise ElementNotFound("in find_on_page().  element could not be found: %s, %s" % (search_term, element_type))

    @trace
    def find_all(self, search_term='', element_type=None, partial=False):
        """
        Find elements by name (i.e. "Log In", "Submit", etc...)

        :param search_term: The name to query for.
        """
        if (type(search_term) == list):
            return self._find_one_of_all(search_term, element_type, partial)
        else:
            return self._find_all(search_term, element_type, partial)

    def _find_all(self, search_term='', element_type=None, partial=False):
        """
        Does the work for find_all()
        """
        web_elements = self._find_elements(search_term=search_term, partial=partial, element_type=element_type)

        return [self.ui_factory(element_type or 'normal object', el) for el in web_elements]

    @trace
    def find_all_safe(self, search_term='', element_type=None, partial=False):
        """
        wraps find_all to return False instead of throwing exception on finding 0 elements
        """
        try:
            return self.find_all(search_term, element_type, partial)
        except (ElementNotFound, NoSuchElementException, WebDriverException), e:

            if (str(e).find('died') > -1):
                self.log.debug("In find_all_safe().  caught and dying on exception: %s" % str(e))
                raise e
            else:
                self.log.debug("In find_all_safe().  caught and swallowed exception: %s" % str(e))
                return []

    def _find_one_of_all(self, search_terms, element_type=None, partial=False):
        """
        Wrapper for find_all() which takes an array of search terms instead of a single one.
        Useful for things that are a little different across android devices such as "Search" vs "Search, or say Google"
        Throws ElementNotFound exception
        :return: the element
        """
        for term in search_terms:
            elements = self.find_all_safe(term, element_type, partial)
            if (elements):
                return elements

        raise ElementNotFound("in _find_one_of_all().  no element in our list could be found:%s, %s" % (search_terms, element_type))


    @trace
    def find_by_type(self, element_type):
        """
        Find a single element by type (i.e. UIAButton, UIATextfield, etc...)

        :param element_type: The type of element we're searching for.
        """
        web_element = self._find_element(element_type=element_type)
        if not web_element:
            raise ElementNotFound("Element could not be found for type: %s" % element_type)

        return self.ui_factory(element_type or 'normal object', web_element)

    @trace
    def find_all_by_type(self, element_type):
        """
        Find a elements by type (i.e. UIAButton, UIATextfield, etc...)

        :param element_type: The type of element we're searching for.
        """
        web_elements = self._find_elements(element_type=element_type)
        return [self.ui_factory(element_type or 'normal object', el) for el in web_elements]



#################################################################################
# internal...
#################################################################################
    def _find_element(self, *args, **kwargs):
        #Uses driver.find_elements_by_xpath to find 1 element and returns a selenium web object

        try:
            web_element = self._find_elements(number_elements_to_find=1, *args, **kwargs)
        except AttributeError:
            web_element = []

        return web_element

    def _find_elements(self, search_term=None, partial=False, element_type=None, number_elements_to_find='all'):
        #Uses driver.find_elements_by_xpath to find elements and returns a list of selenium web objects

        kwargs = {'element_type': element_type, 'search_term': search_term, 'partial': partial, 'number_elements_to_find':number_elements_to_find}

        if element_type:
            element_type = self.classmap.map(element_type)

        try:
            if (self.session.platform == 'android'):
                elems = self._find_elements_android(search_term, partial, element_type, number_elements_to_find)
            elif (self.session.platform == 'ios'):
                elems = self._find_elements_ios(search_term, partial, element_type, number_elements_to_find)
            else:
                raise RuntimeError('invalid platform: ' + self.session.platform)

            if (elems):
                return elems
            else:
                raise NoSuchElementException("Element could not be found")

        except (ElementNotFound, NoSuchElementException, WebDriverException), e:
            #create a new exception of the same type we caught but tack on what wer were looking for for loggings sake
            err = str(e).strip('Message: ').strip()
            raise type(e)("%s: %s" % (err, str(kwargs)))

    ###########################
    # note:
    # you will notice that a lot of these calls are the same, especially calls to _find_elements_by_xpath().
    # I encourage you to very serious think about where it's going if you start "simplifying" by combining calls, even though you will be tempted to do so
    # I have tried to make it very explicit as to each of the many cases (combinations of search_term/elem_type/parital/etc.) because it was much more complicated when it was a shorter function

    # for ios, the element attributes are name (accessibility id), value, and label
    #   Typically name == label
    #   But when we have added our acc id, then typically name != label
    #   When a value IS present, typically value == label
    #   But when in some cases (textfields) the value != label

    # for android, the element attributes are content-desc (accessibility id), and text
    #   Typically content-desc != text

    def _find_elements_ios(self, search_term, partial, element_type, number_elements_to_find):
        kwargs = {'element_type': element_type, 'search_term': search_term, 'partial': partial, 'number_elements_to_find':number_elements_to_find}
        self.log.info("_find_elements_ios: %s" % str(kwargs))

        # find EVERYTHING
        # here's our little unit test: open Nike Soccer, log in, go to a crew, pull to show compose message box, use the simulator keyboard to enter 887766, then click so the cursor is at the front of the "887766"
        # then run the following:
        #   self.app._find_elements_ios('', False, None, 1).tag_name                  #by xpath
        #   self.app._find_elements_ios('', False, None, 'all')[0].tag_name           #by xpath
        #     self.app.find('', partial=False, element_type=None).tag_name
        #     self.app.find_all('', partial=False, element_type=None)[0].tag_name
        if (not search_term and not element_type):
            xpath = "//*"
            if (number_elements_to_find=='all'):
                return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
            else:
                elems = self.driver.find_elements_by_xpath(xpath)
                return elems[0]

        # only element type (class).  For example when user calls app.button()
        #    self.app._find_elements_ios('', True, 'UIAButton', 1).text                 #by class_name
        #    self.app._find_elements_ios('', True, 'UIAButton', 'all')[0].text          #by class_name
        #     self.app.find('', partial=True, element_type='button').text
        #     self.app.find_all('', partial=True, element_type='button')[0].text
        elif (element_type and not search_term):
            if (number_elements_to_find=='all'):
                return self.driver.find_elements_by_class_name(element_type)
            else:
                return self.driver.find_element_by_class_name(element_type)

        # only search term (name/text)
        #   self.app._find_elements_ios('nav_profile_button', False, None, 1).text               #by name, exact, 1
        #   self.app._find_elements_ios('nav_profile_button', False, None, 'all')[0].text        #by name, exact, 'all'
        #   self.app._find_elements_ios('navmenu image default', False, None, 1).text            #by label, exact, 1
        #   self.app._find_elements_ios('navmenu image default', False, None, 'all')[0].text     #by label, exact, 'all'
        #   self.app._find_elements_ios('887766', False, None, 1).text                           #by value, exact, 1
        #   self.app._find_elements_ios('887766', False, None, 'all')[0].text                    #by value, exact, 'all'
        #
        #   self.app._find_elements_ios('nav_profile_but', True, None, 1).text                   #by xpath @name, partial, 1
        #   self.app._find_elements_ios('nav_profile_but', True, None, 'all')[0].text            #by xpath @name, partial, 'all'
        #   self.app._find_elements_ios('navmenu image', True, None, 1).text                     #by xpath @label, partial, 1
        #   self.app._find_elements_ios('navmenu image', True, None, 'all')[0].text              #by xpath @label, partial, 'all'
        #   self.app._find_elements_ios('8877', True, None, 1).text                              #by xpath @value, partial, 1
        #   self.app._find_elements_ios('8877', True, None, 'all')[0].text                       #by xpath @value, partial, 'all'

        #     self.app.find('nav_profile_button', partial=False, element_type=None).text
        #     self.app.find_all('nav_profile_button', partial=False, element_type=None)[0].text
        #     self.app.find('navmenu image default', partial=False, element_type=None).text
        #     self.app.find_all('navmenu image default', partial=False, element_type=None)[0].text
        #     self.app.find('887766', partial=False, element_type=None).text
        #     self.app.find_all('887766', partial=False, element_type=None)[0].text
        #
        #     self.app.find('nav_profile_but', partial=True, element_type=None).text
        #     self.app.find_all('nav_profile_but', partial=True, element_type=None)[0].text
        #     self.app.find('navmenu image', partial=True, element_type=None).text
        #     self.app.find_all('navmenu image', partial=True, element_type=None)[0].text
        #     self.app.find('8877', partial=True, element_type=None).text
        #     self.app.find_all('8877', partial=True, element_type=None)[0].text
        elif (search_term and not element_type):
            if partial:
                #first look for acc ids (name), then try text
                try:
                    xpath = "//*[contains(@name, \"%s\")]" % search_term
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    pass
                try:
                    xpath = "//*[contains(@label, \"%s\")]" % search_term
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    pass
                #leave the last one out of try/except
                xpath = "//*[contains(@value, \"%s\")]" % search_term
                return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)

            else:
                if (number_elements_to_find=='all'):
                    #1.from what I can tell, find_element_by_accessibility_id is the same as find_element_by_name (which is now deprecated)
                    #2.we're not using find_elements_by_id because it will match partial matches
                    #3.find_element_by_accessibility_id matches "name" and "label" in page source but not "value" so we'll have to fail over to find the "value" tags
                    elems = self.driver.find_elements_by_accessibility_id(search_term)
                    if (elems != []):
                        return elems
                    else:
                        xpath = "//*[@value=\"%s\"]" % search_term
                        return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)

                else:
                    try:
                        return self.driver.find_element_by_accessibility_id(search_term)
                    except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                        xpath = "//*[@value=\"%s\"]" % search_term
                        return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)



        # search term (name/text) AND element_type (class)

        # here's our little unit test: open Nike Soccer, log in, go to a crew, pull to show compose message box, use the simulator keyboard to enter 887766, then click so the cursor is at the front of the "887766"
        # then run the following:
        #   self.app._find_elements_ios('nav_profile_button', False, 'UIAButton', 1).text               #by name, exact, 1
        #   self.app._find_elements_ios('nav_profile_button', False, 'UIAButton', 'all')[0].text        #by name, exact, 'all'
        #   self.app._find_elements_ios('navmenu image default', False, 'UIAButton', 1).text            #by label, exact, 1
        #   self.app._find_elements_ios('navmenu image default', False, 'UIAButton', 'all')[0].text     #by label, exact, 'all'
        #   self.app._find_elements_ios('887766', False, 'UIATextView', 1).text                         #by value, exact, 1
        #   self.app._find_elements_ios('887766', False, 'UIATextView', 'all')[0].text                  #by value, exact, 'all'
        #
        #   self.app._find_elements_ios('nav_profile_but', True, 'UIAButton', 1).text                   #by xpath @name, partial, 1
        #   self.app._find_elements_ios('nav_profile_but', True, 'UIAButton', 'all')[0].text            #by xpath @name, partial, 'all'
        #   self.app._find_elements_ios('navmenu image', True, 'UIAButton', 1).text                     #by xpath @label, partial, 1
        #   self.app._find_elements_ios('navmenu image', True, 'UIAButton', 'all')[0].text              #by xpath @label, partial, 'all'
        #   self.app._find_elements_ios('8877', True, 'UIATextView', 1).text                            #by xpath @value, partial, 1
        #   self.app._find_elements_ios('8877', True, 'UIATextView', 'all')[0].text                     #by xpath @value, partial, 'all'

        #     self.app.find('nav_profile_button', partial=False, element_type='button').text
        #     self.app.find_all('nav_profile_button', partial=False, element_type='button')[0].text
        #     self.app.find('navmenu image default', partial=False, element_type='button').text
        #     self.app.find_all('navmenu image default', partial=False, element_type='button')[0].text
        #     self.app.find('887766', partial=False, element_type='textview').text
        #     self.app.find_all('887766', partial=False, element_type='textview')[0].text
        #
        #     self.app.find('nav_profile_but', partial=True, element_type='button').text
        #     self.app.find_all('nav_profile_but', partial=True, element_type='button')[0].text
        #     self.app.find('navmenu image', partial=True, element_type='button').text
        #     self.app.find_all('navmenu image', partial=True, element_type='button')[0].text
        #     self.app.find('8877', partial=True, element_type='textview').text
        #     self.app.find_all('8877', partial=True, element_type='textview')[0].text
        else:
            if partial:
                #first look for acc ids, then try text, then value
                try:
                    xpath = "//%s[contains(@name, \"%s\")]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    pass
                try:
                    xpath = "//%s[contains(@label, \"%s\")]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    pass
                #leave the last one out of try/except
                xpath = "//%s[contains(@value, \"%s\")]" % (element_type, search_term)
                return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)

            else:
                #first look for acc ids, then try text, then value
                try:
                    xpath = "//%s[@name=\"%s\"]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    pass
                try:
                    xpath = "//%s[@label=\"%s\"]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    pass
                #leave the last one out of try/except
                xpath = "//%s[@value=\"%s\"]" % (element_type, search_term)
                return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)


    def _find_elements_android(self, search_term, partial, element_type, number_elements_to_find):
        kwargs = {'element_type': element_type, 'search_term': search_term, 'partial': partial,'number_elements_to_find': number_elements_to_find}
        self.log.info("_find_elements_android: %s" % str(kwargs))

        # find EVERYTHING
        # "unit tests" are for Nike app, login page
        #    self.app._find_elements_android('', False, None, 1).id               #by xpath
        #    self.app._find_elements_android('', False, None, 'all')[0].id        #by xpath
        #     self.find('', partial=False, element_type=None).id
        #     self.find_all('', partial=False, element_type=None)[0].id
        if (not search_term and not element_type):
            xpath = "//*"
            if (number_elements_to_find == 'all'):
                elems = self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                return elems
            else:
                elems = self.driver.find_elements_by_xpath(xpath)
                return elems[0]

        # only element type.  happens when user calls app.button()
        #    self.app._find_elements_android('', True, 'android.widget.Button', 1).text                  #by class_name
        #    self.app._find_elements_android('', True, 'android.widget.Button', 'all')[0].text           #by class_name
        #     self.find('', partial=True, element_type='button').text
        #     self.find_all('', partial=True, element_type='button')[0].text
        elif (element_type and not search_term):
            if (number_elements_to_find == 'all'):
                return self.driver.find_elements_by_class_name(element_type)
            else:
                return self.driver.find_element_by_class_name(element_type)

        # only search term (name/text)
        #    self.app._find_elements_android('Sign In', False, None, 1).text                            #by name
        #    self.app._find_elements_android('Sign In', False, None, 'all')[0].text                     #by name
        #    self.app._find_elements_android('splash_sign_button', False, None, 1).text                 #by name
        #    self.app._find_elements_android('splash_sign_button', False, None, 'all')[0].text          #by name
        #    self.app._find_elements_android('Sign', True, None, 1).text                                #by xpath @label
        #    self.app._find_elements_android('Sign', True, None, 'all')[0].text                         #by xpath @label
        #    self.app._find_elements_android('splash_sign', True, None, 1).text                         #by xpath @name fails.  android limitation
        #    self.app._find_elements_android('splash_sign', True, None, 'all')[0].text                  #by xpath @name fails.  android limitation
        #     self.find('Sign In', partial=False, element_type=None).text
        #     self.find_all('Sign In', partial=False, element_type=None)[0].text
        #     self.find('splash_sign_button', partial=False, element_type=None).text
        #     self.find_all('splash_sign_button', partial=False, element_type=None)[0].text
        #     self.find('Sign', partial=True, element_type=None).text
        #     self.find_all('Sign', partial=True, element_type=None)[0].text
        #     self.find('splash_sign', partial=True, element_type=None).text
        #     self.find_all('splash_sign', partial=True, element_type=None)[0].text
        elif (search_term and not element_type):  # only search term
            if partial:
                #first look for acc ids (name), then try text
                try:
                    xpath = "//*[contains(@content-desc, \"%s\")]" % search_term
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    xpath = "//*[contains(@text, \"%s\")]" % search_term
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)

            else:
                if (number_elements_to_find == 'all'):
                    #1.find_element_by_name matches on both "content-desc" and "text" but is now deprecated
                    #2.find_element_by_accessibility_id only matches on "content-desc" but not "text" so we have to fail over and find by xpath
                    elems = self.driver.find_elements_by_accessibility_id(search_term)
                    if (elems != []):
                        return elems
                    else:
                        xpath = "//*[@text=\"%s\"]" % (search_term)
                        return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                else:
                    try:
                        return self.driver.find_element_by_accessibility_id(search_term)
                    except  (ElementNotFound, NoSuchElementException, WebDriverException), e:
                        pass
                    xpath = "//*[@text=\"%s\"]" % (search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)

        # search term (name/text) and element_type (class)
        #    self.app._find_elements_android('Sign In', False, 'android.widget.Button', 1).text                          #by xpath
        #    self.app._find_elements_android('Sign In', False, 'android.widget.Button', 'all')[0].text                   #by xpath
        #    self.app._find_elements_android('splash_sign_button', False, 'android.widget.Button', 1).text               #by xpath
        #    self.app._find_elements_android('splash_sign_button', False, 'android.widget.Button', 'all')[0].text        #by xpath
        #    self.app._find_elements_android('Sign', True, 'android.widget.Button', 1).text                              #by xpath
        #    self.app._find_elements_android('Sign', True, 'android.widget.Button', 'all')[0].text                       #by xpath
        #    self.app._find_elements_android('splash_sign', True, 'android.widget.Button', 1).text                       #by xpath
        #    self.app._find_elements_android('splash_sign', True, 'android.widget.Button', 'all')[0].text                #by xpath
        #     self.find('Sign In', partial=False, element_type='button').text
        #     self.find_all('Sign In', partial=False, element_type='button')[0].text
        #     self.find('splash_sign_button', partial=False, element_type='button').text
        #     self.find_all('splash_sign_button', partial=False, element_type='button')[0].text
        #     self.find('Sign', partial=True, element_type='button').text
        #     self.find_all('Sign', partial=True, element_type='button')[0].text
        #     self.find('splash_sign', partial=True, element_type='button').text
        #     self.find_all('splash_sign', partial=True, element_type='button')[0].text
        else:
            if partial:
                #first look for acc ids, then try text
                try:
                    xpath = "//%s[contains(@content-desc, \"%s\")]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    xpath = "//%s[contains(@text, \"%s\")]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
            else:
                #first look for acc ids, then try text
                try:
                    xpath = "//%s[@content-desc=\"%s\"]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)
                except (ElementNotFound, NoSuchElementException, WebDriverException), e:
                    xpath = "//%s[@text=\"%s\"]" % (element_type, search_term)
                    return self._find_elements_by_xpath(xpath, number_elements_to_find, kwargs)


    def _find_elements_by_xpath(self, xpath, number_elements_to_find, kwargs):
        self.log.info("xpath=" + xpath)

        if (number_elements_to_find==1):
            return self.driver.find_element_by_xpath(xpath)
        else:
            # this is strange:
            # driver.find_ELEMENT_by_xpath() will throw an exception if nothing found
            # driver.find_ELEMENTS_by_xpath() will return an empty array
            # I don't like that.  We'll make ...ELEMENTS also throw an exception for parallel behavior.
            elems = self.driver.find_elements_by_xpath(xpath)
            if (elems==[]):
                # kwargs is here for documentation.  it's easier to read than the xpath and should be more useful to the script writer
                raise ElementNotFound("in _find_elements_by_xpath().  Could not find: %s" % kwargs)
            return elems


class UIObject(UIBase):
    """
    These are the objects the user will deal with, examples are tables, staticTexts, etc.
    'attributes' param is for special UIObjects such as UITextFields, which have 'text' and 'send_keys' attributes
    """
    def __init__(self, session, web_obj=None, attributes=[]):
        super(UIObject, self).__init__(session, web_obj, attributes)

    # some of the attributes here are actually attributes of our selenium web_obj, and some are kind of
    # hidden by the web_obj and for some reason we have to call web_obj.get_web_obj_attribute to get them.
    # Not sure why they're not plain ol' attributes of that class.
    @property
    def name(self):
        return self.web_obj.get_web_obj_attribute('name')

    @property
    def value(self):
        return self.web_obj.get_web_obj_attribute('value')

    @property
    def label(self):
        return self.web_obj.get_web_obj_attribute('label')

    @property
    def tag_name(self):
        return self.web_obj.tag_name

    @property
    def visible(self):
        return self.web_obj.is_displayed()

    @property
    def enabled(self):
        return self.web_obj.is_enabled()

    @property
    def selected(self):
        return self.web_obj.is_selected()

    @property
    def parent(self):
        """
        Returns the webDRIVER for the whole app, not the parent webELEMENT.
        Not sure if this will ever be useful because we always have access to the webDriver object through Flow.driver
        """
        return self.web_obj.parent

    def tap(self, x=.5, y=.5, duration=0.1, count=1):
        """
        Used indirectly when you do flow.tap('my label')
        Used directly when you do flow.button().tap()
        """
        self.log.debug("tapping with parameters: x=%s, y=%s, duration=%s, count=%s" % (x, y, duration, count))

        #if all our parameters are our defaults, just use normal click (it's faster)
        if (x==.5 and y==.5 and duration==0.1 and count==1):
            self.log.debug('simple web_obj.click()')
            self.web_obj.click()
        else:
            self.tap_complex(x=x, y=y, duration=duration, count=count)

    def tap_complex(self, x, y, duration, count):
        #now using TouchActions, duration is in ms, so multiply by 1000
        duration = duration * 1000
        if (x != .5 or y != .5):
            raise RuntimeError('not yet impl')

        ta = TouchAction(self.session.driver)

        # to impl:
        # ta.tap(self.web_obj, x=x, y=y, count=count).perform()
        # but take into account that it wants pixels, not %s

        if (count > 1):
            return ta.tap(self.web_obj, count=count).perform()
        else:
            return ta.press(self.web_obj).wait(duration).release().perform()



    def tap_safe(self, x=0.5, y=0.5, duration=0.1, count=1):
        """
        Used directly when you do flow.button().tap_safe()
        """
        try:
            self.tap(x=x, y=y, duration=duration, count=count)
        except (ElementNotFound, NoSuchElementException, WebDriverException), e:
            if (str(e).find('died') > -1):
                self.log.debug("In tap_safe().  caught and dying on exception: %s" % str(e))
                raise e
            else:
                self.log.debug("In tap_safe().  caught and swallowed exception: %s" % str(e))
                return False

    def tap_by_location(self, duration=0.1, count=1, xoffset=0, yoffset=0):
        """
        Tap an element that exists but is not visible.  This is a workaround for an ios bug in which
        we can see the element on the screen but tapping throws a WebDriverException: Message: u'An unknown server-side error occurred while processing the command.'

        :xoffset: If you want to tap something NEAR what we're tapping, use x/y offset.  can be > or < 0.  defaults to 0
        :yoffset: If you want to tap something NEAR what we're tapping, use x/y offset.  can be > or < 0.  defaults to 0

        :param timeout: Optional (default=3 sec), tries to tap for up to 'wait' seconds before failing.
        """
        loc = self.location
        x, y = loc['x'], loc['y']
        size = self.size
        h, w = size['height'], size['width']

        x = x + w / 2 + xoffset
        y = y + h / 2 + yoffset

        self.session.device().tap(x=x, y=y, duration=duration, count=count)


    @trace
    def swipe_up(self, duration=.5):
        """
        Short hand for :py:meth:`swipe` going from bottom center, to top center of the element.
        """
        self.log.debug("UIObject swipe_up")
        self.session.device().swipe(0.5, 0.9, 0.5, 0.1, duration, self)

    @trace
    def swipe_down(self, duration=.5):
        """
        Short hand for :py:meth:`swipe` going from top center, to bottom center of the element.
        """
        self.log.debug("UIObject swipe_down")
        self.session.device().swipe(0.5, 0.1, 0.5, 0.9, duration, self)

    @trace
    def swipe_right(self, duration=.5):
        """
        Short hand for :py:meth:`swipe` going from left center, to right center of the element.
        """
        self.log.debug("UIObject swipe_right")
        self.session.device().swipe(0.1, 0.5, 0.9, 0.5, duration, self)

    @trace
    def swipe_left(self, duration=.5):
        """
        Short hand for :py:meth:`swipe` going from right center, to left center of the element.
        """
        self.log.debug("UIObject swipe_left")
        self.session.device().swipe(0.9, 0.5, 0.1, 0.5, duration, self)

    @trace
    def flick(self, startx=0.5, starty=0.5, endx=0.5, endy=0.5, fingers=1):
        """
        Flick the element.
        """
        self.log.debug('UIObject: flick %d %d %d %d %d' % (startx, starty, endx, endy, fingers))
        self.session.driver.execute_script("mobile: flick", {
            "touchCount": fingers,
            "startX": startx,
            "startY": starty,
            "endX": endx,
            "endY": endy,
            "element": self.web_obj.id
        })

    @trace
    def flick_up(self):
        """
        Short hand for :py:meth:`flick` up.
        """
        self.log.debug('UIObject: flick_up')
        self.flick(starty=0.1, endy=0.9)

    @trace
    def flick_down(self):
        """
        Short hand for :py:meth:`flick` down by 200 pixels.
        """
        self.log.debug('UIObject: flick_down')
        self.flick(starty=0.9, endy=0.1)

    @trace
    def flick_right(self):
        """
        Short hand for :py:meth:`flick` right by 200 pixels.
        """
        self.log.debug('UIObject: flick_right')
        self.flick(startx=0.1, endx=0.9)

    @trace
    def flick_left(self):
        """
        Short hand for :py:meth:`flick` left by 200 pixels.
        """
        self.log.debug('UIObject: flick_left')
        self.flick(startx=0.9, endx=0.1)

    def checked(self):
        self.log.debug('UICheckBox.checked')
        return self.web_obj.get_web_obj_attribute('checked') == 'true'

    def check(self):
        self.log.debug('UICheckBox.check')
        if not self.checked():
            self.web_obj.click()

    select = check


class UIAlert(UIBase):
    def __init__(self, session, web_obj=None):
        super(UIAlert, self).__init__(
            session, session.driver.switch_to_alert(),
            ['accept', 'dismiss', 'send_keys', 'text'])

    def exists(self):
        self.log.debug('UIAlert.exists')
        return self.web_obj is not None


class UISearchBar(UIObject):
    def __init__(self, session, web_obj=None):
        super(UISearchBar, self).__init__(
            session, web_obj, ['send_keys', 'text'])

    def search_for(self, text):
        self.log.debug('UISearchBar.search_for: %s' % text)
        self.send_keys(text)
        keyboard = self.session.app().keyboard()
        keyboard.button("Search").tap()


class UITextField(UIObject):
    def __init__(self, session, web_obj=None):
        super(UITextField, self).__init__(
            session, web_obj, ['send_keys', 'text'])


class UISwitch(UIObject):
    def __init__(self, session, web_obj=None):
        super(UISwitch, self).__init__(session, web_obj)

    def toggle(self):
        self.log.debug('UISwitch.toggle')
        self.web_obj.click()


class UICheckBox(UISwitch):
    def __init__(self, session, web_obj=None):
        super(UICheckBox, self).__init__(session, web_obj)

    def checked(self):
        self.log.debug('UICheckBox.checked')
        return self.web_obj.get_web_obj_attribute('checked') == 'true'

    def check(self):
        self.log.debug('UICheckBox.check')
        if not self.checked():
            self.web_obj.click()

    def uncheck(self):
        self.log.debug('UICheckBox.uncheck')
        if self.checked():
            self.web_obj.click()


class UIContainer(UIObject):
    """
    A UIObject that necessarily contains children.  Examples would be a table, a radioGroup.
    I'm not really sure what advantage this construct has since all elements can have children.
    """
    def __init__(self, session, web_obj=None, child_elem_type=''):
        super(UIContainer, self).__init__(session, web_obj, ['children'])
        self.child_elem_type = child_elem_type
        self._children = []

    def children(self, elem_type=None):
        """
        Return the children of a UIContainer.  if 'elem_type' is specified, only return those children
        """
        self._refresh_children()
        if elem_type:
            rv = self._find_elements(element_type=self.child_elem_type, search_term=elem_type, partial=True)
            rv = [self.ui_factory(self.child_elem_type, x) for x in rv]
            if isinstance(rv, list) and len(rv) == 1:
                return rv[0]
            else:
                return rv
        return self._children

    def tap(self, index=None):
        self._refresh_chilren()

        if index is None:
            super(UIList, self).tap()
        else:
            if index < len(self._children):
                self._children[index].click()

    def _refresh_children(self):
        if not self._children:
            self._children = self.find_all_by_type(self.child_elem_type)

    def __len__(self):
        self._refresh_children()

        return len(self._children)

    def __getitem__(self, key):
        """
        Notation for __getitem__ is myObj[key]
        Can be used to get a UIObject's child based on the key passed in.  key can be:
        an int   - myObj[3] acts like list index
        a string - myObj['some text'] returns first child with text == 'some text'
        a slice  - myObj[slice(2,4)] returns a list of items
        """
        self._refresh_children()

        if isinstance(key, (str, unicode)):
            for child in self._children:
                if child.text == key:
                    return child
        if isinstance(key, slice):
            return [self._children[x] for x in xrange(*key.indices(len(self._children)))]
        return self._children[key]


class UITableGroup(UIContainer):
    pass


class UISegmentedControl(UIContainer):
    def __init__(self, session, web_obj=None):
        child_elem_type = 'button'
        super(UISegmentedControl, self).__init__(session, web_obj, child_elem_type=child_elem_type)


class UIRadioButton(UIObject):
    def __init__(self, session, web_obj=None):
        super(UIRadioButton, self).__init__(session, web_obj)

    def checked(self):
        self.log.debug('UICheckBox.checked')
        return self.web_obj.get_web_obj_attribute('checked') == 'true'

    selected = checked

    def check(self):
        self.log.debug('UICheckBox.check')
        if not self.checked():
            self.web_obj.click()

    select = check


class UIRadioGroup(UIContainer):
    def __init__(self, session, web_obj=None):
        child_elem_type = 'radioButton' if session.platform == 'android' else 'tableCell'
        super(UIRadioGroup, self).__init__(session, web_obj, child_elem_type=child_elem_type)

class UIList(UIContainer):
    def __init__(self, session, web_obj=None):
        if session.platform == 'android':
            child_elem_type = 'textView'
        else:
            child_elem_type = 'tableCell'
        super(UIList, self).__init__(session, web_obj, child_elem_type=child_elem_type)

    def scroll_to(self, item):
        """
        scrolls to an element based on key passed in.
        If android, key must be text (searches by name and text)
        If ios, key can be a UIObject (such as tableCell) or text (searches by name and text)
        """
        text = None
        if isinstance(item, (str, unicode)):
            text = item

        if self.session.platform == 'android':
            if not text:
                raise InvalidSearchParameters("For android, scroll_to requires a string to match against the elements name or text")
            args = {'element': self.id, 'text': text}
        else:
            if text:
                item = self.find(text)
            args = {'element': item.id}
        self.session.driver.execute_script("mobile: scrollTo", args)
