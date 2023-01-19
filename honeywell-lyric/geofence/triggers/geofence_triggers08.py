################################################################################
#
# NAME: geofence_triggers08 - one user: crossing fence then enabling location services causes notification and updates home/away
# ID: 39575 39576
# DESCRIPTION: one user: disable loc services, depart geofence, enable services, see notification and verify away.  Repeat with arriving home...
#
################################################################################
from common import *

def run_test(flow, device, data):
    #android: works on Lyric Relaunch build from 30 Mar 2015, 16:03 on "last_couple_changes" branch commit 447035a1f0501bb566ffda619842ec5a35fd1ea4 with hack: verify_notification() simply returns True

    flow.blocked_on_ios("location_services not currently automatable on ios")
    #flow.login_and_logout(data.user03, set_loc=data.geo_loc03a)

    flow.login(data.user02, show_geofence_alerts=True)
    flow.get_api().set_default_setpoints()

    #set geofence to known state
    flow.set_geofence(data.geofence01a, data.user02.loc01)
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='arrived', result='?'), "should have seen arrive via fencecrossed notif but did NOT"
    flow.goto_home()
    assert flow.verify_loc('home', data.user02.loc01.dev01), "We should be HOME but we are NOT"
    flow.goto_home()

    #turn off loc services, set current location to AWAY, turn services back on
    flow.set_location_services('off', False)
    flow.set_geo_location(data.geo_loc03a)
    flow.set_location_services('on')
    flow.dismiss_location_services_dialog()

    #verify we got departed trigger
    assert flow.verify_notification(type='fencecrossed', location=data.user02.loc01, action='departed', result='empty'), "should have seen departed via fenceCrossed notif but did NOT"
    assert flow.verify_loc('away', data.user02.loc01.dev01), "We should be AWAY but we are NOT"
    flow.goto_home()

    #turn off loc services, set current location to HOME, turn services back on
    flow.set_location_services('off', False)
    flow.set_geo_location(data.geo_loc01a)
    flow.set_location_services('on')
    flow.dismiss_location_services_dialog()

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
