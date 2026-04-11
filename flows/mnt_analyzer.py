# -*- coding: utf-8 -*-

"""
APP: TIFF Analyzer (OneCode version)
Author: Abraham TERI
"""
import onecode
import rasterio
import matplotlib.pyplot as plt
import numpy as np



def analyze_tiff(file_path: str, band_index: int = 1):
    """
    Analyze TIFF file :
    - metadata
    - band extraction
    - histogram + image
    """

    with rasterio.open(file_path) as src:

        # ===== Metadata =====
        info = {
            "width": src.width,
            "height": src.height,
            "bands": src.count,
            "crs": str(src.crs),
            "transform": str(src.transform),
            "driver": src.driver,
        }


        # ===== Band reading =====
        if band_index < 1 or band_index > src.count:
            raise ValueError(f"Band index must be between 1 and {src.count}")

        band = src.read(band_index)

    # ===== Conversion to numpy array =====
    array = np.array(band)

    # ===== Plot =====
    plt.figure(figsize=(10, 5))

    # Image
    plt.subplot(1, 2, 1)
    im = plt.imshow(array, cmap="gray")
    plt.title(f"Band {band_index}")
    plt.colorbar(im)

    # Histogram
    plt.subplot(1, 2, 2)
    plt.hist(array.flatten(), bins=50)
    plt.title("Histogram")

    output_file = onecode.file_output(
        key="output_image",
        value="model/ouput.png",
        make_path=True
    )
    plt.savefig(output_file)
    plt.close()

    print(f"\nSaved figure: {output_file}")

    #save metadata
    meta_file = onecode.file_output(
        key="metadata",
        value="model/metadata.txt",
        tags=['TXT'],
        make_path=True
    )
    data_to_save=""
    for key, value in info.items():
        data_to_save = data_to_save + f"{key}:{value}\n"
    with open(meta_file, 'w') as f:
        f.write(data_to_save)
        print(f"\nSaved figure: {meta_file}")


def run():
    """
    OneCode entry point
    """

    #Input TIFF file
    file_path = onecode.file_input(
        key="TIFF_File_Input",
        value="C:/Users/HP/Desktop/mnt_analyzer/2025-07-25-00_Sentinel-2_L2A_B4B3B2B8.tiff"
        )

    #Input Band index
    band_index = onecode.number_input(
        key="Index_Number",
        value=1,
        label="Enter band index",
        min=0,
        max=None,
        step=1
    )

    analyze_tiff(file_path, band_index)

    onecode.Logger.info("Finished !")
