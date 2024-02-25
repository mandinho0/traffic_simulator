import pygame


class TrafficLight:
    def __init__(self, x, y, size, angle):
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.colors = {
            'red': (255, 0, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
        }
        self.current_color = None

    def get_position(self):
        return (self.x, self.y)

    def set_color(self, color):
        if color in self.colors:
            self.current_color = color


    def draw(self, screen):
        # Define the dimensions for the traffic light background
        background_width = self.size // 3
        background_height = self.size
        background_x = self.x + self.size // 3

        # Create the traffic light as a separate surface
        traffic_light = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Draw the gray background as a rectangle with smaller spacing
        pygame.draw.rect(traffic_light, (169, 169, 169), (0, 0, background_width, background_height))

        # Define spacing between the circles
        circle_radius = self.size // 6  # Adjust the size of the circles
        spacing = circle_radius // 2

        # Draw the circles for red, yellow, and green
        circle_x = background_width // 2

        for color, pos_y in [('red', circle_radius),
                             ('yellow', 3 * circle_radius),
                             ('green', 5 * circle_radius)]:
            # Draw a simple black outline for all circles
            pygame.draw.circle(traffic_light, (0, 0, 0), (circle_x, pos_y), circle_radius, 2)

            if self.current_color == color:
                # Fill the selected circle with the corresponding color
                pygame.draw.circle(traffic_light, self.colors[color], (circle_x, pos_y), circle_radius - 2)

        # Rotate the traffic light based on the specified angle
        rotated_traffic_light = pygame.transform.rotate(traffic_light, self.angle)

        # Draw the rotated traffic light on the screen
        screen.blit(rotated_traffic_light, (self.x, self.y))