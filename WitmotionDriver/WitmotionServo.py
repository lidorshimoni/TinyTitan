""" Driver for Witmotion Servo Controller boards """

from __future__ import annotations
from typing import List, Optional # remove at python 3.9
import serial
from serial.tools import list_ports

WITMOTION_VID = 0x1a86
WITMOTION_PID = 0x7523

class WitmotionServo():
    """ Class for controlling Witmotion Servo Controller boards """

    @classmethod
    def list_devices(cls):
        ports = serial.tools.list_ports.comports()
        results = []
        for port in sorted(ports):
            if port.vid == WITMOTION_VID and port.pid == WITMOTION_PID:
                results.append(port)
        return results

    def __init__(self, serial_number: Optional[str]=None, channels: int=16) -> None:
        """ Creates the hid device object
        :param serial: Optional serial number of device to connect
        :param channels: Optional number of channels the board has
        """
        self.device = None
        self.serial_number = serial_number
        self.channels = channels

    def open(self) -> WitmotionServo:
        """ Connects to the device
        device.open will raise IOError if it can't connect

        :returns: itself, facilitating method chaining
        """
        for device in self.list_devices():
            if self.serial_number is None or device.serial_number == self.serial_number:
                self.device = serial.Serial(
                    port='COM3',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )   
                return self
        raise Exception("No Device Found")

    def close(self) -> None:
        """ Closes the device """
        self.device.close()

    def heartbeat(self, timeout: float=0.1) -> List[int]:
        """ Sends the heartbeat
        :param timeout: time to wait for response before returning
        :returns: the status value array
        """
        self.device.write([0xff, 0x00, 0x12] + [0]*2)
        answer = self.device.read(5)
        if answer:
            if answer == bytes([0xff, 0xf0, 0x12] + [0]*2):
                return True
            raise Exception(f"Bad keepalive response: {answer}")
        # return False
        raise TimeoutError("Read value timed out")

    def set_position(self, channel: int, value: int) -> None:
        """ Sends servo position request
        :param channel: the channel of the servo to send
        :param value: the value (0-180) to send
        """
        if channel < 0 or channel >= self.channels:
            raise ValueError(f"Channel out of range (0, {self.channels-1})")

        if (value < 0 or value > 180):
            raise ValueError("Value out of range: (0, 180)")
        value *= (2000/180.0)
        value+=500
        value = int(value)
        datal = value & 0xff 
        datah = value >> 8
        self.device.write([0xff, 0x02, channel, datal, datah] )

    def set_speed(self, channel: int, value: int) -> None:
        """ Sends servo position request
        The actual speed value is 9*value degrees per second.
        e.g. speed value 15 is 135 degres per second

        :param channel: the channel of the servo to send
        :param value: the speed value (0-0xff)
        """
        if channel < 0 or channel >= self.channels:
            raise ValueError(f"Channel out of range (0, {self.channels-1})")

        if value < 1 or value > 0xff:
            raise ValueError("Value out of range: (0, 0xff)")

        self.device.write([0xff, 0x01, channel, value, 0x00])

    def execute_action_group(self, action_group: int) -> None:
        """ Executes an action group
        :param action_group: the action_group to execute (1-16)
        """
        if action_group < 1 or action_group > 16:
            raise ValueError("Action Group out of range (1, 16)")

        self.device.write([0xff, 0x09, 0x00, action_group, 0x00])

    def emergency_stop(self) -> None:
        """ Sends the emergency stop command """

        self.device.write([0xff, 0x0b, 0x00, 0x01, 0x00] + [0]*56)

    def emergency_recovery(self) -> None:
        """ Sends the recover from emergency command """

        self.device.write([0xff, 0x0b, 0x00, 0x00, 0x00] + [0]*56)

    def upload_action(self, action):
        raise NotImplementedError()
        # start action learning
        self.device.write([0xff, 0xfb, 0x00, 0x01, 0x00] + [0]*56)


        # stop action learning
        self.device.write([0xff, 0xfb, 0x00, 0x00, 0x00] + [0]*56)

    def erase(self):
        raise NotImplementedError()
        self.device.write([0xff, 0xfa, 0x00, 0x01, 0x00] + [0]*56)
        self.device.write([0xff, 0xfa, 0x00, 0x00, 0x00] + [0]*56)
        