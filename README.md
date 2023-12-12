# underwater-dataset-gen
Simple python scripts to generate simplified underwater images of fish, sharks and branching corals. Meant to generate a simple dataset for a semantic segmentation demonstration.
Images such as these are generated together with a mask.

Sample image of a generated scene.            |  And the corresponding mask.
:-------------------------:|:-------------------------:
![image](examples/underwater_example.png)  |  ![mask](examples/mask_example.png)

The labels in the mask are as follows:
 - 0: Background
 - 1: Ground
 - 2: Fish
 - 3: Shark
 - 4: Coral

The generated images are randomly blurred with gaussian blurring using a radius of 1 or 2.

## Dependencies
This repo only depends on Pillow, numpy and nibabel. Install them with:
```
pip install numpy nibabel Pillow
```

## Usage
Example use case, to generate 1000 data samples of size (512, 512), simply run:
```
python generate.py -n 1000 --size 512 512 -d /path/where/to/generate
```
Then if you wish, you can convert it to .nii.gz (only makes sense for the originally intended example) using:
```
python convert.py -d /path/where/the/files/are -o /where/to/save/the/niftis
```