import os
import sys
import carla

import random
import time

def main():

    actor_list = []

    # First of all, we need to create the client that will send the requests
    # to the simulator. Here we'll assume the simulator is accepting
    # requests in the localhost at port 2000.
    client = carla.Client('localhost', 3000)
    client.set_timeout(2.0)

    # Once we have a client we can retrieve the world that is currently
    # running.
    world = client.get_world()

    # The world contains the list blueprints that we can use for adding new
    # actors into the simulation.
    blueprint_library = world.get_blueprint_library()

    bp = random.choice(blueprint_library.filter('tesla'))
    bp.set_attribute('color', "255,255,255")

    transform = world.get_spectator().get_transform()

    our_tesla = world.spawn_actor(bp, transform)    
    our_tesla.set_autopilot(True)


if __name__ == '__main__':

    main()