################################################################################
#
# NAME: geofence_triggers04 - one user: modifying geofence that does NOT result in a geofence crossing only yields fencemodified notification
# ID: 39579 39584
# DESCRIPTION: one user: while inside fence, modify fence but stay inside fence, only get fence modified notif.  Repeat while outside fence
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

    ####currently, verify_notification() is just returning True, If it were working, we'd get the notif, then go check that the thermostat is right.
    ####since we're not getting the notif, we need to wait while the system processes the geofence update....
    flow.sleep(60)
    flow.set_geofence(data.geofence01b, data.user02.loc01, recenter=False)
    assert (flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='nosignificance')), "should have seen arrived via fencecrossed no significance but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"
    flow.goto_home()

    #depart geofence
    flow.set_geo_location(data.geo_loc03a)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()

    ####currently, verify_notification() is just returning True, If it were working, we'd get the notif, then go check that the thermostat is right.
    ####since we're not getting the notif, we need to wait while the system processes the geofence update....
    flow.sleep(60)
    flow.set_geofence(data.geofence01a, data.user02.loc01, recenter=False)
    assert (flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='nosignificance')), "should have seen departed via fencecrossed no significance but did NOT"
    flow.goto_home()
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()


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
