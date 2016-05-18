#!/usr/bin/python
from maestro_lib import Device
from math import fabs

# positions
LOW = 0
MIDDLE = 1
HIGH = 2
# values: low, middle, high
INMOOV_JOINTS = [
    [0,0,0],  # test servo
    [608,1000,1376],  # head pitch
    [800,1150,1504],  # head yaw
    [496,1500,2304],  # torso
    [1760,2000,2304],  # L shoulder roll
    [1808,2200,2656],  # L shoulder pitch
    [1312,1650,2000],  # L shoulder yaw
    [896,1000,1152],  # L elbow
    [1472,1600,1952],  # R shoulder roll
    [1056,1400,1808],  # R shoulder pitch
    [1152,1750,2304],  # R shoulder yaw
    [1200,1350,1552],  # R elbow
]

INMOOV_SERVOS = {
    'head': {
        'pitch': 1,
        'yaw': 2
    },
    'torso': 3,
    'left':
    {
        'shoulder': {
            'roll': 4,
            'pitch': 5,
            'yaw': 6
        },
        'elbow': 7
    },
    'right':
    {
        'shoulder': {
            'roll': 8,
            'pitch': 9,
            'yaw': 10
        },
        'elbow': 11
    },
}

# sides
LEFT = 0
RIGHT = 1

SIDE_NAMES = {
    LEFT: 'left',
    RIGHT: 'right'
}

POS_NAMES = {
    MIDDLE: 'middle',
    LOW: 'low',
    HIGH: 'high'
}

servo = Device("/dev/ttyACM0","/dev/ttyACM0")

import sys
from math import floor

def head(part, pos, speed = 5):
    if pos_valid(pos):
        print '[MOVE] Head: {0} {1}'.format(part, POS_NAMES[pos])
        srv = INMOOV_SERVOS['head'][part]
        target = INMOOV_JOINTS[srv][pos]
        print 'Target: {0}'.format(target)
        servo.set_speed(srv, speed)
        servo.set_target(srv, target)
    else:
        print 'Invalid position'

def torso(pos, speed = 5):
    if pos_valid(pos):
        print '[MOVE] Torso: {0}'.format(POS_NAMES[pos])
        srv = INMOOV_SERVOS['torso']
        target = INMOOV_JOINTS[srv][pos]
        print 'Target: {0}'.format(target)
        servo.set_speed(srv, speed)
        servo.set_target(srv, target)
    else:
        print 'Invalid position'

def elbow(side, pos, speed = 10):
    if pos_valid(pos):
        print '[MOVE] Elbow: {0} {1}'.format(SIDE_NAMES[side], POS_NAMES[pos])
        srv = INMOOV_SERVOS[SIDE_NAMES[side]]['elbow']
        target = INMOOV_JOINTS[srv][pos]
        print 'Target: {0}'.format(target)
        servo.set_speed(srv, speed)
        servo.set_target(srv, target)
    else:
        print 'Invalid position'

def shoulder(side, axis, pos, offset = 0, speed = 10):
    if pos_valid(pos):
        if(fabs(offset) > 1000):
            offset = 1000
        print '[MOVE] Shoulder: {0} {1} {2}'.format(SIDE_NAMES[side], axis, POS_NAMES[pos])
        srv = INMOOV_SERVOS[SIDE_NAMES[side]]['shoulder'][axis]
        target = INMOOV_JOINTS[srv][pos]+offset
        print 'Target: {0}'.format(target)
        servo.set_speed(srv, speed)
        servo.set_target(srv, target)
    else:
        print 'Invalid position'

def pos_valid(pos):
    valid = False
    if(pos == LOW or pos == MIDDLE or pos == HIGH):
        valid = True
    return valid

def arm_init(side, reverse = False):
    if(reverse):
        shoulder(side, 'pitch', HIGH)
    else:
        shoulder(side, 'pitch', LOW)
    shoulder(side, 'yaw', MIDDLE)
    shoulder(side, 'roll', LOW)
    elbow(side, HIGH)

def arm_abitup(side):
    shoulder(side, 'pitch', MIDDLE,300)
    shoulder(side, 'yaw', MIDDLE)
    shoulder(side, 'roll', LOW)
    elbow(side, HIGH)
