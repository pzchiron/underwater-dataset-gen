from PIL import ImageDraw
import random
import math

def draw_fish(draw: ImageDraw, mask_draw: ImageDraw, position, size, color, mask_label):
    """
    Draws a fish consisting of an ellipse as body and triangle for the caudal fin.
    The fish will be drawn such that the ellipse's center is the given image coordinate.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        mask_draw (PIL.ImageDraw): to draw the mask of the fish.
        position (Tuple): (x,y) where 0,0 is the upper left corner of the image.
        size (Tuple): (dx, dy) size of the bounding box for the ellipse.
        color (Tuple): (int, int, int) rgb color
        mask_label (int): value for the fish label
    """
    # Draw fish body (ellipse)
    ellipse_pos = [position[0]-size[0]//2, position[1]-size[1]//2, position[0] + size[0]//2, position[1] + size[1]//2] 
    draw.ellipse(ellipse_pos, fill=color)
    mask_draw.ellipse(ellipse_pos, fill=mask_label)

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
    mask_draw.polygon(tail_points, fill=mask_label)


def draw_shark(draw: ImageDraw, mask_draw: ImageDraw, position, size, color, mask_label):
    """
    Draws a random colorful shark consisting of an ellipse as body and triangle for the caudal and dorsal fin.
    The fish will be drawn such that the ellipse's center is the given image coordinate.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        mask_draw (PIL.ImageDraw): to draw the mask of the fish.
        position (Tuple): (x,y) where 0,0 is the upper left corner of the image.
        size (Tuple): (dx, dy) size of the bounding box for the ellipse.
        color (Tuple): (int, int, int) rgb color
        mask_label (int): value for the fish label
    """
    # Draw body (ellipse)
    ellipse_pos = [position[0]-size[0]//2, position[1]-size[1]//2, position[0] + size[0]//2, position[1] + size[1]//2]
    draw.ellipse(ellipse_pos, fill=color)
    mask_draw.ellipse(ellipse_pos, fill=mask_label)

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
    mask_draw.polygon(tail_points, fill=mask_label)

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
    mask_draw.polygon(tail_points, fill=mask_label)

    
def draw_ground(draw: ImageDraw, mask_draw: ImageDraw, img_size, fraction, color, mask_label):
    """
    Draws a random colorful shark consisting of an ellipse as body and triangle for the caudal and dorsal fin.
    The fish will be drawn such that the ellipse's center is the given image coordinate.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        mask_draw (PIL.ImageDraw): to draw the mask of the fish.
        img_size (Tuple): (dx, dy) size of the image
        fraction (float): fraction of the image which should be floor. 1 means full image, 0 means no floor.
        color (Tuple): (int, int, int) rgb color
        mask_label (int): value for the fish label
    """
    # get random floor size
    floor_points = [
        0, img_size[1] *(1 - fraction),
        img_size[0], img_size[1]
    ]
    draw.rectangle(floor_points, fill=color)
    mask_draw.rectangle(floor_points, fill=mask_label)


def gen_branch(draw: ImageDraw, mask_draw: ImageDraw, position, width, length, angle, color, mask_label):
    """
    Draws a single line and returns the end point.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        mask_draw (PIL.ImageDraw): to draw the mask of the fish.
        position (Tuple): (x,y), the lower middle point of the first branch
        width (int): width of the line
        angle (float): angle of the line
        color (Tuple): (int, int, int) rgb color
        mask_label (int): value for the fish label
    Return:
        (Tuple): (int, int) end position after drawing the line
    """
    x_new = int(position[0] + length * math.cos(angle))
    y_new = int(position[1] - length * math.sin(angle))
    line_points = [position[0], position[1], x_new, y_new]
    draw.line(line_points, width=width, fill=color)
    mask_draw.line(line_points, width=width, fill=mask_label)
    return x_new, y_new

def draw_coral(draw: ImageDraw, mask_draw: ImageDraw, size, position, levels, color, mask_label):
    """
    Draws a random colored branching coral.

    Args:
        draw (PIL.ImageDraw): to draw the fish.
        mask_draw (PIL.ImageDraw): to draw the mask of the fish.
        size (int): length of first branch
        position (Tuple): (x,y), the lower middle point of the first branch
        levels (int): how many nodes to draw
        color (Tuple): (int, int, int) rgb color
        mask_label (int): value for the fish label
    """
    # draw the first line
    first_width = size // 10
    line_points = [position[0], position[1], position[0], position[1] - size // 2]
    draw.line(line_points, width=first_width, fill=color)
    mask_draw.line(line_points, width=first_width, fill=mask_label)

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
                        mask_draw=mask_draw,
                        position=node,
                        width=int(first_width * 0.8**(level+1)),
                        length=random.uniform(0.2, 0.8) * size * 0.8**(level+1),
                        angle=random.uniform(0, 3/2 * math.pi) - math.pi / 4,
                        color=color,
                        mask_label=mask_label,
                    )
                )
        nodes = next_nodes
        next_nodes = []