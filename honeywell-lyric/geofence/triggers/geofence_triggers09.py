################################################################################
#
# NAME: geofence_triggers09 - one user: force close, cross geofence, launch app, get notification and verify we're correctly home or away
# ID: 39573 39574
# DESCRIPTION: one user: force close, depart geofence, launch app, get crossed notif and verify away.  Repeat with arriving home
#
################################################################################
from common import *

def run_test(flow, device, data):
    #android: works on Lyric Relaunch build from 30 Mar 2015, 16:03 on "last_couple_changes" branch commit 447035a1f0501bb566ffda619842ec5a35fd1ea4 with hack: verify_notification() simply returns True

    flow.blocked_on_ios("force quit does not exist on ios")

    #flow.login_and_logout(data.user03, set_loc=data.geo_loc03a)

    flow.login(data.user02, show_geofence_alerts=True)
    flow.get_api().set_default_setpoints()

    #set geofence to known state
    flow.set_geofence(data.geofence01a, data.user02.loc01)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='?'), "should have seen arrive via fencecrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"
    flow.goto_home()

    #force quit, set current location to AWAY, relaunch
    flow.force_quit()
    flow.set_geo_location(data.geo_loc03a, switch_back=False)
    flow.launch_app()

    #verify we got departed trigger
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()

    #force quit, set current location to HOME, relaunch
    flow.force_quit()
    flow.set_geo_location(data.geo_loc01a, switch_back=False)
    flow.launch_app()

    #verify we got arrived trigger
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='occupied'), "should have seen arrived via fenceCrossed notif but did NOT"
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
