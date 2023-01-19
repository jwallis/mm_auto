################################################################################
#
# NAME: side_drawer01 - open side drawer, view First/Last name
# ID: 43692
# DESCRIPTION: open side drawer, view First/Last name
#
################################################################################

from common import *

def run_test(flow, device, data):
    flow.login(data.user02)

    flow.open_side_drawer()
    assert flow.is_side_drawer_visible(), "side drawer should be OPEN but is NOT"
    flow.close_side_drawer()
    assert (not flow.is_side_drawer_visible()), "side drawer should be CLOSED but is NOT"

try:
    flow, device, data=get_flow()
    flow.hw_lyric_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    # make sure everything's in a try block so the original exception will not be hidden by any exceptions in this section...
    try:
        flow.hw_lyric_teardown()
    except:
        pass