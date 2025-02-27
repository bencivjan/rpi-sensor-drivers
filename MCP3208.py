import platform
import os
import time

import Adafruit_GPIO.SPI as SPI

class MCP3208(object):
    def __init__(self):
        self.spi = SPI.SpiDev(0, 0, max_speed_hz=1000000)
        self.spi.set_mode(0)
        self.spi.set_bit_order(SPI.MSBFIRST)

    def __del__(self):
        self.spi.close()

    def read(self, ch):
        if 7 < ch or ch < 0:
            raise Exception('MCP3208 channel must be 0-7: ' + str(ch))
        
        cmd = 128  # 1000 0000
        cmd += 64  # 1100 0000
        cmd += ((ch & 0x07) << 3)
        ret = self.spi.transfer([cmd, 0x0, 0x0])

        # get the 12b out of the return
        val = (ret[0] & 0x01) << 11  # only B11 is here
        val |= ret[1] << 3           # B10:B3
        val |= ret[2] >> 5           # MSB has B2:B0 ... need to move down to LSB

        return (val & 0x0FFF)  # ensure we are only sending 12b

if __name__ == "__main__":
    hat = MCP3208()

    print('Reading MCP3208 values, press Ctrl-C to quit...')
    # Print nice channel column headers.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
    print('-' * 57)
    # Main program loop.
    while True:
        # Read all the ADC channel values in a list.
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = hat.read(i)
        # Print the ADC values.
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        # Pause for half a second.
        time.sleep(0.5)