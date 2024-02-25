import asyncio
import random

import pygame
import spade

from Agents.Car.CarBase import CarBase
from Agents.TrafficLights.MasterTrafficLightAgent import MasterTrafficLightAgent
from Agents.TrafficLights.TrafficLightAgent import TrafficLightAgent
from Environment.environment import Environment
from Models.CoordinateModel import CoordinateModel


async def main():
    environment = Environment()

    # # Traffic Light Agents
    # # left top
    # tl_1 = TrafficLightAgent("traffic_light1@localhost",
    #                          "trafficlight1pass",
    #                          environment,
    #                          CoordinateModel(240, 840, 40, 0),  # main tl
    #                          CoordinateModel(160, 760, 40, 180),  # front tl
    #                          CoordinateModel(160, 840, 40, 270),  # left tl
    #                          CoordinateModel(240, 760, 40, 90))  # right tl
    #
    # # left mid
    # tl_2 = TrafficLightAgent("traffic_light2@localhost",
    #                          "trafficlight2pass",
    #                          environment,
    #                          CoordinateModel(240, 490, 40, 0),  # main tl
    #                          CoordinateModel(160, 410, 40, 180),  # front tl
    #                          CoordinateModel(160, 490, 40, 270),  # left tl
    #                          CoordinateModel(240, 410, 40, 90))  # right tl
    #
    # # left bottom
    # tl_3 = TrafficLightAgent("traffic_light3@localhost",
    #                          "trafficlight3pass",
    #                          environment,
    #                          CoordinateModel(240, 140, 40, 0),  # main tl
    #                          CoordinateModel(160, 60, 40, 180),  # front tl
    #                          CoordinateModel(160, 140, 40, 270),  # left tl
    #                          CoordinateModel(240, 60, 40, 90))  # right tl
    #
    # # mid left top
    # tl_4 = TrafficLightAgent("traffic_light4@localhost",
    #                          "trafficlight4pass",
    #                          environment,
    #                          CoordinateModel(640, 840, 40, 0),  # main tl
    #                          CoordinateModel(560, 760, 40, 180),  # front tl
    #                          CoordinateModel(560, 840, 40, 270),  # left tl
    #                          CoordinateModel(640, 760, 40, 90))  # right tl
    #
    # # mid left middle
    # tl_5 = TrafficLightAgent("traffic_light5@localhost",
    #                          "trafficlight5pass",
    #                          environment,
    #                          CoordinateModel(640, 490, 40, 0),  # main tl
    #                          CoordinateModel(560, 410, 40, 180),  # front tl
    #                          CoordinateModel(560, 490, 40, 270),  # left tl
    #                          CoordinateModel(640, 410, 40, 90))  # right tl
    #
    # # mid left bottom
    # tl_6 = TrafficLightAgent("traffic_light6@localhost",
    #                          "trafficlight6pass",
    #                          environment,
    #                          CoordinateModel(640, 140, 40, 0),  # main tl
    #                          CoordinateModel(560, 60, 40, 180),  # front tl
    #                          CoordinateModel(560, 140, 40, 270),  # left tl
    #                          CoordinateModel(640, 60, 40, 90))  # right tl
    #
    # # mid right top
    # tl_7 = TrafficLightAgent("traffic_light7@localhost",
    #                          "trafficlight7pass",
    #                          environment,
    #                          CoordinateModel(1040, 840, 40, 0),  # main tl
    #                          CoordinateModel(960, 760, 40, 180),  # front tl
    #                          CoordinateModel(960, 840, 40, 270),  # left tl
    #                          CoordinateModel(1040, 760, 40, 90))  # right tl
    #
    # # mid right middle
    # tl_8 = TrafficLightAgent("traffic_light8@localhost",
    #                          "trafficlight8pass",
    #                          environment,
    #                          CoordinateModel(1040, 490, 40, 0),  # main tl
    #                          CoordinateModel(960, 410, 40, 180),  # front tl
    #                          CoordinateModel(960, 490, 40, 270),  # left tl
    #                          CoordinateModel(1040, 410, 40, 90))  # right tl
    #
    # # mid right bottom
    # tl_9 = TrafficLightAgent("traffic_light9@localhost",
    #                          "trafficlight9pass",
    #                          environment,
    #                          CoordinateModel(1040, 140, 40, 0),  # main tl
    #                          CoordinateModel(960, 60, 40, 180),  # front tl
    #                          CoordinateModel(960, 140, 40, 270),  # left tl
    #                          CoordinateModel(1040, 60, 40, 90))  # right tl
    #
    # # right top
    # tl_10 = TrafficLightAgent("traffic_light10@localhost",
    #                           "trafficlight10pass",
    #                           environment,
    #                           CoordinateModel(1440, 840, 40, 0),  # main tl
    #                           CoordinateModel(1360, 760, 40, 180),  # front tl
    #                           CoordinateModel(1360, 840, 40, 270),  # left tl
    #                           CoordinateModel(1440, 760, 40, 90))  # right tl
    #
    # # right middle
    # tl_11 = TrafficLightAgent("traffic_light11@localhost",
    #                           "trafficlight1pass",
    #                           environment,
    #                           CoordinateModel(1440, 490, 40, 0),  # main tl
    #                           CoordinateModel(1360, 410, 40, 180),  # front tl
    #                           CoordinateModel(1360, 490, 40, 270),  # left tl
    #                           CoordinateModel(1440, 410, 40, 90))  # right tl
    #
    # # right bottom
    # tl_12 = TrafficLightAgent("traffic_light12@localhost",
    #                           "trafficlight12pass",
    #                           environment,
    #                           CoordinateModel(1440, 140, 40, 0),  # main tl
    #                           CoordinateModel(1360, 60, 40, 180),  # front tl
    #                           CoordinateModel(1360, 140, 40, 270),  # left tl
    #                           CoordinateModel(1440, 60, 40, 90))  # right tl

    # await tl_1.start(auto_register=True)
    # await tl_2.start(auto_register=True)
    # await tl_3.start(auto_register=True)
    # await tl_4.start(auto_register=True)
    # await tl_5.start(auto_register=True)
    # await tl_6.start(auto_register=True)
    # await tl_7.start(auto_register=True)
    # await tl_8.start(auto_register=True)
    # await tl_9.start(auto_register=True)
    # await tl_10.start(auto_register=True)
    # await tl_11.start(auto_register=True)
    # await tl_12.start(auto_register=True)


    # Car Agents
    car_images = [
        pygame.image.load("Map/assets/cars/base/blue.png"),
        pygame.image.load("Map/assets/cars/base/red.png"),
        pygame.image.load("Map/assets/cars/base/yellow.png"),
        pygame.image.load("Map/assets/cars/base/green.png"),
    ]

    for id in range(50):
        car = CarBase(id, environment, random.choice(car_images))
        await car.start(auto_register=True)

    while True:
        environment.rebuild_map()
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    spade.run(main())
