from PIL import Image, ImageDraw, ImageFilter
import random
from pathlib import Path
import os
import argparse

from modules.draw import draw_ground, draw_fish, draw_shark, draw_coral


def generate_underwater_scene(width, height, num_fish=15, num_sharks=8, num_corals=10):
    """
    Creates an underwater scene with mask
    """
    # Create a blank image
    img = Image.new("RGB", (width, height), "lightblue")
    mask = Image.new("L", (width, height), 0)

    # setup draw
    draw = ImageDraw.Draw(img)
    mask_draw = ImageDraw.Draw(mask)

    # draw floor
    floor_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    fraction = random.uniform(0.1,1)*0.5
    draw_ground(draw, mask_draw, img.size, fraction, floor_color, mask_label=1)

    # random order generation
    choices = ["fish", "shark", "coral"]
    fish_counter, shark_counter, coral_counter = 0, 0, 0
    while choices:
        choice = random.choice(choices)

        if choice == "fish":
            fish_size = (random.randint(10, 30), random.randint(5, 20))
            fish_position = (random.randint(0, width), random.randint(0, height))
            fish_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Draw fish with fins
            draw_fish(draw, mask_draw, fish_position, fish_size, fish_color, mask_label=2)
            fish_counter += 1
            if fish_counter >= num_fish:
                choices.remove("fish")

        elif choice == "shark":
            shark_size = (random.randint(30, 40), random.randint(20, 30))
            shark_position = (random.randint(0, width), random.randint(0, height))
            shark_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Draw fish with fins
            draw_shark(draw, mask_draw, shark_position, shark_size, shark_color, mask_label=3)
            shark_counter += 1
            if shark_counter >= num_sharks:
                choices.remove("shark")

        elif choice == "coral":
            coral_size = random.randint(20, 50)
            coral_color = (random.randint(150, 255), random.randint(50, 150), random.randint(50, 100))
            coral_position = (random.randint(0, width), random.randint(int((1-fraction)*height), height))
            coral_levels = random.randint(2,4)
            # Draw coral shape (a simple branching structure)
            draw_coral(draw, mask_draw, coral_size, coral_position, coral_levels, coral_color, mask_label=4)
            coral_counter += 1
            if coral_counter >= num_corals:
                choices.remove("coral")


    return img, mask


def rand_gauss_blur(img: Image) -> Image:
    """
    Blurs an image using gaussian blurring with a random radius.
    """
    radius = random.randint(0,2)
    return img.filter(ImageFilter.GaussianBlur(radius))


def get_args():
    """
    Get arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_samples", type=int, default=500, help="How many samples to generate.")
    parser.add_argument("-d", "--data_path", default='data/', help="Path to the folder where to generate the files.")
    parser.add_argument("--size", nargs='+', type=int, default=[256, 256], help="(Width, Height) of the images." )
    return parser.parse_args()


if __name__ == "__main__":

    # setup
    args = get_args()
    assert len(args.size) == 2, "Make sure the --size argument is width height. For example: --size 256 256"
    width, height = args.size[0], args.size[1]
    n_samples = args.n_samples
    output_path = Path(args.data_path)

    for i in range(n_samples):
        folder_name = str(i).zfill(3)
        folder_path = output_path / folder_name
        os.makedirs(folder_path, exist_ok=True)
        
        # generate images
        underwater_image, underwater_mask = generate_underwater_scene(width, height)
        underwater_image = rand_gauss_blur(underwater_image)

        # save images
        underwater_image.save(folder_path / "image.png")
        underwater_mask.save(folder_path / "mask.png")
