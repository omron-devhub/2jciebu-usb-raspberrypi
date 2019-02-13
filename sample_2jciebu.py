import serial
import time
from datetime import datetime
import os
import sys

# LED display rule. Normal Off.
DISPLAY_RULE_NORMALLY_OFF = 0

# LED display rule. Normal On.
DISPLAY_RULE_NORMALLY_ON = 1


def calc_crc(buf, length):
    """
    CRC-16 calculation.

    """
    crc = 0xFFFF
    for i in range(length):
        crc = crc ^ buf[i]
        for i in range(8):
            carrayFlag = crc & 1
            crc = crc >> 1
            if (carrayFlag == 1) : 
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    return(bytearray([crcL,crcH]))


def print_latest_data(data):
    """
    print measured latest value.
    """
    print("")
    print("Time measured:" + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print("Temperature:" + str(int(hex(data[9])+format(data[8], 'x'), 16)/100))
    print("Relative humidity:" + str(int(hex(data[11])+format(data[10], 'x'), 16)/100))
    print("Ambient light:" + str(int(hex(data[13])+format(data[12], 'x'), 16)))
    print("Barometric pressure:" + str(int(hex(data[17])+format(data[16], 'x')+format(data[15], 'x')+format(data[14], 'x'), 16)/1000))
    print("Sound noise:" + str(int(hex(data[19])+format(data[18], 'x'), 16)/100))
    print("eTVOC:" + str(int(hex(data[21])+format(data[20], 'x'), 16)))
    print("eCO2:" + str(int(hex(data[23])+format(data[22], 'x'), 16)))
    print("Discomfort index:" + str(int(hex(data[25])+format(data[24], 'x'), 16)/100))
    print("Heat stroke:" + str(int(hex(data[27])+format(data[26], 'x'), 16)/100))
    print("Vibration information:" + str(int(hex(data[28]), 16)))
    print("SI value:" + str(int(hex(data[30])+format(data[29], 'x'), 16)/10))
    print("PGA:" + str(int(hex(data[32])+format(data[31], 'x'), 16)/10))
    print("Seismic intensity:" + str(int(hex(data[34])+format(data[33], 'x'), 16)/1000))
    print("Temperature flag:" + str(int(hex(data[36])+format(data[35], 'x'), 16)))
    print("Relative humidity flag:" + str(int(hex(data[38])+format(data[37], 'x'), 16)))
    print("Ambient light flag:" + str(int(hex(data[40])+format(data[39], 'x'), 16)))
    print("Barometric pressure flag:" + str(int(hex(data[42])+format(data[41], 'x'), 16)))
    print("Sound noise flag:" + str(int(hex(data[44])+format(data[43], 'x'), 16)))
    print("eTVOC flag:" + str(int(hex(data[46])+format(data[45], 'x'), 16)))
    print("eCO2 flag:" + str(int(hex(data[48])+format(data[47], 'x'), 16)))
    print("Discomfort index flag:" + str(int(hex(data[50])+format(data[49], 'x'), 16)))
    print("Heat stroke flag:" + str(int(hex(data[52])+format(data[51], 'x'), 16)))
    print("SI value flag:" + str(int(hex(data[53]), 16)))
    print("PGA flag:" + str(int(hex(data[54]), 16)))
    print("Seismic intensity flag:" + str(int(hex(data[55]), 16)))


def now_utc_str():
    """
    Get now utc.
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    
    # Serial.
    ser = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE)

    try:
        # LED On. Color of Green.
        command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, DISPLAY_RULE_NORMALLY_ON, 0x00, 0, 255, 0])
        command = command + calc_crc(command, len(command))
        ser.write(command)
        ret = ser.read(14)
        time.sleep(0.1)

        while(ser.isOpen() == True):
            # Get Latest data Long.
            command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
            command = command + calc_crc(command,len(command))
            tmp = ser.write(command)
            time.sleep(1)
            data = ser.read(58)
            print_latest_data(data)
            time.sleep(1)

    except KeyboardInterrupt:
        # LED Off.
        command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, DISPLAY_RULE_NORMALLY_OFF, 0x00, 0, 0, 0])
        command = command + calc_crc(command, len(command))
        ser.write(command)
        time.sleep(1)
        # script finish.
        sys.exit
