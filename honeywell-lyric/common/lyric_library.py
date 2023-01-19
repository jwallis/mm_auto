from generic_flow import *

class commonFlow(object):
    def busy_wait_until_visible(self, element, attempts=3, partial=False):
        '''
        Checks if the element exists and is visible, if not,
        it will busy wait incrementally and check again until the number of attempts reaches 0.
        '''
        assert attempts > 0
        if(attempts > 20):
            attempts = 20

        first = 0
        second = 1
        tmp = 0
        for i in range(0, attempts):
            if(attempts <= 0) or (self.exists_and_visible_on_page(element), partial):
                break
            tmp = first + second
            first = second
            second = tmp
            self.sleep(second)

            attempts = attempts - 1
