#!/usr/bin/env python
import time
import serial
          
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.baudrate = 9600
servo=0

ser.close()
ser.open()
#ser.open()
#ser.isOpen()

print("Initializing the device ..")

ser.write(chr(0xAA))
ser.flush()

print("Write command")
ser.write (bytes([132, 0, 122, 46]))

ser.write(bytes(map(hex,[132,1,112,34])))

ser.write(bytes([0x84, 0x02, 0x70, 0x2E]))

#ser.write(bytes(0x84))
#ser.write(bytes(0x00))

print('Done')

#while 1:
    #servo_str = "{0:x}{1:x}{2:x}{3:x}".format(132,servo,112,46)

    #servo_str = "\xAA\x84\x00\x70\x2E"  #.format(hex(servo))
    #servo_str = '0x84, 0x00, 0x70, 0x2E'
    #print(servo_str)
    #ser.write(servo_str)
    #time.sleep(1)
    #servo += 1
