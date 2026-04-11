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
    Analyse un fichier TIFF :
    - métadonnées
    - extraction bande
    - histogramme + image
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

        print("=== TIFF METADATA ===")
        for k, v in info.items():
            print(f"{k}: {v}")

        # ===== Lecture bande =====
        if band_index < 1 or band_index > src.count:
            raise ValueError(f"Band index must be between 1 and {src.count}")

        band = src.read(band_index)

    # ===== Conversion numpy =====
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
        make_path=True  # will create the model folder if doesn't exist
    )
    plt.savefig(output_file)
    plt.close()

    print(f"\nSaved figure: {output_file}")

    return {
        "metadata": info,
        "output_image": output_file
    }


def run():
    """
    OneCode entry point
    """

    #Exemple : adapter selon input OneCode
    file_path = onecode.file_input(
        key="FileInput",
        value="C:/Users/HP/Desktop/mnt_analyzer/2025-07-25-00_Sentinel-2_L2A_B4B3B2B8.tiff"
        )  # fichier uploadé

    band_index = onecode.number_input(
        key="magic_number",
        value=1,
        label="Choose a magic number",
        min=0,
        max=None,
        step=2
    )

    result = analyze_tiff(file_path, band_index)

    onecode.Logger.info(result)
