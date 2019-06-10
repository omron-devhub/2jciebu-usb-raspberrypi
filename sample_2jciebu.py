import serial
import time
from datetime import datetime
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
            if (carrayFlag == 1):
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    return (bytearray([crcL, crcH]))


def print_latest_data(data):
    """
    print measured latest value.
    """
    time_measured = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    temperature = str(int(hex(data[9]) + '{:02x}'.format(data[8], 'x'), 16) / 100)
    relative_humidity = str(int(hex(data[11]) + '{:02x}'.format(data[10], 'x'), 16) / 100)
    ambient_light = str(int(hex(data[13]) + '{:02x}'.format(data[12], 'x'), 16))
    barometric_pressure = str(int(hex(data[17]) + '{:02x}'.format(data[16], 'x')
                                  + '{:02x}'.format(data[15], 'x') + '{:02x}'.format(data[14], 'x'), 16) / 1000)
    sound_noise = str(int(hex(data[19]) + '{:02x}'.format(data[18], 'x'), 16) / 100)
    eTVOC = str(int(hex(data[21]) + '{:02x}'.format(data[20], 'x'), 16))
    eCO2 = str(int(hex(data[23]) + '{:02x}'.format(data[22], 'x'), 16))
    discomfort_index = str(int(hex(data[25]) + '{:02x}'.format(data[24], 'x'), 16) / 100)
    heat_stroke = str(int(hex(data[27]) + '{:02x}'.format(data[26], 'x'), 16) / 100)
    vibration_information = str(int(hex(data[28]), 16))
    si_value = str(int(hex(data[30]) + '{:02x}'.format(data[29], 'x'), 16) / 10)
    pga = str(int(hex(data[32]) + '{:02x}'.format(data[31], 'x'), 16) / 10)
    seismic_intensity = str(int(hex(data[34]) + '{:02x}'.format(data[33], 'x'), 16) / 1000)
    temperature_flag = str(int(hex(data[36]) + '{:02x}'.format(data[35], 'x'), 16))
    relative_humidity_flag = str(int(hex(data[38]) + '{:02x}'.format(data[37], 'x'), 16))
    ambient_light_flag = str(int(hex(data[40]) + '{:02x}'.format(data[39], 'x'), 16))
    barometric_pressure_flag = str(int(hex(data[42]) + '{:02x}'.format(data[41], 'x'), 16))
    sound_noise_flag = str(int(hex(data[44]) + '{:02x}'.format(data[43], 'x'), 16))
    etvoc_flag = str(int(hex(data[46]) + '{:02x}'.format(data[45], 'x'), 16))
    eco2_flag = str(int(hex(data[48]) + '{:02x}'.format(data[47], 'x'), 16))
    discomfort_index_flag = str(int(hex(data[50]) + '{:02x}'.format(data[49], 'x'), 16))
    heat_stroke_flag = str(int(hex(data[52]) + '{:02x}'.format(data[51], 'x'), 16))
    si_value_flag = str(int(hex(data[53]), 16))
    pga_flag = str(int(hex(data[54]), 16))
    seismic_intensity_flag = str(int(hex(data[55]), 16))
    print("")
    print("Time measured:" + time_measured)
    print("Temperature:" + temperature)
    print("Relative humidity:" + relative_humidity)
    print("Ambient light:" + ambient_light)
    print("Barometric pressure:" + barometric_pressure)
    print("Sound noise:" + sound_noise)
    print("eTVOC:" + eTVOC)
    print("eCO2:" + eCO2)
    print("Discomfort index:" + discomfort_index)
    print("Heat stroke:" + heat_stroke)
    print("Vibration information:" + vibration_information)
    print("SI value:" + si_value)
    print("PGA:" + pga)
    print("Seismic intensity:" + seismic_intensity)
    print("Temperature flag:" + temperature_flag)
    print("Relative humidity flag:" + relative_humidity_flag)
    print("Ambient light flag:" + ambient_light_flag)
    print("Barometric pressure flag:" + barometric_pressure_flag)
    print("Sound noise flag:" + sound_noise_flag)
    print("eTVOC flag:" + etvoc_flag)
    print("eCO2 flag:" + eco2_flag)
    print("Discomfort index flag:" + discomfort_index_flag)
    print("Heat stroke flag:" + heat_stroke_flag)
    print("SI value flag:" + si_value_flag)
    print("PGA flag:" + pga_flag)
    print("Seismic intensity flag:" + seismic_intensity_flag)


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
        time.sleep(0.1)
        ret = ser.read(ser.inWaiting())

        while ser.isOpen():
            # Get Latest data Long.
            command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
            command = command + calc_crc(command, len(command))
            tmp = ser.write(command)
            time.sleep(0.1)
            data = ser.read(ser.inWaiting())
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
