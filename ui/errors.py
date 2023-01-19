class NotInitialized(Exception):
    """ Requested an attribute on an object that is not initialized """
    pass

class ElementNotFound(Exception):
    """ If no element was returned from UIObject.find. """
    pass

class InvalidSearchParameters(Exception):
    """ Unable to search for an element based on the search parameters """
    pass


# This should be the only reference to selenium we make.  Should only be referencing Appium any other place.
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
