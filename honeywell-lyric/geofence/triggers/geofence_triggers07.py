################################################################################
#
# NAME: geofence_triggers07 - one user: crossing fence then logging in causes notification
# ID: 39560 39561
# DESCRIPTION: one user: log out, leave fence, log in, see Departed.  Log out, enter fence, log in, see Arrived
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

    #[TC: Geofence-39560] - Verify user gets "UserDeparted" & "HouseIsEmpty" notifications
    #logout, set current location to AWAY, log back in
    flow.logout()
    flow.set_geo_location(data.geo_loc03a)
    flow.login(data.user02, show_geofence_alerts=True, skip_all=True)

    #verify we got departed trigger
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()

    #[TC: Geofence-39561] - Verify user gets "UserArrived" & "HouseIsOccupied" notifications
    #logout, set current location to HOME, log back in
    flow.logout()
    flow.set_geo_location(data.geo_loc01a)
    flow.login(data.user02, show_geofence_alerts=True, skip_all=True)

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
