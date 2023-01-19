################################################################################
#
# NAME: geofence_triggers03 - one user: Test geofence triggers scenarios when we use airplane mode
# ID: 39569 39570
# DESCRIPTION: one user: Verify geofence trigger activates when we set airplane mode on and we move away from geofence.
# Verify geofence trigger activates when we set airplane mode on and we move into from geofence.
#
################################################################################
from common import *

def run_test(flow, device, data):
    #android: works on Lyric Relaunch build from 30 Mar 2015, 16:03 on "last_couple_changes" branch commit 447035a1f0501bb566ffda619842ec5a35fd1ea4 with hack: verify_notification() simply returns True
    flow.blocked_on_ios("airplane mode does not exist on ios")

    #flow.login_and_logout(data.user03, set_loc=data.geo_loc03a, timeout=140)
    flow.login(data.user02)
    flow.get_api().set_default_setpoints()

    flow.set_geofence(data.geofence01a) # in geofence.py
    flow.goto_home()

    # Android Only
    #[TC: Geofence-39569 ] - Verify user gets "UserDeparted" & "HouseIsEmpty" notifications when the user goes
    # outside the geofence and then disables airplane mode
    # - Turn on Airplane mode then move Away from the Location
    flow.set_airplane_mode("on", False)
    flow.set_geo_location(data.geo_loc03a)
    flow.set_airplane_mode("off")
    flow.retry_connection()
    assert flow.verify_loc('away', data.user02.loc01.dev01, "away"), "[TC: Geofence-39569] - We should be AWAY but we are NOT"

    # Android Only
    #[TC: Geofence-39570] - Verify user gets "UserArrived" & "HouseIsOccupied" notifications when the user gets
    # inside the geofence and then disables airplane mode
    # - Turn on Airplane mode then move Home to the Location
    flow.set_airplane_mode("on", False)
    flow.set_geo_location(data.geo_loc01a)
    flow.set_airplane_mode("off")
    flow.retry_connection()
    assert flow.verify_loc('home', data.user02.loc01.dev01, "home"), "[TC: Geofence-39570] - We should be HOME but we are NOT"

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
