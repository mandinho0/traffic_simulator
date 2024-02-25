import math
import sys

import pygame
from pygame.locals import *

from Map.car import Car
from Map.traficclass import TrafficLight

class Environment:
    def __init__(self):
        # Initialize environment variables
        self.cars = {}
        self.traffic_lights = {}
        self.light_status = {}

        # Initialize Pygame
        pygame.init()

        # Define screen dimensions
        self.screen_width, self.screen_height = 1600, 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Define colors
        self.green = (0, 255, 0)
        self.gray = (128, 128, 128)
        self.white = (255, 255, 255)

        #
        self.street_width = 60

        # Create a list to store road instances
        self.roads = []

        self.build_map()

    def get_roads_info(self):
        return {
            # horizontal roads
            'H': {
                (0, 1600, 185, 335),
                (0, 1600, 535, 685)
            },

            # vertical roads
            'V': {
                (200, 350, 0, 1000),
                (700, 850, 0, 1000),
                (1200, 1350, 0, 1000),
            }
        }

    def get_intersection_points(self):
        return {
            # Vertical Intersections
            # Down Direction
            # Road 1
            (200, 160, 'R'), (200, 510, 'R'),
            (230, 160, 'F'), (230, 510, 'F'),
            (260, 160, 'L'), (260, 510, 'L'),
            # Road 2
            (700, 160, 'R'), (700, 510, 'R'),
            (730, 160, 'F'), (730, 510, 'F'),
            (760, 160, 'L'), (760, 510, 'L'),
            # Road 3
            (1200, 160, 'R'), (1200, 510, 'R'),
            (1230, 160, 'F'), (1230, 510, 'F'),
            (1260, 160, 'L'), (1260, 510, 'L'),

            # Up Direction
            # Road 1
            (290, 370, 'L'), (290, 720, 'L'),
            (320, 370, 'F'), (320, 720, 'F'),
            (350, 370, 'R'), (350, 720, 'R'),
            # Road 2
            (790, 370, 'L'), (790, 720, 'L'),
            (820, 370, 'F'), (820, 720, 'F'),
            (850, 370, 'R'), (850, 720, 'R'),
            # Road 3
            (1290, 370, 'L'), (1290, 720, 'L'),
            (1320, 370, 'F'), (1320, 720, 'F'),
            (1350, 370, 'R'), (1350, 720, 'R'),

            # Horizontal Intersections
            # Right Direction
            # Road 1
            (170, 280, 'L'), (670, 280, 'L'), (1170, 280, 'L'),
            (170, 310, 'F'), (670, 310, 'F'), (1170, 310, 'F'),
            (170, 340, 'R'), (670, 340, 'R'), (1170, 340, 'R'),
            # Road 2
            (170, 630, 'L'), (670, 630, 'L'), (1170, 630, 'L'),
            (170, 660, 'F'), (670, 660, 'F'), (1170, 660, 'F'),
            (170, 690, 'R'), (670, 690, 'R'), (1170, 690, 'R'),

            # Left Direction
            # Road 1
            (380, 190, 'R'), (880, 190, 'R'), (1380, 190, 'R'),
            (380, 220, 'F'), (880, 220, 'F'), (1380, 220, 'F'),
            (380, 250, 'L'), (880, 250, 'L'), (1380, 250, 'L'),
            # Road 2
            (380, 540, 'R'), (880, 540, 'R'), (1380, 540, 'R'),
            (380, 570, 'F'), (880, 570, 'F'), (1380, 570, 'F'),
            (380, 600, 'L'), (880, 600, 'L'), (1380, 600, 'L'),
        }

    # Add Goal
    def add_goal(self, goal):
        pygame.draw.circle(self.screen, (255, 0, 0), goal, 2)  # Red circle for the goal

        self.render_map()

    # CAR Methods
    #
    def add_car_position(self, car_id, pos, road_side, size, angle, car_image):
        car = Car(pos, road_side, size, angle, car_image)
        car.draw(self.screen)

        self.cars[str(car_id)] = car  # Convert o JID em uma string
        self.render_map()

        return str(car_id)

    def update_car_position(self, car, environment):
        car_id = car.jid

        if str(car_id) in self.cars:
            car = self.cars[str(car_id)]

            # moving car random
            car.update_position(environment, car)

            # refresh map
            # self.rebuild_map()
        else:
            print(f"JID {car_id} não encontrado no dicionário de posições de carros.")

    def get_car_position(self, car_id):
        return self.cars[car_id]

    # TRAFFIC LIGHTS Methods
    #
    def add_traffic_light(self, tf_jid, x, y, size, angle, status):
        traffic_light = TrafficLight(x, y, size, angle)
        traffic_light.set_color(status)
        traffic_light.draw(self.screen)

        self.traffic_lights[str(tf_jid)] = traffic_light

        # self.render_map()
        return traffic_light

    def update_light_status(self, light_id, traffic_light, status):
        self.light_status[light_id] = status

        traffic_light.set_color(status)
        traffic_light.draw(self.screen)

        # self.render_map()

        print("Status of Light {} is now {}".format(light_id, status))

    def get_light_status(self, light_id):
        return self.light_status[light_id]

    # Create Roads Method
    #
    def create_road(self, start_x, start_y, end_x, end_y, width, angle, road_divider='dashed'):
        road_length = int(math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2))
        road = pygame.Surface((road_length, width * 3), pygame.SRCALPHA)

        for i in range(3):
            lane_height = width
            lane_y = i * lane_height
            pygame.draw.rect(road, self.gray, (0, lane_y, road_length, lane_height))

        rotated_road = pygame.transform.rotate(road, angle)
        self.screen.blit(rotated_road, (start_x, start_y))
        self.roads.append((rotated_road, start_x, start_y, end_x, end_y, width))

    # Build Map method
    def build_map(self):
        # # Set the background color to green
        # self.screen.fill(self.green)
        #
        # # Horizontal Roads
        # self.create_road(0, 100, 1600, 100, self.street_width, 0, road_divider="dashed")
        # self.create_road(0, 450, 1600, 450, self.street_width, 0, road_divider="dashed")
        # self.create_road(0, 800, 1600, 800, self.street_width, 0, road_divider="dashed")
        #
        # # Vertical Roads
        # #
        # self.create_road(200, 0, 200, 900, self.street_width, 90, road_divider="dashed")
        # self.create_road(700, 0, 700, 900, self.street_width, 90, road_divider="dashed")
        # self.create_road(1200, 0, 1200, 900, self.street_width, 90, road_divider="dashed")
        #
        # # Draw roads from the list
        # for road in self.roads:
        #     self.screen.blit(road[0], (road[1], road[2]))

        self.screen.fill((0, 0, 0))
        background_image = pygame.image.load("/home/isiauser/Desktop/AI/Map/assets/background/mapa_bg.jpg")
        # Blit the background image onto the screen
        self.screen.blit(background_image, (0, 0))

        # self.render_map()

    # Rebuild map to update car positions
    def rebuild_map(self):
        self.build_map()

        #rint(self.traffic_lights.items())

        # rebuild traffic lights
        for tf_key, tf_instance in self.traffic_lights.items():
            tf_instance.draw(self.screen)


        #rebuild cars
        for c_key, c_instance in self.cars.items():
            c_instance.draw(self.screen)

        self.render_map()


    # Render Map method
    def render_map(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.update()

    def update_map(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.flip()
