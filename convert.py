from PIL import Image
import numpy as np
from pathlib import Path
import nibabel as nib
import argparse

def get_args():
    """
    Get arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_path", default='data/', help="Path to the folder where to take the files.")
    parser.add_argument("-o", "--out_path", default='data/', help="Path to the folder where to generate the files.")
    return parser.parse_args()

if __name__ == "__main__":

    # setup
    args = get_args()
    data_path = Path(args.data_path)
    out_path = Path(args.out_path)

    # iterate through the samles
    for sample in data_path.iterdir():
        if sample.is_dir():
            print(f"converting {sample.name}")
            # search files
            for file in [f for f in sample.rglob("*") if f.is_file()]:

                # convert image file
                if "image.png" in file.name.lower():
                    pil_img = Image.open(file)
                    np_img = np.asarray(pil_img)
                    np_img = np.rot90(np_img, k=1, axes=(1,0))

                    nifti_img = nib.Nifti1Image(np_img, np.eye(4))
                    nib.save(nifti_img, out_path / sample.name / "image.nii.gz")

                # convert mask file
                elif "mask.png" in file.name.lower():
                    pil_mask = Image.open(file)
                    np_mask = np.asarray(pil_mask)
                    np_mask = np.rot90(np_mask, k=1, axes=(1,0))
                    
                    nifti_mask = nib.Nifti1Image(np_mask, np.eye(4))
                    nib.save(nifti_mask, out_path / sample.name / "mask.nii.gz")