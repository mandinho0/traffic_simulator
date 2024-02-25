import asyncio

import pygame
import random
import math


class Car:
    def __init__(self, pos, road_side, size, angle, car_image):
        self.pos = pos
        self.angle = angle
        self.road_side = road_side
        self.next_road_side = ''
        self.size = size
        self.car_image = car_image.convert_alpha()
        self.goal = (0, 0)
        self.speed = 5

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        if angle == 360:
            self.angle = 0.0
        else:
            self.angle = angle
        print(self.angle)

    def update_position(self, environment, agent):
        angle = self.angle
        speed = self.speed
        x, y = self.pos

        # select next road_side and change lane if necessary
        if self.is_at_intersection(environment):
            options = ['R', 'L', 'F']
            self.next_road_side = random.choice(options)
            self.change_direction(environment, angle, speed, x, y)

        elif angle == 0:
            if y < 0:
                self.pos = (x, environment.screen_height)
            else:
                self.pos = (x, y - agent.speed)

        elif angle == 90:
            if x < 0:
                self.pos = (environment.screen_width, y)
            else:
                self.pos = (x - agent.speed, y)

        elif angle == 180:
            if y > environment.screen_height:
                self.pos = (x, 0)
            else:
                self.pos = (x, y + agent.speed)

        elif angle == 270:
            if x > environment.screen_width:
                self.pos = (0, y)
            else:
                self.pos = (x + agent.speed, y)

    def change_direction(self, environment, angle, speed, x, y):
        new_road_side = self.road_side

        if angle == 0:
            if self.road_side == 'F':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x, y - speed)
                elif self.next_road_side == 'R':
                    self.pos = (x + (speed * 3), y - speed)
                    new_road_side = 'R'
                elif self.next_road_side == 'L':
                    self.pos = (x - (speed * 3), y - speed)
                    new_road_side = 'L'

            if self.road_side == 'R':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x + (speed * 3), y - (speed * 6))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x + (speed * 3), y - (speed * 3))
                elif self.next_road_side == 'L':
                    self.pos = (x + (speed * 3), y - (speed * 9))
                    new_road_side = 'L'

                self.set_angle(270)

            if self.road_side == 'L':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x - (speed * 3), y - (speed * 15))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x - (speed * 3), y - (speed * 18))
                elif self.next_road_side == 'L':
                    self.pos = (x - (speed * 3), y - (speed * 12))
                    new_road_side = 'L'

                self.set_angle(90)

        if angle == 90:
            if self.road_side == 'F':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x - speed, y)
                elif self.next_road_side == 'R':
                    self.pos = (x - (speed * 3), y - (speed * 3))
                    new_road_side = 'R'
                elif self.next_road_side == 'L':
                    self.pos = (x - (speed * 3), y + (speed * 3))
                    new_road_side = 'L'

            if self.road_side == 'R':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x - (speed * 6), y - (speed * 3))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x - (speed * 3), y - (speed * 3))
                elif self.next_road_side == 'L':
                    self.pos = (x - (speed * 9), y - (speed * 3))
                    new_road_side = 'L'

                self.set_angle(0)

            if self.road_side == 'L':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x - (speed * 15), y + (speed * 3))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x - (speed * 18), y + (speed * 3))
                elif self.next_road_side == 'L':
                    self.pos = (x - (speed * 12), y + (speed * 3))
                    new_road_side = 'L'

                self.set_angle(180)

        if angle == 180:
            if self.road_side == 'F':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x, y + speed)
                elif self.next_road_side == 'R':
                    self.pos = (x - (speed * 3), y + speed)
                    new_road_side = 'R'
                elif self.next_road_side == 'L':
                    self.pos = (x + (speed * 3), y + speed)
                    new_road_side = 'L'

            if self.road_side == 'R':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x - (speed * 3), y + (speed * 6))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x - (speed * 3), y + (speed * 3))
                elif self.next_road_side == 'L':
                    self.pos = (x - (speed * 3), y + (speed * 9))
                    new_road_side = 'L'

                self.set_angle(90)

            if self.road_side == 'L':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x + (speed * 3), y + (speed * 15))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x + (speed * 3), y + (speed * 18))
                elif self.next_road_side == 'L':
                    self.pos = (x + (speed * 3), y + (speed * 12))
                    new_road_side = 'L'

                self.set_angle(270)

        if angle == 270:
            if self.road_side == 'F':
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x + speed, y)
                elif self.next_road_side == 'R':
                    self.pos = (x + (speed * 3), y + (speed * 3))
                    new_road_side = 'R'
                elif self.next_road_side == 'L':
                    self.pos = (x + (speed * 3), y - (speed * 3))
                    new_road_side = 'L'

            if self.road_side == 'R':
                y = y - speed
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x + (speed * 6), y + (speed * 3))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x + (speed * 3), y + (speed * 3))
                elif self.next_road_side == 'L':
                    self.pos = (x + (speed * 9), y + (speed * 3))
                    new_road_side = 'L'

                self.set_angle(180)

            if self.road_side == 'L':
                new_y = y - speed
                speed = speed * 2

                if self.next_road_side == 'F':
                    self.pos = (x + (speed * 15), new_y - (speed * 3))
                    new_road_side = 'F'
                elif self.next_road_side == 'R':
                    self.pos = (x + (speed * 18), new_y - (speed * 3))
                elif self.next_road_side == 'L':
                    self.pos = (x + (speed * 12), new_y - (speed * 3))
                    new_road_side = 'L'

                self.set_angle(0)

        self.road_side = new_road_side

    def is_at_intersection(self, environment):
        x, y = self.pos
        margin = self.speed
        intersection_points = environment.get_intersection_points()

        for intersection_point in intersection_points:
            if abs(x - intersection_point[0]) < margin and abs(y - intersection_point[1]) < margin:
                return True

        return False

    def turnOrFront(self, environment):
        angle = self.angle
        speed = self.speed

        while True:
            x, y = new_x, new_y = self.pos

            if angle == 0:
                new_y = y - (2 * speed)
                #self.set_angle(self.get_angle() + 270)

            if angle == 90:
                new_x = x - (2 * speed)
                self.set_angle(self.get_angle() - 90)

            if angle == 180:
                new_y = y + (2 * speed)
                self.set_angle(self.get_angle() - 90)

            if angle == 270:
                new_x = x + (2 * speed)
                self.set_angle(self.get_angle() - 90)

            # moving
            self.pos = (new_x, new_y)
            break


        # Atualiza a representação visual do carro no ambiente
        #environment.rebuild_map()

    def draw(self, screen):
        # Rotate the car image based on the angle of the Car instance
        rotated_car = pygame.transform.rotate(self.car_image, self.angle)
        rotated_car = pygame.transform.scale(rotated_car, (self.size, self.size))
        screen.blit(rotated_car, self.pos)
