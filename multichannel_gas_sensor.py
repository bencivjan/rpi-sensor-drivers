#!/usr/bin/env python

import time
import smbus

class MultichannelGasSensor:
    def __init__(self, address=0x08):
        self.address = address
        self.bus = smbus.SMBus(1)  # Raspberry Pi I2C Bus 1

        self.adcValueR0_NH3_Buf = 0
        self.adcValueR0_CO_Buf = 0
        self.adcValueR0_NO2_Buf = 0

        print("Initializing Multi-channel Gas Sensor...")

        try:
            # Power ON and set LED
            self.bus.write_word_data(self.address, 11, 1)
            self.bus.write_word_data(self.address, 10, 1)
            time.sleep(1)
            print("Sensor Initialized.")
        except IOError:
            print("Error: Unable to communicate with sensor. Check I2C connection.")

    def get_sensor_data(self):
        """Read sensor values for NH3, CO, and NO2"""
        try:
            # nh3 = self.get_addr_dta(0x08)   # NH3
            co = self.get_addr_dta(0x07)   # CO (Carbon Monoxide)
            no2 = self.get_addr_dta(0x01)  # NO2 (Nitrogen Dioxide)
            voc = self.get_addr_dta(0x05)  # VOC (Volatile Organic Compounds)
            c2h5ch = self.get_addr_dta(0x03) # C2H5CH (Ethyl alcohol)
            return {"CO": co, "NO2": no2, "VOC": voc, "C2H5CH": c2h5ch}
        except IOError:
            print("Error: Failed to read from sensor.")
            return None

    def get_addr_dta(self, addr_reg):
        """Fetch gas concentration data from the sensor"""
        try:
            self.bus.write_byte(self.address, addr_reg)
            time.sleep(0.1)  # Allow sensor to respond
            data = self.bus.read_i2c_block_data(self.address, addr_reg, 2)

            value = (data[0] << 8) | data[1]  # Combine two bytes
            return value
        except IOError:
            print(f"Error: Failed to read data from register {addr_reg}.")
            return None

if __name__ == "__main__":
    sensor = MultichannelGasSensor()

    while True:
        data = sensor.get_sensor_data()
        if data:
            print(f"CO: {data['CO']}, NO2: {data['NO2']}, VOC: {data['VOC']}, C2H5CH: {data['C2H5CH']}")
        time.sleep(1)  # Wait 1 second before the next read
