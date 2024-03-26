import time
from Witmotion16chServoDriverV2.Witmotion16chServoDriverV2 import Witmotion16chServoDriverV2
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
    def __init__(self):
        self.driver = Witmotion16chServoDriverV2()

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
        logger.debug(f"Conncted Devices: {Witmotion16chServoDriverV2.list_devices()}")
        return len(Witmotion16chServoDriverV2.list_devices()) > 0 
    
    def open(self, bluetooth=True, *args, **kwargs):
        if bluetooth:
            self.driver.open_bluetooth(*args, **kwargs)
        else:
            self.driver.open_serial(*args, **kwargs)

    def neutralize(self):
        # for motor in self.limbs.values():
        for motor in range(16):
            self.driver.set_position(motor, 90)
        logger.debug("Moved motors to neutral position!")
    
    def jitter(self):
        time.sleep(0.2)
        for motor in range(16):
            self.driver.set_position(motor, 85)
        time.sleep(0.2)
        for motor in range(16):
            self.driver.set_position(motor, 95)

    def validate_limbs(self, limbs):
        for limb, limb_config in limbs.items():
            if not (0 <= limb_config.get("motorPin", None) <= 15):
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
    
    def perform_animation(self, animation):
        chosen_animation = self.animations.get(animation, None)
        if chosen_animation is None:
            raise Exception(f"Animation {animation} not found!")
        
        for pose_entry in chosen_animation:
            pose =pose_entry[0]
            duration = pose_entry[1]
            self.move_to_pose(pose)
            time.sleep(duration / 1000.0) # convert ms to seconds
        
    def move_to_pose(self, pose):
        chosen_pose = self.poses.get(pose, None)
        if chosen_pose is None:
            raise Exception(f"Pose {pose} not found!")
        
        for limb, position in chosen_pose.items():
            self.move_limb(limb, position)

    def move_limb(self, limb, position):
        chosen_lim = self.limbs.get(limb, None)
        if chosen_lim is None:
            raise Exception(f"limb {limb} not found!")
        
        self.driver.set_speed(chosen_lim["motorPin"], chosen_lim["defaultSpeed"])
        self.driver.set_position(chosen_lim["motorPin"], position)


    
    def heartbeat(self):
        return self.driver.heartbeat()

        
        
        
