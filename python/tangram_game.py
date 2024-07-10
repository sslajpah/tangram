# Tangram game designed for PTIT 2024
#
# - there is 7 tiles are numbered 1 - 7
# - use mouse to move tiles around, use right mouse click to rotate the tile
# - the tile must be picked in the vicinity of its center (black cross shows the center of the inscribed circle)
# - with "Reset tiles" button tiles are placed to its initial pose
# - with "Send figure" button poses of tiles places in the white area 
# - checkboxes are used to display tile number, tile pose, and inscribed circles
# - shown poses are regarding to area's coordinate system (grey or white, origin is in top left corner, vertical direction = x axis, horizontal direction = y axis, detoned with red and green lines, respectively)
# 
# TO DO:
# - add communication with UR robot to send it the desired poses of individual tiles
#  
# author: Sebastjan Slajpah
# mail: sebastjan.slajpah@fe.uni-lj.si
# University of Ljubljana, Faculty of Electrical Engineering
# Laboratory of Robotics
# www.robolab.si
# June 2024


import pygame
import math



# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 20
LEFT_AREA_WIDTH = 30 * TILE_SIZE
RIGHT_AREA_WIDTH = 50 * TILE_SIZE
WIDTH, HEIGHT = LEFT_AREA_WIDTH + RIGHT_AREA_WIDTH, 50 * TILE_SIZE
BUTTON_HEIGHT = 50
PLACEHOLDER_HEIGHT = 100
THICK_LINE_WIDTH = 5
ROTATION_STEP = 15

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (144, 238, 144)
VIOLET = (238, 130, 238)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangram Game UL FE LR")

# Load image
image_path = "ULFE_LR_logo.png"  # Update with the path to your image
image = pygame.image.load(image_path)
image_rect = image.get_rect()
image_rect.center = (LEFT_AREA_WIDTH // 2, HEIGHT - 3 * BUTTON_HEIGHT - image_rect.height // 2 - 30)

# Helper functions to calculate the inscribed circle center and radius for triangles
def triangle_incenter(vertices):
    ax, ay = vertices[0]
    bx, by = vertices[1]
    cx, cy = vertices[2]
    a = math.dist((bx, by), (cx, cy))
    b = math.dist((ax, ay), (cx, cy))
    c = math.dist((ax, ay), (bx, by))
    px = (a * ax + b * bx + c * cx) / (a + b + c)
    py = (a * ay + b * by + c * cy) / (a + b + c)
    return px, py

def triangle_inradius(vertices, incenter):
    ax, ay = vertices[0]
    bx, by = vertices[1]
    cx, cy = vertices[2]
    area = abs(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by)) / 2
    s = (math.dist((ax, ay), (bx, by)) + math.dist((bx, by), (cx, cy)) + math.dist((cx, cy), (ax, ay))) / 2
    return area / s

# Triangle properties
green_triangle_points = [(0, 0), (18 * TILE_SIZE, 0), (9 * TILE_SIZE, 9 * TILE_SIZE)]
green_triangle_center = triangle_incenter(green_triangle_points)
green_triangle_radius = triangle_inradius(green_triangle_points, green_triangle_center)

blue_triangle_points = [(0, 0), (9 * TILE_SIZE, 0), (9 * TILE_SIZE, 9 * TILE_SIZE)]
blue_triangle_center = triangle_incenter(blue_triangle_points)
blue_triangle_radius = triangle_inradius(blue_triangle_points, blue_triangle_center)

small_triangle_points = [(0, 0), (9 * TILE_SIZE, 0), (4.5 * TILE_SIZE, 4.5 * TILE_SIZE)]
small_triangle_center = triangle_incenter(small_triangle_points)
small_triangle_radius = triangle_inradius(small_triangle_points, small_triangle_center)

square_size = (9 / 2) * TILE_SIZE * math.sqrt(2)
square_points = [(0, 0), (square_size, 0), (square_size, square_size), (0, square_size)]
square_center = [square_size / 2, square_size / 2]
square_radius = square_size / 2

parallelogram_points = [(0, 0), (9 * TILE_SIZE, 0), (13.5 * TILE_SIZE, 4.5 * TILE_SIZE), (4.5 * TILE_SIZE, 4.5 * TILE_SIZE)]
parallelogram_center = [(parallelogram_points[0][0] + parallelogram_points[2][0]) / 2, (parallelogram_points[0][1] + parallelogram_points[2][1]) / 2]
parallelogram_radius = min(9 * TILE_SIZE / 2, 4.5 * TILE_SIZE / 2)

# Initial positions and orientations for tiles in the left area
initial_positions = [
    (10 * TILE_SIZE, 6 * TILE_SIZE),
    (10 * TILE_SIZE, 16 * TILE_SIZE),
    (10 * TILE_SIZE, 25 * TILE_SIZE),
    (25 * TILE_SIZE, 3 * TILE_SIZE),
    (25 * TILE_SIZE, 10 * TILE_SIZE),
    (25 * TILE_SIZE, 17 * TILE_SIZE),
    (23 * TILE_SIZE, 25 * TILE_SIZE)
]
#initial_rotations = [180, 180, 315, 180, 180, 0, 0]
initial_rotations = [180, 180, 315, 180, 180, 0, 0]

# Angle offsets to normalize the initial orientations to 0°
#angle_offsets = [180, 180, 315, 180, 180, 0, 0]
angle_offsets = [180, 180, 315, 0, 0, 180, 180]

# Shapes definition
shapes = [
    {'points': green_triangle_points, 'color': GREEN, 'center': green_triangle_center, 'radius': green_triangle_radius, 'position': None, 'number': 2},
    {'points': green_triangle_points, 'color': ORANGE, 'center': green_triangle_center, 'radius': green_triangle_radius, 'position': None, 'number': 1},
    {'points': blue_triangle_points, 'color': BLUE, 'center': blue_triangle_center, 'radius': blue_triangle_radius, 'position': None, 'number': 3},
    {'points': small_triangle_points, 'color': LIGHT_GREEN, 'center': small_triangle_center, 'radius': small_triangle_radius, 'position': None, 'number': 6},
    {'points': small_triangle_points, 'color': VIOLET, 'center': small_triangle_center, 'radius': small_triangle_radius, 'position': None, 'number': 7},
    {'points': square_points, 'color': YELLOW, 'center': square_center, 'radius': square_radius, 'position': None, 'number': 4},
    {'points': parallelogram_points, 'color': RED, 'center': parallelogram_center, 'radius': parallelogram_radius, 'position': None, 'number': 5}
]

# Dragging and rotation states
dragging = [False] * len(shapes)
rotations = initial_rotations.copy()

# Reset tile positions and rotations
def reset_tile_positions():
    for i, shape in enumerate(shapes):
        shape['position'] = initial_positions[i]
        rotations[i] = initial_rotations[i]

# Initialize tile positions and rotations
reset_tile_positions()

# Checkbox states
display_tile_number = True
display_pose = True
show_circles = False

def draw_grid(surface, area_size, offset_x=0, offset_y=0, tile_size=TILE_SIZE):
    for x in range(0, area_size, tile_size):
        pygame.draw.line(surface, BLACK, (x + offset_x, offset_y), (x + offset_x, area_size + offset_y))
    for y in range(0, area_size, tile_size):
        pygame.draw.line(surface, BLACK, (offset_x, y + offset_y), (area_size + offset_x, y + offset_y))

def draw_polygon(surface, points, color):
    pygame.draw.polygon(surface, color, points)

def rotate_point(point, angle, center):
    angle_rad = math.radians(angle)
    x, y = point
    cx, cy = center
    new_x = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
    new_y = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
    return new_x, new_y

def draw_center(surface, center):
    x, y = center
    pygame.draw.line(surface, BLACK, (x - 5, y), (x + 5, y), 2)
    pygame.draw.line(surface, BLACK, (x, y - 5), (x, y + 5), 2)

def draw_inscribed_circle(surface, center, radius):
    pygame.draw.circle(surface, BLACK, (int(center[0]), int(center[1])), int(radius), 2)

def draw_pose(surface, center, rotation, number, is_right_area):
    font = pygame.font.Font(None, 24)
    angle_offset = angle_offsets[number - 1]
    corrected_rotation = (rotation - angle_offset) % 360
    if is_right_area:
        coord_y = (center[0] - LEFT_AREA_WIDTH - THICK_LINE_WIDTH) / TILE_SIZE
        coord_x = center[1] / TILE_SIZE
    else:
        coord_y = center[0] / TILE_SIZE
        coord_x = center[1] / TILE_SIZE

    if display_tile_number and display_pose:
        text = f"{number}: ({int(coord_x)}, {int(coord_y)}, {corrected_rotation}°)"
    elif display_tile_number:
        text = f"{number}"
    elif display_pose:
        text = f"({int(coord_x)}, {int(coord_y)}, {corrected_rotation}°)"
    else:
        text = ""

    if text:
        rendered_text = font.render(text, True, BLACK)
        surface.blit(rendered_text, (center[0] + 10, center[1]))

def draw_axes(surface, origin):
    pygame.draw.line(surface, RED, origin, (origin[0], origin[1] + 50), 3)
    pygame.draw.line(surface, GREEN, origin, (origin[0] + 50, origin[1]), 3)

# Function to display tile positions in the right area coordinate system
def display_right_area_positions():
    positions = []
    for shape, rotation in zip(shapes, rotations):
        center_x, center_y = shape['position']
        angle_offset = angle_offsets[shape['number'] - 1]
        corrected_rotation = (rotation - angle_offset) % 360
        if center_x > LEFT_AREA_WIDTH + THICK_LINE_WIDTH:
            # Translate coordinates to the right area coordinate system
            relative_y = (center_x - (LEFT_AREA_WIDTH + THICK_LINE_WIDTH)) / TILE_SIZE
            relative_x = center_y / TILE_SIZE
            positions.append(f"Tile {shape['number']}: ({relative_x:.2f}, {relative_y:.2f}, {corrected_rotation}°)")
    return positions

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw left area with light gray background
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, LEFT_AREA_WIDTH, HEIGHT))
    
    # Draw right area with white background
    pygame.draw.rect(screen, WHITE, (LEFT_AREA_WIDTH + THICK_LINE_WIDTH, 0, RIGHT_AREA_WIDTH, HEIGHT))
    
    # Draw buttons
    send_figure_button_rect = pygame.Rect(0, HEIGHT - 2 * BUTTON_HEIGHT, LEFT_AREA_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BLACK, send_figure_button_rect)
    pygame.draw.rect(screen, WHITE, send_figure_button_rect, 2)
    font = pygame.font.Font(None, 36)
    text = font.render("SEND FIGURE", True, WHITE)
    text_rect = text.get_rect(center=send_figure_button_rect.center)
    screen.blit(text, text_rect)
    
    reset_button_rect = pygame.Rect(0, HEIGHT - BUTTON_HEIGHT, LEFT_AREA_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BLACK, reset_button_rect)
    pygame.draw.rect(screen, WHITE, reset_button_rect, 2)
    text = font.render("RESET TILES", True, WHITE)
    text_rect = text.get_rect(center=reset_button_rect.center)
    screen.blit(text, text_rect)
    
    # Draw image
    screen.blit(image, image_rect)

    # Draw checkboxes
    checkbox_font = pygame.font.Font(None, 24)
    display_tile_number_rect = pygame.Rect(10, HEIGHT - 3 * BUTTON_HEIGHT - 10, 20, 20)
    display_pose_rect = pygame.Rect(200, HEIGHT - 3 * BUTTON_HEIGHT - 10, 20, 20)
    show_circles_rect = pygame.Rect(390, HEIGHT - 3 * BUTTON_HEIGHT - 10, 20, 20)
    pygame.draw.rect(screen, BLACK, display_tile_number_rect, 2)
    pygame.draw.rect(screen, BLACK, display_pose_rect, 2)
    pygame.draw.rect(screen, BLACK, show_circles_rect, 2)
    if display_tile_number:
        pygame.draw.line(screen, BLACK, (display_tile_number_rect.left, display_tile_number_rect.top), (display_tile_number_rect.right, display_tile_number_rect.bottom), 2)
        pygame.draw.line(screen, BLACK, (display_tile_number_rect.left, display_tile_number_rect.bottom), (display_tile_number_rect.right, display_tile_number_rect.top), 2)
    if display_pose:
        pygame.draw.line(screen, BLACK, (display_pose_rect.left, display_pose_rect.top), (display_pose_rect.right, display_pose_rect.bottom), 2)
        pygame.draw.line(screen, BLACK, (display_pose_rect.left, display_pose_rect.bottom), (display_pose_rect.right, display_pose_rect.top), 2)
    if show_circles:
        pygame.draw.line(screen, BLACK, (show_circles_rect.left, show_circles_rect.top), (show_circles_rect.right, show_circles_rect.bottom), 2)
        pygame.draw.line(screen, BLACK, (show_circles_rect.left, show_circles_rect.bottom), (show_circles_rect.right, show_circles_rect.top), 2)
    screen.blit(checkbox_font.render("Display tile number", True, BLACK), (40, HEIGHT - 3 * BUTTON_HEIGHT - 10))
    screen.blit(checkbox_font.render("Display pose", True, BLACK), (230, HEIGHT - 3 * BUTTON_HEIGHT - 10))
    screen.blit(checkbox_font.render("Show circles", True, BLACK), (420, HEIGHT - 3 * BUTTON_HEIGHT - 10))

    draw_grid(screen, LEFT_AREA_WIDTH, 0, 0, TILE_SIZE)
    draw_grid(screen, RIGHT_AREA_WIDTH, LEFT_AREA_WIDTH + THICK_LINE_WIDTH, 0, TILE_SIZE)

    # Draw axes
    draw_axes(screen, (15, 15))  # Left area
    draw_axes(screen, (LEFT_AREA_WIDTH + THICK_LINE_WIDTH + 15, 15))  # Right area

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for i, shape in enumerate(shapes):
                    if math.hypot(event.pos[0] - shape['position'][0], event.pos[1] - shape['position'][1]) < shape['radius']:
                        dragging[i] = True
                        mouse_x, mouse_y = event.pos
                        offset_x = shape['position'][0] - mouse_x
                        offset_y = shape['position'][1] - mouse_y
                if reset_button_rect.collidepoint(event.pos):
                    reset_tile_positions()
                elif send_figure_button_rect.collidepoint(event.pos):
                    positions = display_right_area_positions()
                    for position in positions:
                        print(position)
                elif display_tile_number_rect.collidepoint(event.pos):
                    display_tile_number = not display_tile_number
                elif display_pose_rect.collidepoint(event.pos):
                    display_pose = not display_pose
                elif show_circles_rect.collidepoint(event.pos):
                    show_circles = not show_circles
            elif event.button == 3:  # Right mouse button
                for i, shape in enumerate(shapes):
                    if math.hypot(event.pos[0] - shape['position'][0], event.pos[1] - shape['position'][1]) < shape['radius']:
                        rotations[i] += ROTATION_STEP
                        if rotations[i] >= 360:
                            rotations[i] -= 360
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = [False] * len(shapes)
        elif event.type == pygame.MOUSEMOTION:
            for i, shape in enumerate(shapes):
                if dragging[i]:
                    mouse_x, mouse_y = event.pos
                    shape['position'] = (mouse_x + offset_x, mouse_y + offset_y)

    for i, shape in enumerate(shapes):
        rotated_points = [rotate_point(point, rotations[i], shape['center']) for point in shape['points']]
        rotated_points = [(x + shape['position'][0] - shape['center'][0], y + shape['position'][1] - shape['center'][1]) for x, y in rotated_points]
        draw_polygon(screen, rotated_points, shape['color'])
        actual_center = shape['position']
        draw_center(screen, actual_center)
        if show_circles:
            draw_inscribed_circle(screen, actual_center, shape['radius'])
        draw_pose(screen, actual_center, rotations[i], shape['number'], actual_center[0] > LEFT_AREA_WIDTH + THICK_LINE_WIDTH)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
