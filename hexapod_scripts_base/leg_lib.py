#!/usr/bin/python
from maestro_lib import Device
####################################################################

hexapod_legs_safe = [
    [[804,2204], [996,2108], [628,1500]],  # leg 0
    [[596,1900], [804,1900], [500,1548]],  # leg 1
    [[404,1804], [1284,2412], [756,1900]],  # leg 2
    [[1092,2348], [1092,2156], [996,2108]],  # leg 3
    [[756,2108], [596,1548], [708,1596]],  # leg 4
    [[1092,2508], [708,1708], [596,1500]],  # leg 5
]

servo = Device("/dev/ttyAMA0","/dev/ttyAMA0")

import sys
from math import floor

def lower_leg(leg):
    # depending on the side the increase/decrease of the values does
    # a different thing
    # LHS
    lhs = False
    if(leg == 0 or leg == 3 or leg == 5):
        lhs = True

    # simple lowering of the leg
    # srv = leg*3 + joint
    # 1) move foot low to 1/4
    joint = 0
    srv = get_servo(leg, joint)
    # foot - LHS lower up
    if(lhs):
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
    # knee - LHS lower down
    if(lhs):
        # start point + 1/2 of the range
        target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/2))
    else:  # RHS
        # end point - 1/2 of the range
        target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/2))
    print 'lowering knee {0} to {1}'.format(leg, target)
    servo.set_target(srv, target)

def lift_leg(leg):
    # depending on the side the increase/decrease of the values does
    # a different thing
    # LHS
    lhs = False
    if(leg == 0 or leg == 3 or leg == 5):
        lhs = True

    # simple lifting of the leg
    # srv = leg*3 + joint
    # 1) move foot low to 1/4
    joint = 0
    srv = get_servo(leg, joint)
    # foot - LHS lower up
    if(lhs):
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
    if(lhs):
        # end point - 1/4 of the range
        target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    else:  # RHS
        # start point + 1/4 of the range
        target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
    print 'lifting knee {0} to {1}'.format(leg, target)
    servo.set_target(srv, target)

def rotate_leg(leg, position):
    # depending on the side the increase/decrease of the values does
    # a different thing
    # LHS
    lhs = False
    if(leg == 0 or leg == 3 or leg == 5):
        lhs = True

    joint = 2  # shoulder
    if(position == "back"):
        srv = get_servo(leg, joint)
        # foot - LHS lower back
        if(lhs):
            # start point + 1/4 of the range
            target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        else:  # RHS
            # end point - 1/4 of the range
            target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        print 'moving shoulder {0} back to {1}'.format(leg, target)
        servo.set_target(srv, target)

    if(position == "forward"):
        srv = get_servo(leg, joint)
        # foot - LHS lower back
        if(lhs):
            # end point - 1/4 of the range
            target = hexapod_legs_safe[leg][joint][1] - int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
        else:  # RHS
            # start point + 1/4 of the range
            target = hexapod_legs_safe[leg][joint][0] + int(floor((hexapod_legs_safe[leg][joint][1]-hexapod_legs_safe[leg][joint][0])/4))
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
