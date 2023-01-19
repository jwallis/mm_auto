################################################################################
#
# NAME: geofence_triggers06 - one user: modify geofence size so that we effectively cross it
# ID: 39580 39581 39582 39585 39586 39587
# DESCRIPTION: set fence, depart, increase radius so that we arrive, verify it, decrease so we depart, verify it
#
################################################################################
from common import *


def run_test(flow, device, data):

    flow.blocked_on_ios('changing radius so that we cross not yet implemented on ios')

    flow.login(data.user02, show_geofence_alerts=True)

    # go home
    flow.set_geofence(data.geofence01c, data.user02.loc01, recenter=True)
    flow.goto_home()
    assert (flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT")

    # depart geofence
    flow.set_geo_location(data.geo_loc02a)
    assert (flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen 'departed via fenceCrossed' notification but did NOT")
    assert (flow.verify_loc('away'), "We should be AWAY but we are NOT")

    # increase geofence size so that we're now inside fence
    flow.set_geofence(data.geofence01c, data.user02.loc01, recenter=False)
    assert (flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='occupied'), "should have seen 'arrived via fencecrossed' notification but did NOT")
    flow.goto_home()
    assert (flow.verify_loc('home'), "We should be HOME but we are NOT")

    # decrease geofence size so that we're now outside fence
    flow.set_geofence(data.geofence01a, data.user02.loc01, recenter=False)
    assert (flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen 'departed via fencecrossed' notification but did NOT")
    assert (flow.verify_loc('away'), "We should be AWAY but we are NOT")

try:
    flow, device, data = get_flow()
    flow.hw_lyric_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    # make sure everything's in a try block so the original exception will not be hidden by any exceptions here
    try:
        flow.hw_lyric_teardown()
    except:
        pass
