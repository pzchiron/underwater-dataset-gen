from PIL import Image, ImageDraw
import random
import math

def draw_fish(draw, position, size, color):
    """
    Draws a fish consisting of an ellipse as body and triangle for the caudal fin.
    The fish will be drawn such that the ellipse's center is the given image coordinate.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        position (Tuple): (x,y) where 0,0 is the upper left corner of the image.
        size (Tuple): (dx, dy) size of the bounding box for the ellipse.
        color (Tuple): (int, int, int) rgb color
    """
    # Draw fish body (ellipse)
    draw.ellipse([position[0]-size[0]//2, position[1]-size[1]//2, position[0] + size[0]//2, position[1] + size[1]//2], fill=color)

    # Draw fish tail (triangle)
    tail_length = size[0] // 2
    tail_left = random.uniform(0,1) >= 0.5
    if tail_left:
        tail_points = [
            position[0] - tail_length - size[0]//2, position[1] - size[1]//2,
            position[0] - tail_length - size[0]//2, position[1] + size[1]//2,
            position[0] - size[0]//2, position[1]
        ]
    else:
        tail_points = [
            position[0] + tail_length + size[0]//2, position[1] - size[1]//2,
            position[0] + tail_length + size[0]//2, position[1] + size[1]//2,
            position[0] + size[0]//2, position[1]
        ]
    draw.polygon(tail_points, fill=color)


def draw_shark(draw, position, size, color):
    """
    Draws a random colorful shark consisting of an ellipse as body and triangle for the caudal and dorsal fin.
    The fish will be drawn such that the ellipse's center is the given image coordinate.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        position (Tuple): (x,y) where 0,0 is the upper left corner of the image.
        size (Tuple): (dx, dy) size of the bounding box for the ellipse.
        color (Tuple): (int, int, int) rgb color
    """
    # Draw body (ellipse)
    draw.ellipse([position[0]-size[0]//2, position[1]-size[1]//2, position[0] + size[0]//2, position[1] + size[1]//2], fill=color)

    # determine swim direction
    tail_left = random.uniform(0,1) >= 0.5

    # Draw caudal tail (triangle)
    tail_length = size[0] // 2
    if tail_left:
        tail_points = [
            position[0] - tail_length - size[0]//2, position[1] - size[1]//2,
            position[0] - tail_length - size[0]//2, position[1] + size[1]//2,
            position[0] - size[0]//2, position[1]
        ]
    else:
        tail_points = [
            position[0] + tail_length + size[0]//2, position[1] - size[1]//2,
            position[0] + tail_length + size[0]//2, position[1] + size[1]//2,
            position[0] + size[0]//2, position[1]
        ]
    draw.polygon(tail_points, fill=color)

    # Draw dorsal fin (triangle)
    tail_length = size[0] // 2
    if tail_left:
        tail_points = [
            position[0] - size[0]//8, position[1],
            position[0] + 3*size[0]//8, position[1],
            position[0] - size[0]//8, position[1] - size[1]//2 - size[1]//4
        ]
    else:
        tail_points = [
            position[0] + size[0]//8, position[1],
            position[0] - 3*size[0]//8, position[1],
            position[0] + size[0]//8, position[1] - size[1]//2 - size[1]//4
        ] 
    draw.polygon(tail_points, fill=color)

    
def draw_ground(draw, img_size, fraction, color):
    """
    Draws a random colorful shark consisting of an ellipse as body and triangle for the caudal and dorsal fin.
    The fish will be drawn such that the ellipse's center is the given image coordinate.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        img_size (Tuple): (dx, dy) size of the image
        fraction (float): fraction of the image which should be floor. 1 means full image, 0 means no floor.
        color (Tuple): (int, int, int) rgb color
    """
    # get random floor size
    floor_points = [
        0, img_size[1] *(1 - fraction),
        img_size[0], img_size[1]
    ]
    draw.rectangle(floor_points, fill=color)

def gen_branch(draw, position, width, length, angle, color):
    """
    Draws a single line and returns the end point.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        position (Tuple): (x,y), the lower middle point of the first branch
        width (int): width of the line
        angle (float): angle of the line
        color (Tuple): (int, int, int) rgb color
    Return:
        (Tuple): (int, int) end position after drawing the line
    """
    x_new = int(position[0] + length * math.cos(angle))
    y_new = int(position[1] - length * math.sin(angle))
    draw.line(
        [position[0], position[1], x_new, y_new],
        width=width,
        fill=color
    )
    return x_new, y_new

def draw_coral(draw, size, position, levels, color):
    """
    Draws a random colored branching coral.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        size (int): length of first branch
        position (Tuple): (x,y), the lower middle point of the first branch
        levels (int): how many nodes to draw
        color (Tuple): (int, int, int) rgb color
    """
    # draw the first line
    first_width = size // 10
    draw.line(
        [position[0], position[1],
         position[0], position[1] - size // 2],
        width=first_width,
        fill=color,
    )

    # branch out
    nodes = [(position[0], position[1] - size // 2)]
    next_nodes = []
    for level in range(levels):
        # iterate through each level
        for node in nodes:
            num_branches = random.randint(3, 5)
            
            # draw each branch
            for _ in range(num_branches):
                next_nodes.append(
                    gen_branch(
                        draw=draw,
                        position=node,
                        width=int(first_width * 0.8**(level+1)),
                        length=random.uniform(0.2, 0.8) * size * 0.8**(level+1),
                        angle=random.uniform(0, 3/2 * math.pi) - math.pi / 4,
                        color=color,
                    )
                )
        nodes = next_nodes
        next_nodes = []


def generate_underwater_scene(width, height, num_fish=10, num_corals=10):
    # Create a blank image
    img = Image.new("RGB", (width, height), "lightblue")
    print(img.size)

    # setup draw
    draw = ImageDraw.Draw(img)

    # draw floor
    floor_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    fraction = random.uniform(0.1,1)*0.5
    draw_ground(draw, img.size, fraction, floor_color)

    # draw fish
    for _ in range(num_fish):
        fish_size = (random.randint(10, 30), random.randint(5, 20))
        fish_position = (random.randint(0, width), random.randint(0, height))
        fish_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Draw fish with fins
        draw_fish(draw, fish_position, fish_size, fish_color)

    # Draw sharks
    for _ in range(num_fish):
        fish_size = (random.randint(30, 40), random.randint(20, 30))
        fish_position = (random.randint(0, width), random.randint(0, height))
        fish_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Draw fish with fins
        draw_shark(draw, fish_position, fish_size, fish_color)

    # Draw corals
    for _ in range(num_corals):
        coral_size = random.randint(20, 50)
        coral_color = (random.randint(150, 255), random.randint(50, 150), random.randint(50, 100))
        coral_position = (random.randint(0, width), random.randint(int((1-fraction)*height), height))
        coral_levels = random.randint(2,4)
        
        # Draw coral shape (a simple branching structure)
        draw_coral(draw, coral_size, coral_position, coral_levels, coral_color)

    return img

if __name__ == "__main__":

    width, height = 256, 256
    underwater_image = generate_underwater_scene(width, height)
    underwater_image.show()
    #underwater_image.save("underwater_scene.png")