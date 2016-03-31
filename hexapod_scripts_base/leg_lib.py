#!/usr/bin/python
from maestro_lib import Device
####################################################################

hexapod_legs_safe = [
    [[1268,2412], [580,1644], [624,1500]],  # leg 0
    [[596,1900], [804,1900], [500,1548]],  # leg 1
    [[736,2044], [500,1612], [756,1692]],  # leg 2
    [[500,1772], [1348,2396], [1012,1452]],  # leg 3
    [[1012,2396], [1172,2140], [1460,1996]],  # leg 4
    [[804,2204], [1044,1996], [596,1500]],  # leg 5
]

servo = Device("/dev/ttyACM0","/dev/ttyACM0")

import sys
from math import floor

def lower_leg(leg):
    # simple lowering of the leg
    foot_reverse, knee_reverse, hip_reverse = get_reverse(leg)
    # 1) move foot low to 1/4
    joint = 0
    srv = get_servo(leg, joint)
    # foot - lower up
    if(foot_reverse):
        # end point - 1/4 of the range
        target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    else:  # RHS
        # start point + 1/4 of the range
        target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    print 'lowering foot {0} to {1}'.format(leg, target)
    servo.set_target(srv, target)

    # 2) move knee to middle
    joint = 1
    srv = get_servo(leg, joint)
    # knee
    if(knee_reverse):
        # end point - 1/2 of the range
        target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/2))
    else:
        # start point + 1/2 of the range
        target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/2))
    print 'lowering knee {0} to {1}'.format(leg, target)
    servo.set_target(srv, target)

def lift_leg(leg):
    # simple lifting of the leg
    foot_reverse, knee_reverse, hip_reverse = get_reverse(leg)
    # 1) move foot low to 1/4
    joint = 0
    srv = get_servo(leg, joint)
    # foot
    if(foot_reverse):
        # end point - 1/4 of the range
        target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    else:  # RHS
        # start point + 1/4 of the range
        target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    print 'lifting foot {0} to {1}'.format(leg, target)
    servo.set_target(srv, target)

    # 2) move knee to the top
    joint = 1
    srv = get_servo(leg, joint)
    # knee - LHS lower down
    if(knee_reverse):
        # start point + 1/4 of the range
        target = hexapod_legs_safe[leg][joint][0]# + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    else:
        # end point - 1/4 of the range
        target = hexapod_legs_safe[leg][joint][1]# - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    print 'lifting knee {0} to {1}'.format(leg, target)
    servo.set_target(srv, target)

def rotate_leg(leg, position):
    foot_reverse, knee_reverse, hip_reverse = get_reverse(leg)

    joint = 2  # shoulder
    if(position == "back"):
        srv = get_servo(leg, joint)
        # foot
        if(foot_reverse):
            # end point - 1/4 of the range
            target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        else:
            # start point + 1/4 of the range
            target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        print 'moving shoulder {0} back to {1}'.format(leg, target)
        servo.set_target(srv, target)

    if(position == "forward"):
        srv = get_servo(leg, joint)
        # foot
        if(foot_reverse):
            # start point + 1/4 of the range
            target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        else:
            # end point - 1/4 of the range
            target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        print 'moving shoulder {0} forward to {1}'.format(leg, target)
        servo.set_target(srv, target)

    if(position == "middle"):
        srv = get_servo(leg, joint)
        # start point + 1/2 of the range
        target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/2))
        print 'moving shoulder {0} to the middle {1}'.format(leg, target)
        servo.set_target(srv, target)

def get_servo(leg, joint):
    return leg*3 + joint

def get_reverse(leg):
    foot_reverse = False
    knee_reverse = False
    hip_reverse = False
    # depending on the leg the increase/decrease of the values does
    # a different thing i.e. lower-up, lower-forward etc
    if(leg == 0 or leg == 4 or leg == 5):
        foot_reverse = True
        knee_reverse = False
        hip_reverse = True
    elif(leg == 1 or leg == 2 or leg == 3):
        foot_reverse = False
        knee_reverse = True
        hip_reverse = False
    return foot_reverse, knee_reverse, hip_reverse

def init_legs():
    print 'Reseting legs to the initial position'

    print 'shoulders to the middle'
    rotate_leg(0, "middle")
    rotate_leg(1, "middle")
    rotate_leg(2, "middle")
    rotate_leg(3, "middle")
    rotate_leg(4, "middle")
    rotate_leg(5, "middle")

    print 'lifting all legs'
    lift_leg(0)
    lift_leg(1)
    lift_leg(2)
    lift_leg(3)
    lift_leg(4)
    lift_leg(5)
