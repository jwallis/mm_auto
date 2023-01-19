################################################################################
#
# NAME: geofence_triggers02 - two users: one stays inside geofence while other crosses
# ID: 39632 39636
# DESCRIPTION: two users: one user inside fence, other user arrives and departs, should have no effect
#
################################################################################
from common import *

def run_test(flow, device, data):
    flow.blocked("2-user tests no good right now.")
    flow.login(data.user03)

    flow.set_geo_location(data.geo_loc01a)
    flow.sleep(5)           # make sure the location change sets in
    flow.device.reset()     # destroy session with user still logged in

    flow.login(data.user02, show_geofence_alerts=True)
    flow.get_api().set_default_setpoints()
    flow.set_geofence(data.geofence01a)
    flow.goto_home()

    # move away, but user03 still home, stat should still be set to home
    flow.set_geo_location(data.geo_loc03a)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01 , action='departed', result='nosignificance'), "should have seen departed via fenceCrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()

    flow.set_geo_location(data.geo_loc01a)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01 , action='arrived', result='nosignificance'), "should have seen arrived via fenceCrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"

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
