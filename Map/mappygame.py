import pygame
import sys
import traficclass


# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
green = (0, 255, 0)
gray = (128, 128, 128)
white = (255, 255, 255)

# Create a list to store road instances
roads = []

# Function to create a road and add it to the list
def create_road(x, y, width, height, angle, road_divider="solid"):
    road = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(road, gray, (0, 0, width, height))

    if road_divider == "solid":
        divider_width = 5  # Width of the solid divider
        pygame.draw.rect(road, white, (0, height // 2 - divider_width // 2, width, divider_width))
    elif road_divider == "dashed":
        divider_width = 15  # Width of each dash
        divider_height = 2
        dash_gap = 10  # Gap between dashes
        num_dashes = width // (divider_width + dash_gap)

        for i in range(num_dashes):
            if i % 2 == 0:  # Draw dashes on even indices to create dashed effect
                pygame.draw.rect(road, white, (i * (divider_width + dash_gap), height // 2 - divider_height // 2, divider_width, divider_height))

    rotated_road = pygame.transform.rotate(road, angle)
    screen.blit(rotated_road, (x, y))
    roads.append((rotated_road, x, y))
def create_train_tracks(x, y, width, height):
    tracks = pygame.Surface((width, height), pygame.SRCALPHA)
    # Fill the background with yellow color (sand-like background)
    pygame.draw.rect(tracks, (255, 255, 0), (0, 0, width, height))

    # Draw several horizontal brown stripes based on the height
    stripe_height = 20  # Adjust the height of each stripe as desired
    num_stripes = height // stripe_height
    for i in range(num_stripes):
        if i % 2 == 0:
            pygame.draw.rect(tracks, (139, 69, 19), (10, i * stripe_height, width - 20, stripe_height))  # Subtract 20 from both sides

    # Draw two vertical black stripes
    stripe_width = 20  # Width of black stripes
    pygame.draw.rect(tracks, (0, 0, 0), (width // 4 - stripe_width // 2, 0, stripe_width, height))
    pygame.draw.rect(tracks, (0, 0, 0), (3 * width // 4 - stripe_width // 2, 0, stripe_width, height))

    # Blit the tracks onto the screen
    screen.blit(tracks, (x, y))

def create_crosswalk(x, y, size, num_horizontal_stripes, stripe_width, stripe_gap, angle):
    crosswalk = pygame.Surface((size, size), pygame.SRCALPHA)
    background_color = (128, 128, 128)  # Gray background color

    # Fill the background with the gray color
    pygame.draw.rect(crosswalk, background_color, (0, 0, size, size))

    # Calculate the spacing for the horizontal stripes
    total_gap = (num_horizontal_stripes - 1) * stripe_gap
    available_height = size - total_gap
    stripe_height = available_height / num_horizontal_stripes

    # Draw the two vertical white lines
    vertical_stripe_width = size // 10  # Adjust the width of the vertical stripes
    pygame.draw.rect(crosswalk, (255, 255, 255), (size // 4 - vertical_stripe_width // 2, 0, vertical_stripe_width, size))
    pygame.draw.rect(crosswalk, (255, 255, 255), (3 * size // 4 - vertical_stripe_width // 2, 0, vertical_stripe_width, size))

    # Draw the horizontal white stripes
    for i in range(num_horizontal_stripes):
        # Calculate the starting and ending points of the horizontal stripes
        start_x = size // 20
        end_x = size - (size // 20)*2
        horizontal_stripe_y = (i + 0.5) * (stripe_height + stripe_gap) - stripe_width / 2
        pygame.draw.rect(crosswalk, (255, 255, 255), (size // 4 - vertical_stripe_width // 2, horizontal_stripe_y,size - size // 2, stripe_width))

    # Rotate the crosswalk based on the specified angle
    rotated_crosswalk = pygame.transform.rotate(crosswalk, angle)

    # Blit the rotated crosswalk onto the screen
    screen.blit(rotated_crosswalk, (x, y))







# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Set the background color to green
    screen.fill(green)

    # Create and add roads to the list with different types of dividers
    #Horizontal Roads
    create_road(0, 100, screen_width, 50, 0, road_divider="dashed") # Rua horizontal em cima percorre a totalidade do ecra  pode ser problem com paredes
    create_road(100, 600, 500, 50, 0, road_divider="dashed")#Em baixo entre ruas
    create_road(550, 600, 800, 50, 0, road_divider="dashed") # Em baixo lado direito
    #Vertical Roadas
    create_road(100, 0, screen_height, 100, 90, road_divider="solid")
    create_road(500, 0, screen_height, 100, 90, road_divider="solid")
    #Divisão de 45º
    create_road(580, 120, 200, 30, 45, road_divider="")
    #Train Tracks
    create_train_tracks(1000, 0, 150, screen_height)

    # Draw roads from the list
    for road in roads:
        screen.blit(road[0], (road[1], road[2]))

    # Crosswalk LEFt:
    create_crosswalk(100, 0, 100, num_horizontal_stripes=4, stripe_width=6, stripe_gap=7, angle=90)
    create_crosswalk(100, 180, 100, num_horizontal_stripes=4, stripe_width=6, stripe_gap=10, angle=90)
    create_crosswalk(20, 100, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)
    create_crosswalk(250, 100, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)

    # Crosswalk right:
    create_crosswalk(500, 0, 100, num_horizontal_stripes=4, stripe_width=6, stripe_gap=7, angle=90) #direita topo grande
    create_crosswalk(500, 140, 100, num_horizontal_stripes=4, stripe_width=6, stripe_gap=10, angle=90)
    create_crosswalk(450, 100, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)
    create_crosswalk(600, 100, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)

    create_crosswalk(600, 600, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)
    create_crosswalk(450, 600, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)
    create_crosswalk(600, 600, 50, num_horizontal_stripes=4, stripe_width=5, stripe_gap=10, angle=0)


    #trafic rua esquera
    traffic_light = traficclass.TrafficLight(60, 130, 50,270)
    traffic_light.set_color('green')
    traffic_light.draw(screen)

    # trafic rua centro lado esquerdo
    traffic_light1 = traficclass.TrafficLight(180, 150, 50,0)
    traffic_light1.set_color('red')
    traffic_light1.draw(screen)

    # trafic rua  lado esquerdo sentido direita-esquerd
    traffic_light1 = traficclass.TrafficLight(200, 70, 50,90)
    traffic_light1.set_color('green')
    traffic_light1.draw(screen)

    # trafic rua centro lado esquerdo
    traffic_light1 = traficclass.TrafficLight(80, 50, 50,180)
    traffic_light1.set_color('red')
    traffic_light1.draw(screen)


    #trafic rua direito
    traffic_light = traficclass.TrafficLight(450, 130, 50,270) # esta localizado corretamen
    traffic_light.set_color('green')
    traffic_light.draw(screen)

    # trafic rua centro lado direito
    traffic_light1 = traficclass.TrafficLight(580, 150, 50,0) # esta localizado corretamen
    traffic_light1.set_color('red')
    traffic_light1.draw(screen)

    # trafic rua  lado direito
    traffic_light1 = traficclass.TrafficLight(600, 70, 50,90)# esta localizado corretamen
    traffic_light1.set_color('green')
    traffic_light1.draw(screen)

    # trafic rua centro lado direito
    traffic_light1 = traficclass.TrafficLight(480, 50, 50,180)
    traffic_light1.set_color('yellow')
    traffic_light1.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
