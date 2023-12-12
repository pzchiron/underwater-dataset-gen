from PIL import Image
import numpy as np
from pathlib import Path
import nibabel as nib

if __name__ == "__main__":

    # setup
    data_path = Path("/home/peterzhang/Documents/underwater-dataset/")

    # iterate through the samles
    for sample in data_path.iterdir():
        print(sample)
        if sample.is_dir():
            # search files
            for file in [f for f in sample.rglob("*") if f.is_file()]:

                # convert image file
                if "image.png" in file.name.lower():
                    pil_img = Image.open(file)
                    np_img = np.asarray(pil_img)
                    np_img = np.rot90(np_img, k=1, axes=(1,0))

                    nifti_img = nib.Nifti1Image(np_img, np.eye(4))
                    nib.save(nifti_img, file.parent / "image.nii.gz")

                # convert mask file
                elif "mask.png" in file.name.lower():
                    pil_mask = Image.open(file)
                    np_mask = np.asarray(pil_mask)
                    np_mask = np.rot90(np_mask, k=1, axes=(1,0))
                    
                    nifti_mask = nib.Nifti1Image(np_mask, np.eye(4))
                    nib.save(nifti_mask, file.parent / "mask.nii.gz")