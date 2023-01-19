################################################################################
#
# NAME: geofence_triggers11 - one user: put app in background, cross fence, foreground, see notif and updated setpoint
# ID: 39558 39559
# DESCRIPTION: one user: put app in background, depart the geofence, foreground app, see departed notif and AWAY setpoint, repeat for arriving
#
################################################################################
from common import *

def run_test(flow, device, data):
    #android: works on Lyric Relaunch build from 30 Mar 2015, 16:03 on "last_couple_changes" branch commit 447035a1f0501bb566ffda619842ec5a35fd1ea4 with hack: verify_notification() simply returns True

    #flow.login_and_logout(data.user03, set_loc=data.geo_loc03a)

    flow.login(data.user02, show_geofence_alerts=True)
    flow.get_api().set_default_setpoints()

    #set geofence to known state
    flow.set_geofence(data.geofence01a, data.user02.loc01)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='?'), "should have seen arrive via fencecrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"
    flow.goto_home()

    #go to homescreen, set current location to AWAY
    flow.device.home()
    flow.sleep(2)
    flow.set_geo_location(data.geo_loc03a, switch_back=False)

    #verify we got departed trigger
    if (flow.android):
        assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    else:
        assert flow.verify_push_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    flow.switch_apps()
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()

    #go to homescreen, set current location to HOME
    flow.device.home()
    flow.sleep(2)
    flow.set_geo_location(data.geo_loc01a, switch_back=False)

    #verify we got arrived trigger
    if (flow.android):
        assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='occupied'), "should have seen arrived via fenceCrossed notif but did NOT"
    else:
        assert flow.verify_push_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='occupied'), "should have seen arrived via fenceCrossed notif but did NOT"
    flow.switch_apps()
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
