################################################################################
#
# NAME: test android fun funcs
# ID: 00000
# DESCRIPTION: test wi-fi, airplane, app_switch, force_quit, launch
#
################################################################################
from common import *

def run_test(flow, device, data):

    #
    flow.set_airplane_mode('on')
    flow.button("OK").tap()
    assert (flow.exists(flow.strings.NO_CONNECTION_AVAILABLE)), 'airplane on. no connection msg SHOULD exist but DOES NOT'

    flow.set_airplane_mode('off')
    assert (not flow.exists(flow.strings.NO_CONNECTION_AVAILABLE)), 'airplane off. no connection msg should NOT EXIST but DOES'

    flow.set_wifi_mode('off')
    assert (flow.exists(flow.strings.NO_CONNECTION_AVAILABLE)), 'wifi off. no connection msg SHOULD exist but DOES NOT'

    flow.set_wifi_mode('on')
    assert (not flow.exists(flow.strings.NO_CONNECTION_AVAILABLE)), 'wifi on. no connection msg should NOT EXIST but DOES'

    flow.force_quit()
    flow.launch_app()
    assert flow.is_app_running(), 'app should be running but is NOT'


try:
    flow, device, data=get_flow()
    flow.nike_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    # make sure everything's in a try block so the original exception will not be hidden by any exceptions in this section...
    try:
        flow.nike_teardown()
    except:
        pass
