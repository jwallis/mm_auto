################################################################################
#
# NAME: geofence_triggers01 - one user: depart and arrive, verify notifications and thermostat current temp update
# ID: 39556 39557 39563 39564 39565
# DESCRIPTION: one user: depart and arrive, verify notifications and thermostat current temp update
#
################################################################################
from common import *

def run_test(flow, device, data):
    #android: works on Lyric Relaunch build from 30 Mar 2015, 16:03 on "last_couple_changes" branch commit 447035a1f0501bb566ffda619842ec5a35fd1ea4 with hack: verify_notification() simply returns True

    #flow.login_and_logout(data.user03, set_loc=data.geo_loc03a)

    flow.login(data.user02, show_geofence_alerts=True)
    flow.get_api().set_default_setpoints()

    #need to be either heat or cool during our verification step
    flow.api.set_heat_cool('cool')

    # Set-up the geofence and our locations
    flow.set_geofence(data.geofence01a, data.user02.loc01)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='?'), "should have seen arrive via fencecrossed notif but did NOT"
    flow.goto_home()

    #[TC: Geofence-39556] - Verify user gets "UserDeparted" & "HouseIsEmpty" notifications
    # when the user goes outside the geofence
    flow.set_geo_location(data.geo_loc03a)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    assert flow.verify_loc('away', data.user02.loc01.dev01), "39556: We should be AWAY but we are NOT"
    flow.goto_home()

    #[TC: Geofence-39557] - Verify user gets "UserArrived" & "HouseIsOccupied" notifications
    # when the user gets inside the geofence
    flow.set_geo_location(data.geo_loc01a)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='occupied'), "should have seen arrived via fenceCrossed notif but did NOT"
    assert flow.verify_loc('home', data.user02.loc01.dev01), "39557: We should be HOME but we are NOT"


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
