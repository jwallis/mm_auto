# This file will hold all external dependencies
# This file must be imported by all "library function" files (login, navigation, etc)
# So if you think your "library function" file needs an external class, stick it here to save time...

import mats

#mats library
#we can import these into our namespace for easy access because things like "WebDriverException" and "AttrDict" probably aren't found in multiple libraries.  Use your judgement
from mats.appium.ui.errors import ElementNotFound, NoSuchElementException, WebDriverException
from mats.errors import FrameworkError
from mats.thirdparty import AttrDict

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

#sys library
#we maybe should keep these in their respective namespaces because really generic methods like "sleep" or "date" may appear in several libraries.  Use your judgement
import datetime
import logging
import random
import time
import re #regexp
import os
import inspect