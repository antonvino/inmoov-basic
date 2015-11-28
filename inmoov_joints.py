#!/usr/bin/python
from maestro_lib import Device


  # <Channels MiniMaestroServoPeriod="80000" ServoMultiplier="1">
  #   <!--Period = 20 ms-->
  #   <!--Channel 0-->
  #   <Channel name="test" mode="Servo" min="256" max="16000" homemode="Ignore" home="256" speed="0" acceleration="0" neutral="3968" range="1905" />
  #   <!--Channel 1-->
  #   <Channel name="head up-down" mode="Servo" min="2432" max="5504" homemode="Off" home="2432" speed="0" acceleration="0" neutral="5440" range="1905" />
  #   <!--Channel 2-->
  #   <Channel name="head LR RECAL" mode="Servo" min="4544" max="7936" homemode="Off" home="4544" speed="0" acceleration="0" neutral="6720" range="1905" />
  #   <!--Channel 3-->
  #   <Channel name="torso (double)" mode="Servo" min="1984" max="9216" homemode="Off" home="1984" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 4-->
  #   <Channel name="L shldr" mode="Servo" min="7040" max="9216" homemode="Off" home="7040" speed="0" acceleration="0" neutral="8760" range="1905" />
  #   <!--Channel 5-->
  #   <Channel name="L shldr fb" mode="Servo" min="3264" max="9792" homemode="Off" home="3264" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 6-->
  #   <Channel name="L shldr twst" mode="Servo" min="2048" max="9152" homemode="Off" home="2048" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 7-->
  #   <Channel name="L elbow RECAL" mode="Servo" min="3904" max="5632" homemode="Off" home="3904" speed="0" acceleration="0" neutral="5184" range="1905" />
  #   <!--Channel 8-->
  #   <Channel name="R shldr" mode="Servo" min="5888" max="7808" homemode="Off" home="5888" speed="0" acceleration="0" neutral="5888" range="1905" />
  #   <!--Channel 9-->
  #   <Channel name="R shldr fb" mode="Servo" min="4096" max="8576" homemode="Off" home="4096" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 10-->
  #   <Channel name="R shldr twst" mode="Servo" min="2240" max="10240" homemode="Off" home="2240" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 11-->
  #   <Channel name="R elbow RECAL" mode="Servo" min="5184" max="8384" homemode="Off" home="5184" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 12-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 13-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 14-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 15-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 16-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 17-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 18-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 19-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 20-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 21-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 22-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  #   <!--Channel 23-->
  #   <Channel name="" mode="Servo" min="3968" max="8000" homemode="Off" home="3968" speed="0" acceleration="0" neutral="6000" range="1905" />
  # </Channels>

INMOOV_LIMITS = [
    [0,0],  # test servo
    [2432,5504],  # head up-down
]

INMOOV_HEAD_SERVO = 1

servo = Device("/dev/ttyACM0","/dev/ttyACM1")

import sys
from math import floor

def move_head(direction = 'up'):
    target = None
    print '[MOVE] Head: {0}'.format(direction)
    if(direction == 'up'):
        target = INMOOV_LIMITS[INMOOV_HEAD_SERVO][1]  # upper limit
    elif(direction == 'center'):
        target = INMOOV_LIMITS[INMOOV_HEAD_SERVO][0] + int(floor((INMOOV_LIMITS[INMOOV_HEAD_SERVO][1]-INMOOV_LIMITS[INMOOV_HEAD_SERVO][1])/2))
    elif(direction == 'down'):
        target = INMOOV_LIMITS[INMOOV_HEAD_SERVO][0]  # lower limit
    else:
        print 'Invalid direction'
    if target is not None:
        print 'do! {0}'.format(target)
        target = 1114
        servo.set_target(INMOOV_HEAD_SERVO, target)
