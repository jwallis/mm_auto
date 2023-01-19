################################################################################
#
# NAME: thermostat01 - change stat mode heat/cool/off and verify
# ID: 40383 40384 40408
# DESCRIPTION: change stat mode heat/cool/off and verify settings changed in CHAPI
#
################################################################################
from common import *


def run_test(flow, device, data):

    api = flow.get_api()

    flow.login(data.user02)

    flow.set_heat_cool('heat')
    assert (api.verify_heat_cool('heat')), 'Failed TC 40383: we set it to heat but it is NOT set to heat'

    flow.set_heat_cool('off')
    assert (api.verify_heat_cool('off')), 'Failed TC 40408: we set it to off but it is NOT set to off'

    flow.set_heat_cool('cool')
    assert (api.verify_heat_cool('cool')), 'Failed TC 40384: we set it to cool but it is NOT set to cool'

try:
    flow, device, data=get_flow()
    flow.hw_lyric_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    # make sure everything's in a try block so the original exception will not be hidden by any exceptions here
    try:
        flow.hw_lyric_teardown()
    except:
        pass
