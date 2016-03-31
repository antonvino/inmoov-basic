#!/usr/bin/python
from inmoov_joints import *
import time

cmd = sys.argv[1]
if(cmd == "yes"):
    print '[CMD] Yes. Nodding.'
    head('pitch', HIGH, 20)
    time.sleep(0.3)
    head('pitch', LOW, 20)
    time.sleep(0.3)
    head('pitch', HIGH, 20)
    time.sleep(0.3)
    head('pitch', LOW, 20)
    time.sleep(0.2)
    head('pitch', MIDDLE, 20)
elif(cmd == "no"):
    print '[CMD] No. Shaking head.'
    head('yaw', LOW, 20)
    time.sleep(0.3)
    head('yaw', HIGH, 20)
    time.sleep(0.3)
    head('yaw', LOW, 20)
    time.sleep(0.3)
    head('yaw', HIGH, 20)
    time.sleep(0.2)
    head('yaw', MIDDLE, 20)
elif(cmd == "wave_left"):
    print '[CMD] Waving left hand.'
    # up-shoulder up PITCH is fwd-back shoulder
    shoulder(LEFT, 'pitch', HIGH)
    # twist-shoulder middle
    shoulder(LEFT, 'yaw', MIDDLE)
    # elbow middle
    elbow(LEFT, MIDDLE)
    # side-shoulder low
    shoulder(LEFT, 'roll', LOW)
    time.sleep(8)
    # twist-shoulder left-right
    shoulder(LEFT, 'yaw', HIGH)
    time.sleep(4)
    shoulder(LEFT, 'yaw', LOW)
    time.sleep(4)
    shoulder(LEFT, 'yaw', HIGH)
    time.sleep(4)
    shoulder(LEFT, 'yaw', LOW)
    time.sleep(4)
    # back to normal
    arm_init(LEFT)
elif(cmd == "dance"):
    print '[CMD] Dancing.'
    #arm_init(LEFT)
    #arm_init(RIGHT)
    torso(HIGH)
    time.sleep(2)
    torso(LOW)
    time.sleep(2)
    torso(HIGH)
    time.sleep(2)
    torso(LOW)
elif(cmd == "panhead"):
    print '[CMD] Panning.'
    head('yaw', LOW, 1)
    time.sleep(5)
    head('yaw', HIGH, 1)
    time.sleep(5)
    head('yaw', LOW, 1)
    time.sleep(5)
    head('yaw', HIGH, 1)
    time.sleep(5)
    head('yaw', MIDDLE, 1)
elif(cmd == "hands_up"):
    # left up-shoulder up
    # right up-shoulder up
    # left side shoulder low
    # left side shoulder low
    # left twist-shoulder middle
    # right twist shoulder middle
    pass
elif(cmd == "hands_span"):
    # shoulders up
    # elbows down
    # shoulder-twist forward
    pass
elif(cmd == "hands_wave"):
    # hands up then shoulders low-high, high-low
    # so that hands move in same directions together
    pass
elif(cmd == "arm_init"):
    arm_init(LEFT)
    arm_init(RIGHT)
elif(cmd == "arm_abitup"):
    arm_abitup(LEFT)
    arm_abitup(RIGHT)
elif(cmd == "slow_1"): # event cmd for moving different things slowly
    print '[CMD] Slow movements 1.'
    # first stage
    torso(HIGH, 2)
    head('yaw', LOW, 2)
    elbow(LEFT, HIGH, 2)
    shoulder(LEFT, 'roll', LOW, 300, 2)
    time.sleep(5)
    # second stage
    torso(LOW, 2)
    head('yaw', HIGH, 2)
    elbow(LEFT, LOW, 2)
    shoulder(LEFT, 'roll', HIGH, -300, 2)
    # back to normal
    time.sleep(5)
    torso(MIDDLE, 2)
    head('pitch', MIDDLE, 2)
    head('yaw', MIDDLE, 2)
    elbow(LEFT, MIDDLE, 2)
    shoulder(LEFT, 'roll', MIDDLE, 0, 2)
    shoulder(LEFT, 'yaw', MIDDLE, 0, 2)
elif(cmd == "slow_2"): # event cmd for moving different things slowly
    print '[CMD] Slow movements 2.'
    # first stage
    torso(HIGH, 2)
    head('pitch', LOW, 2)
    elbow(LEFT, HIGH, 2)
    shoulder(LEFT, 'pitch', HIGH, -300, 2)
    #shoulder(LEFT, 'roll', LOW, 100, 2)
    shoulder(LEFT, 'roll', LOW, 100, 2)
    time.sleep(5)
    # second stage
    torso(LOW, 2)
    head('pitch', HIGH, 2)
    elbow(LEFT, LOW, 2)
    shoulder(LEFT, 'roll', HIGH, -100, 2)
    shoulder(LEFT, 'yaw', HIGH, -100, 2)
    time.sleep(5)
    # back to normal
    torso(MIDDLE, 2)
    head('pitch', MIDDLE, 2)
    head('yaw', MIDDLE, 2)
    elbow(LEFT, MIDDLE, 2)
    shoulder(LEFT, 'roll', MIDDLE, 0, 2)
    shoulder(LEFT, 'yaw', MIDDLE, 0, 2)
    shoulder(LEFT, 'pitch', MIDDLE, -100, 2)
