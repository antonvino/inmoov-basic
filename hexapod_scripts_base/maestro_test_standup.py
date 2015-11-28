#!/usr/bin/python
###########################################################################################
# Filename:
#     Device.py
###########################################################################################
# Project Authors:
#     Juhapekka Piiroinen
#     Brian Wu
#
# Changes:
#     June 14, 2010 by Juhapekka Piiroinen - changes committed to svn
#           - added comments for the device commands according to the manual from Pololu
#           - added latest draft code for rotating base servo (Parallax Continuous Rotating Servo)
#           - note! you should be able to clear error flags with .get_errors function according to the manual
#           - renamed CameraDriver to LegacyCameraDriver as Brian Wu has done better one
#           - integrated batch of changes provided by Brian Wu
#
#     June 11, 2010 by Brian Wu - Changes committed thru email
#           - Decoupling the implementation from the program
#
#     April 19, 2010 by Juhapekka Piiroinen
#           - Initial Release
#
# Email:
#     juhapekka.piiroinen@gmail.com
#
# License:
#     GNU/GPLv3
#
# Description:
#     A python-wrapper for Pololu Micro Maestro 6-Channel USB Servo Controller
#
############################################################################################
# /!\ Notes /!\
# You will have to enable _USB Dual Port_ mode from the _Pololu Maestro Control Center_.
#
############################################################################################
# Device Documentation is available @ http://www.pololu.com/docs/pdf/0J40/maestro.pdf
############################################################################################
# (C) 2010 Juhapekka Piiroinen
#          Brian Wu
############################################################################################
import serial
import time

def log(*msgline):
    for msg in msgline:
        print msg,
    print

class Device(object):
    def __init__(self,con_port="COM6",ser_port="COM7",timeout=1): #/dev/ttyACM0  and   /dev/ttyACM1  for Linux
        ############################
        # lets introduce and init the main variables
        self.con = None
        self.ser = None
        self.isInitialized = False

        ############################
        # lets connect the TTL Port
        try:
            self.con = serial.Serial(con_port,timeout=timeout,baudrate=9600)
            self.con.close()
            self.con.open()
            self.con.baudrate = 9600
            log("Link to Command Port -", con_port, "- successful")

        except serial.serialutil.SerialException, e:
            print e
            log("Link to Command Port -", con_port, "- failed")

        if self.con:
            #####################
            #If your Maestro's serial mode is "UART, detect baud rate", you must first send it the baud rate indication byte 0xAA on
            #the RX line before sending any commands. The 0xAA baud rate indication byte can be the first byte of a Pololu protocol
            #command.
            #http://www.pololu.com/docs/pdf/0J40/maestro.pdf - page 35
            self.con.baudrate = 9600
            self.con.write(chr(0xAA))
            self.con.flush()
            log("Baud rate indication byte 0xAA sent!")
            pass

        ###################################
        # lets connect the TTL Port
        try:
            self.ser = serial.Serial(ser_port,timeout=timeout,baudrate=9600)
            self.ser.close()
            self.ser.open()
            self.ser.baudrate = 9600
            log("Link to TTL Port -", ser_port, "- successful")
        except serial.serialutil.SerialException, e:
            print e
            log("Link to TTL Port -", ser_port, "- failed!")

        self.isInitialized = (self.con!=None and self.ser!=None)
        if (self.isInitialized):
            err_flags = self.get_errors()
            log("Device error flags read (",err_flags,") and cleared")
        log("Device initialized:",self.isInitialized)

    ###########################################################################################################################
    ## common write function for handling all write related tasks
    def write(self,*data):
        if not self.isInitialized: log("Not initialized"); return
        if not self.ser.writable():
            log("Device not writable")
            return
        for d in data:
            self.ser.write(chr(d))
        self.ser.flush()

    ###########################################################################################################################
    ## Go Home
    # Compact protocol: 0xA2
    # --
    # This command sends all servos and outputs to their home positions, just as if an error had occurred. For servos and
    # outputs set to "Ignore", the position will be unchanged.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def go_home(self):
        if not self.isInitialized: log("Not initialized"); return
        self.write(0xA2)

    ###########################################################################################################################
    ## Set Target
    # Compact protocol: 0x84, channel number, target low bits, target high bits
    # --
    # The lower 7 bits of the third data byte represent bits 0-6 of the target (the lower 7 bits), while the lower 7 bits of the
    # fourth data byte represent bits 7-13 of the target. The target is a non-negative integer.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def set_target(self,servo,value):
        if not self.isInitialized: log("Not initialized"); return
        highbits,lowbits = divmod(value,32)
        self.write(0x84,servo,lowbits << 2,highbits)

    ###########################################################################################################################
    ## Set Speed
    # Compact protocol: 0x87, channel number, speed low bits, speed high bits
    # --
    # This command limits the speed at which a servo channel's output value changes. The speed limit is given in units of (0.25 us)/(10 ms)
    # --
    # For example, the command 0x87, 0x05, 0x0C, 0x01 sets
    # the speed of servo channel 5 to a value of 140, which corresponds to a speed of 3.5 us/ms. What this means is that if
    # you send a Set Target command to adjust the target from, say, 1000 us to 1350 us, it will take 100 ms to make that
    # adjustment. A speed of 0 makes the speed unlimited, so that setting the target will immediately affect the position. Note
    # that the actual speed at which your servo moves is also limited by the design of the servo itself, the supply voltage, and
    # mechanical loads; this parameter will not help your servo go faster than what it is physically capable of.
    # --
    # At the minimum speed setting of 1, the servo output takes 40 seconds to move from 1 to 2 ms.
    # The speed setting has no effect on channels configured as inputs or digital outputs.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def set_speed(self,servo,speed):
        if not self.isInitialized: log("Not initialized"); return
        highbits,lowbits = divmod(speed,32)
        self.write(0x87,servo,lowbits << 2,highbits)

    ###########################################################################################################################
    ## Set Acceleration
    # Compact protocol: 0x89, channel number, acceleration low bits, acceleration high bits
    # --
    # This command limits the acceleration of a servo channel's output. The acceleration limit is a value from 0 to 255 in units of (0.25 us)/(10 ms)/(80 ms),
    # --
    # A value of 0 corresponds to no acceleration limit. An acceleration limit causes the speed of a servo to slowly ramp up until it reaches the maximum speed, then
    # to ramp down again as position approaches target, resulting in a relatively smooth motion from one point to another.
    # With acceleration and speed limits, only a few target settings are required to make natural-looking motions that would
    # otherwise be quite complicated to produce.
    # --
    # At the minimum acceleration setting of 1, the servo output takes about 3 seconds to move smoothly from a target of 1 ms to a target of 2 ms.
    # The acceleration setting has no effect on channels configured as inputs or digital outputs.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def set_acceleration(self,servo,acceleration):
        if not self.isInitialized: log("Not initialized"); return
        highbits,lowbits = divmod(acceleration,32)
        self.write(0x89,servo,lowbits << 2,highbits)

    ###########################################################################################################################
    ## Get Position
    # Compact protocol: 0x90, channel number
    # Response: position low 8 bits, position high 8 bits
    # --
    # This command allows the device communicating with the Maestro to get the position value of a channel. The position
    # is sent as a two-byte response immediately after the command is received.
    # --
    # If the specified channel is configured as a servo, this position value represents the current pulse width that the Maestro
    # is transmitting on the channel, reflecting the effects of any previous commands, speed and acceleration limits, or scripts
    # running on the Maestro.
    # --
    # If the channel is configured as a digital output, a position value less than 6000 means the Maestro is driving the line low,
    # while a position value of 6000 or greater means the Maestro is driving the line high.
    # --
    # If the channel is configured as an input, the position represents the voltage measured on the channel. The inputs on
    # channels 0-11 are analog: their values range from 0 to 1023, representing voltages from 0 to 5 V. The inputs on channels
    # 12-23 are digital: their values are either exactly 0 or exactly 1023.
    # --
    # Note that the formatting of the position in this command differs from the target/speed/acceleration formatting in the
    # other commands. Since there is no restriction on the high bit, the position is formatted as a standard little-endian two-
    # byte unsigned integer. For example, a position of 2567 corresponds to a response 0x07, 0x0A.
    # --
    # Note that the position value returned by this command is equal to four times the number displayed in the Position box
    # in the Status tab of the Maestro Control Center.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def get_position(self,servo):
        if not self.isInitialized: log("Not initialized"); return None
        self.write(0x90,servo)
        data = self.ser.read(2)
        if data:
            return (ord(data[0])+(ord(data[1])<<8))/4
        else:
            return None

    ###########################################################################################################################
    ## Get Moving State
    # Compact protocol: 0x93
    # Response: 0x00 if no servos are moving, 0x01 if servos are moving
    # --
    # This command is used to determine whether the servo outputs have reached their targets or are still changing, limited
    # by speed or acceleration settings. Using this command together with the Set Target command, you can initiate several
    # servo movements and wait for all the movements to finish before moving on to the next step of your program.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def get_moving_state(self):
        if not self.isInitialized: log("Not initialized"); return None
        self.write(0x93)
        data = self.ser.read(1)
        if data:
            return ord(data[0])
        else:
            return None

    ###########################################################################################################################
    ## Get Errors
    # Compact protocol: 0xA1
    # --
    # Response: error bits 0-7, error bits 8-15
    # --
    # Use this command to examine the errors that the Maestro has detected.
    # --
    # The error register is sent as a two-byte response immediately after the command is received,
    # then all the error bits are cleared. For most applications using serial control, it is a good idea to check errors continuously
    # and take appropriate action if errors occur.
    # --
    # Source: http://www.pololu.com/docs/pdf/0J40/maestro.pdf
    def get_errors(self):
        if not self.isInitialized: log("Not initialized"); return None
        self.write(0xA1)
        data = self.ser.read(2)
        if data:
            return ord(data[0])+(ord(data[1])<<8)
        else:
            return None

    ###########################################################################################################################
    ## a helper function for Set Target
    def wait_until_at_target(self):
        while (self.get_moving_state()):
            time.sleep(0.1)

    ###########################################################################################################################
    ## Lets close and clean when we are done
    def __del__(self):
        if (self.ser):
            self.ser.close()
        if (self.con):
            self.con.close()
        del(self.ser)
        del(self.con)




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

time.sleep(2)
print 'changing legs'
lower_leg(3)
lower_leg(4)
lower_leg(5)
time.sleep(0.2)
lift_leg(0)
lift_leg(1)
lift_leg(2)

time.sleep(2)
print 'changing legs'
lower_leg(0)
lower_leg(1)
lower_leg(2)
time.sleep(0.2)
lift_leg(3)
lift_leg(4)
lift_leg(5)

time.sleep(2)
print 'changing legs'
lower_leg(3)
lower_leg(4)
lower_leg(5)
time.sleep(0.2)
lift_leg(0)
lift_leg(1)
lift_leg(2)

time.sleep(2)
step = 0
while(step < 5):
    print 'lift 3 legs'
    lift_leg(0)
    lift_leg(1)
    lift_leg(2)
    time.sleep(0.2)
    print 'move 3 lifted legs forward'
    rotate_leg(0,"forward")
    rotate_leg(1,"forward")
    rotate_leg(2,"forward")
    time.sleep(0.2)
    print 'lower lifted legs'
    lower_leg(0)
    lower_leg(1)
    lower_leg(2)
    print 'lift other legs'
    lift_leg(3)
    lift_leg(4)
    lift_leg(5)
    print 'move 3 lifted legs forward'
    rotate_leg(3,"forward")
    rotate_leg(4,"forward")
    rotate_leg(5,"forward")
    time.sleep(0.2)
    print 'lower lifted legs'
    lower_leg(3)
    lower_leg(4)
    lower_leg(5)
    step += 1

print 'END of walking'
time.sleep(2)
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
