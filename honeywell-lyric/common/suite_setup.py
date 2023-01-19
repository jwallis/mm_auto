################################################################################
#
# NAME: suite_setup - set device_model and screenshot the version
# ID:
# DESCRIPTION: set device_model and screenshot the version
#
################################################################################
from common import *

def run_test(flow, device, data):
    global device_model
    device_model = flow.device_model

    flow.screenshot_version(data.user02)

try:
    flow, device, data = get_flow()
    flow.hw_lyric_setup()
    run_test(flow, device, data)
    flow.status = 'pass'
finally:
    try:
        flow.hw_lyric_teardown()
    except:
        pass