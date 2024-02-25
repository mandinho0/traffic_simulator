import asyncio
import random
import sys
import numpy as np
import pygame

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class CarBase(Agent):
    def __init__(self, id, environment, car_image):
        jid = "car_" + str(id) + "@localhost"
        super().__init__(jid, 'pass')

        x, y, road_side, angle = (350, 160, 'R', 0) # self.get_unique_start_point()
        pos = (x, y)
        self.environment = environment
        self.pos = pos
        self.road_side = road_side
        self.size = 30
        self.angle = angle
        self.car_image = car_image
        self.goal = (0, 0)
        self.speed = 5
        self.car_position = self.environment.add_car_position(jid, pos, road_side, self.size, angle, car_image)

    def get_start_points(self):
        start_points = [
            # Horizontal -->
            (0, 115, 270.0), (200, 115, 270.0), (600, 115, 270.0), (1000, 115, 270.0),
            (100, 465, 270.0), (300, 465, 270.0), (400, 465, 270.0), (850, 465, 270.0),
            (50, 815, 270.0), (500, 815, 270.0), (800, 815, 270.0), (1100, 815, 270.0),
            # Horizontal <--
            (200, 95, 90.0), (500, 95, 90.0), (800, 95, 90.0), (1200, 95, 90.0),
            (100, 445, 90.0), (400, 445, 90.0), (700, 445, 90.0), (1100, 445, 90.0),
            (125, 795, 90.0), (450, 795, 90.0), (900, 795, 90.0), (860, 795, 90.0),

            # Vertical toDown
            (155, 200, 180.0), (195, 250, 180.0), (195, 775, 180.0),
            (595, 35, 180.0), (595, 300, 180.0), (595, 775, 180.0),
            (995, 120, 180.0), (995, 400, 180.0), (995, 775, 180.0),
            (1395, 150, 180.0), (1395, 350, 180.0), (1395, 775, 180.0),
            # Vertical toUp
            (215, 100, 0.0), (215, 250, 0.0), (215, 600, 0.0),
            (615, 120, 0.0), (615, 275, 0.0), (615, 700, 0.0),
            (1015, 200, 0.0), (1015, 300, 0.0), (1015, 750, 0.0),
            (1415, 50, 0.0), (1415, 155, 0.0), (1415, 775, 0.0),
        ]

        return start_points

    def get_unique_start_point(self):
        start_points = self.get_start_points()

        if not start_points:
            raise ValueError("No more unique start points available")

        selected_point = random.choice(start_points)
        start_points.remove(selected_point)

        return selected_point

    async def setup(self):
        class ReceiveBehav(CyclicBehaviour):
            def __init__(self, agent):
                super().__init__()
                self.agent = agent
                #dest_x, dest_y = self.random_valid_goal()
                #self.set_goal(dest_x, dest_y)
                #self.agent.environment.add_goal(self.agent.goal)

            async def run(self):
                await self.move()

            def get_available_roads(self):
                return self.agent.environment.roads

            def create_road_matrix(self, grid_width, grid_height):
                road_info_list = self.agent.environment.get_roads_info()
                grid = np.zeros((grid_height, grid_width), dtype=int)

                for road_info in road_info_list:
                    start_x = road_info["start_x"]
                    start_y = road_info["start_y"]
                    end_x = road_info["end_x"]
                    end_y = road_info["end_y"]

                    grid[start_y:end_y, start_x:end_x] = 1

                return grid

            async def move(self):
                environment = self.agent.environment
                time_interval = 0.1

                environment.update_car_position(self.agent, environment)

                await asyncio.sleep(time_interval)

            def is_in_street(self, x, y):
                for street in self.get_available_roads():
                    rs, start_x, start_y, end_x, end_y, width, angle, road_divider = street

                    if start_x <= x <= end_x and start_y <= y <= end_y:
                        return True

                return False

            def get_available_positions(self):
                return [(rs[1], rs[2]) for rs in self.get_available_roads()] + [(rs[3], rs[4]) for rs in self.get_available_roads()]

            def set_goal(self, dest_x, dest_y):
                print(dest_x, dest_y)
                self.agent.goal = (dest_x, dest_y)

            def random_valid_goal(self):
                available_roads = self.get_available_roads()

                if not available_roads:
                    return (0, 0)

                selected_road = random.choice(available_roads)

                surface, start_x, start_y, end_x, end_y, width, angle, road_divider = selected_road
                selected_lane = (end_x - width, start_y, end_x, end_y)

                x = random.randint(selected_lane[0], selected_lane[2])
                y = random.randint(selected_lane[1], selected_lane[3])

                return (x, y)

            def is_goal_valid(self, dest_x, dest_y):
                available_positions = self.get_available_positions()
                return (dest_x, dest_y) in available_positions

            def exit(self):
                pygame.quit()
                sys.exit()

        behaviour = ReceiveBehav(self)
        self.add_behaviour(behaviour)
