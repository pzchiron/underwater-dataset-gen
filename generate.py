from PIL import Image, ImageDraw
import random

from modules.draw import draw_ground, draw_fish, draw_shark, draw_coral


def generate_underwater_scene(width, height, num_fish=10, num_corals=10):
    # Create a blank image
    img = Image.new("RGB", (width, height), "lightblue")
    mask = Image.new("L", (width, height), 0)

    # setup draw
    draw = ImageDraw.Draw(img)
    mask_draw = ImageDraw.Draw(mask)

    # draw floor
    floor_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    fraction = random.uniform(0.1,1)*0.5
    draw_ground(draw, mask_draw, img.size, fraction, floor_color, mask_label=100)

    # draw fish
    for _ in range(num_fish):
        fish_size = (random.randint(10, 30), random.randint(5, 20))
        fish_position = (random.randint(0, width), random.randint(0, height))
        fish_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Draw fish with fins
        draw_fish(draw, mask_draw, fish_position, fish_size, fish_color, mask_label=200)

    # Draw sharks
    for _ in range(num_fish):
        fish_size = (random.randint(30, 40), random.randint(20, 30))
        fish_position = (random.randint(0, width), random.randint(0, height))
        fish_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Draw fish with fins
        draw_shark(draw, mask_draw, fish_position, fish_size, fish_color, mask_label=255)

    # Draw corals
    for _ in range(num_corals):
        coral_size = random.randint(20, 50)
        coral_color = (random.randint(150, 255), random.randint(50, 150), random.randint(50, 100))
        coral_position = (random.randint(0, width), random.randint(int((1-fraction)*height), height))
        coral_levels = random.randint(2,4)
        
        # Draw coral shape (a simple branching structure)
        draw_coral(draw, mask_draw, coral_size, coral_position, coral_levels, coral_color, mask_label=150)

    return img, mask

if __name__ == "__main__":

    width, height = 256, 256
    underwater_image, underwater_mask = generate_underwater_scene(width, height)
    underwater_image.show()
    underwater_mask.show()
    #underwater_image.save("underwater_scene.png")