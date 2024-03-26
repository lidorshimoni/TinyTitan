import time
from WitmotionDriver.WitmotionServo import WitmotionServo
import json
import logging

logger = logging.Logger(__name__)

class LimMovement:
    def __init__(self, angle, speed=0xff):
        self.angle = 90
        self.speed = 0xff

class Action:
    def __init__(self, lim_movements=[]):
        self.movements = lim_movements
    
    def add(self, movement):
        self.movements += movement
        return self

class TinyTitan:
    def __init__(self, should_open_device=True):
        self.driver = WitmotionServo()
        if should_open_device:
            self.driver.open()
        self.config = {}
        self.limbs = {}
        self.poses = {}
        self.animations = {}
        self.load_config()
        self.load_poses()
        self.load_animations()
        logger.debug("TinyTitan Created!")

    @classmethod
    def is_connected(cls):
        logger.debug(f"Conncted Devices: {WitmotionServo.list_devices()}")
        return len(WitmotionServo.list_devices()) > 0 
    
    def neutralize(self):
        # for motor in self.limbs.values():
        for motor in range(16):
            self.driver.set_position(motor, 1000)
        logger.debug("Moved motors to neutral position!")
    
    def jitter(self):
        time.sleep(0.2)
        for motor in range(16):
            self.driver.set_position(motor, 900)
        time.sleep(0.2)
        for motor in range(16):
            self.driver.set_position(motor, 1100)

    def validate_limbs(self, limbs):
        for limb, limb_config in limbs.items():
            if not (0 < limb_config.get("motorPin", None) < 16):
                raise Exception("Motor Pin on limb {limb} is not in range! (0-16)")

    def validate_poses(self, poses):
        if not set([i for l in map(poses.values()) for i in l]).issubset(self.limbs):
            raise Exception("Pose contains an unknown limb!")

    def load_animations(self):
        with open("Animations.json") as f:
            self.animations = json.load(f)
    
    def load_poses(self):
        with open("Poses.json") as f:
            self.poses = json.load(f)

    def load_config(self):
        with open("TinyTitanConfig.json") as f:
            self.config = json.load(f)
        limbs = self.config.get("limbs", {})
        self.validate_limbs(limbs)
        self.limbs = limbs
        
        
        
        
