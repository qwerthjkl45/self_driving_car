import carla
import json
import math
import os
import random
import sys
import time

from abc import ABCMeta, abstractmethod
     
class Tesla():

    bp = None
    actor = None
    world = None
    camera_configs = {}
    cameras = {}

    def __init__(self, world):

        self.world = world

        blueprint_library = self.world.get_blueprint_library()
        self.bp = random.choice(blueprint_library.filter('tesla'))

        self.camera_configs = {
            "front_camera": self.load_config(os.path.join("sensors", "camera", "front_camera.json")),
            "rear_camera": self.load_config(os.path.join("sensors", "camera", "rear_camera.json"))
        }

        self.init_car()

    def init_car(self):

        self.bp.set_attribute('color', "255,255,255")
        transform = self.world.get_spectator().get_transform()
        self.actor = self.world.spawn_actor(self.bp, transform)    

        self.init_sensors()

    def init_sensors(self):
        self.init_cameras()
        self.init_gnss()

    def save_image(self, image, path):
        print(path)
        image.save_to_disk(path)

    def init_cameras(self):

        for camera_name, camera_config in self.camera_configs.items():
            cam_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')

            for attr_name, attr_value in camera_config['intrinsics'].items():
                cam_bp.set_attribute(attr_name, str(attr_value))
            
            location = (camera_config["x"], camera_config["y"], camera_config["z"])
            rotation = (camera_config["pitch"], camera_config["yaw"], camera_config["roll"])
            
            cam_location = carla.Location(*location)
            cam_rotation = carla.Rotation(*rotation)
            cam_transform = carla.Transform(cam_location, cam_rotation) 
            
            self.cameras[camera_name] = self.world.spawn_actor(cam_bp, cam_transform, attach_to=self.actor)
            #self.cameras[camera_name].listen(lambda image: image.save_to_disk('./outputs/' + camera_name + '%.6d.jpg' % image.frame_number))
            if camera_name == "front_camera":
                self.cameras[camera_name].listen(lambda image: self.save_image(image, './outputs/' + "front + '1.jpg'))
            else:
                self.cameras[camera_name].listen(lambda image: self.save_image(image, './outputs/' + "back" + '1.jpg'))


        print(self.cameras)

    def init_gnss(self):
        pass

    def load_config(self, path):
        with open(path) as f:
            return json.load(f)

    def drive(self, method="autopilot"):

        if method == "autopilot":
            self.actor.set_autopilot(True)
        else:
            raise NotImplementedError("no such MMMMMMMMMMMMM")
def main():

    print("CHUCHU")

    # First of all, we need to create the client that will send the requests
    # to the simulator. Here we'll assume the simulator is accepting
    # requests in the localhost at port 2000.
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    # Once we have a client we can retrieve the world that is currently
    # running.
    world = client.get_world()

    tesla = Tesla(world)
    tesla.drive()

    while True:
        world_snapshot = world.wait_for_tick()


if __name__ == '__main__':

    main()
