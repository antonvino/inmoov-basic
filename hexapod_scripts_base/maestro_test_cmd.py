#!/usr/bin/python
from leg_lib import *
import time

legset = 1
cmd = sys.argv[1]
if(cmd != "init"):
    legset = int(sys.argv[2])
if(legset == 1):
    legs = [0,1,2]
else:
    legs = [3,4,5]
if(cmd == "lift"):
    print '[CMD] Lift legs {0}'.format(legs)
    for leg in legs:
        lift_leg(leg)
elif(cmd == "lower"):
    print '[CMD] Lower legs {0}'.format(legs)
    for leg in legs:
        lower_leg(leg)
elif(cmd == "forward"):
    print '[CMD] Rotate legs forward {0}'.format(legs)
    for leg in legs:
        rotate_leg(leg, "forward")
elif(cmd == "back"):
    print '[CMD] Rotate legs back {0}'.format(legs)
    for leg in legs:
        rotate_leg(leg, "back")
elif(cmd == "middle"):
    print '[CMD] Rotate legs to the center {0}'.format(legs)
    for leg in legs:
        rotate_leg(leg, "middle")
elif(cmd == "init"):
    print '[CMD] Reset legs'
    init_legs()
elif(cmd == "step_fwd"):
    print '[CMD] Step forward {0}'.format(legset)
    if(legset <= 0 or legset >=11):
        legset = 1
    step = 0
    while(step < legset):
        # assuming initially init()
        # lift 1 set up
        legs = [0,1,2]
        for leg in legs:
            lift_leg(leg)
        time.sleep(0.2)
        # move 1 set forward
        legs = [0,1,2]
        for leg in legs:
            rotate_leg(leg,"forward")
        time.sleep(0.2)
        # lower 1 set down
        legs = [0,1,2]
        for leg in legs:
            lower_leg(leg)
        # lift 2 set up (same time)
        legs = [3,4,5]
        for leg in legs:
            lift_leg(leg)
        time.sleep(0.2)
        # move 1 set to middle (this should move the body forward if there
        # is not too much slip)
        legs = [0,1,2]
        for leg in legs:
            rotate_leg(leg,"middle")
        time.sleep(0.2)
        # move set 2 forward
        legs = [3,4,5]
        for leg in legs:
            rotate_leg(leg,"forward")
        time.sleep(0.2)
        # lower 2 set down
        legs = [3,4,5]
        for leg in legs:
            lower_leg(leg)
        # time.sleep(0.2)
        # lift 1 set up
        legs = [0,1,2]
        for leg in legs:
            lift_leg(leg)
        time.sleep(0.2)
        # move 2 set to the middle (this should move the body forward)
        legs = [3,4,5]
        for leg in legs:
            rotate_leg(leg,"middle")
        time.sleep(0.2)
        # increase the step count
        step+=1

    # stop - init legs
    init_legs()
