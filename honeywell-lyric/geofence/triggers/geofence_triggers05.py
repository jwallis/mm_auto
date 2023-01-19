################################################################################
#
# NAME: geofence_triggers05 - one user: leave geofence, recenter to where we are, verify we are home
# ID: 103425
# DESCRIPTION: one user: leave geofence, recenter to where we are, recieve notif and verify we are home
#
################################################################################
from common import *

def run_test(flow, device, data):
    #android: works on Lyric Relaunch build from 30 Mar 2015, 16:03 on "last_couple_changes" branch commit 447035a1f0501bb566ffda619842ec5a35fd1ea4 with hack: verify_notification() simply returns True

    #flow.login_and_logout(data.user03, set_loc=data.geo_loc03a)

    flow.login(data.user02, show_geofence_alerts=True)
    flow.get_api().set_default_setpoints()

    flow.set_geofence(data.geofence01a, data.user02.loc01)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='?'), "should have seen arrive via fencecrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"
    flow.goto_home()

    flow.set_geofence(data.geofence03a, data.user02.loc01)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='?'), "should have seen arrived via fencecrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"
    flow.goto_home()

    flow.set_geo_location(data.geo_loc01a)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"

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
