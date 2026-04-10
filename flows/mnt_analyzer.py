
# This file is your entry point:
# - add you Python files and folder inside this 'flows' folder
# - add your imports
# - just don't change the name of the function 'run()' nor this filename ('mnt_analyzer.py')
#   and everything is gonna be ok.
#
# Remember: everything is gonna be ok in the end: if it's not ok, it's not the end.
# Alternatively, ask for help at https://github.com/deeplime-io/onecode/issues

import onecode

# -*- coding: utf-8 -*-

"""
APP: TIFF Viewer
Author: Abraham TERI
Date: Oct. 2025
"""

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
    QGridLayout,
)

from osgeo import gdal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class TiffViewer(QWidget):
    """TIFF file visualization application."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TIFF Viewer")

        self.dataset = None

        self._init_ui()
        self._init_layout()

    # ===================== UI ===================== #
    def _init_ui(self) -> None:
        """Initialize UI widgets."""

        # Buttons
        self.load_button = QPushButton("Load TIFF file")
        self.load_button.clicked.connect(self.load_file)

        self.display_button = QPushButton("Display band")
        self.display_button.clicked.connect(self.display_band)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(QApplication.quit)

        # Input fields
        self.filename_label = QLabel("File name:")
        self.filename_edit = QLineEdit()

        self.band_label = QLabel("Band:")
        self.band_edit = QLineEdit("1")
        self.band_edit.setMaximumWidth(50)

        # Information label
        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)

        # Matplotlib canvas
        self.figure = plt.figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)

    def _init_layout(self) -> None:
        """Set up the layout."""
        layout = QGridLayout()

        layout.addWidget(self.load_button, 0, 0, 1, 2)
        layout.addWidget(self.filename_label, 1, 0)
        layout.addWidget(self.filename_edit, 1, 1)
        layout.addWidget(self.band_label, 2, 0)
        layout.addWidget(self.band_edit, 2, 1)
        layout.addWidget(self.display_button, 3, 0, 1, 2)
        layout.addWidget(self.info_label, 4, 0, 1, 2)
        layout.addWidget(self.canvas, 5, 0, 1, 2)
        layout.addWidget(self.quit_button, 6, 0, 1, 2)

        self.setLayout(layout)

    # ===================== LOGIC ===================== #
    def load_file(self) -> None:
        """Load a TIFF file."""
        filename, _ = QFileDialog.getOpenFileName(self, "Open TIFF File")

        if not filename:
            return

        self.filename_edit.setText(filename)
        self.dataset = gdal.Open(filename)

        if not self.dataset:
            self._show_error("Unable to load the TIFF file")
            return

        self._display_metadata()

    def _display_metadata(self) -> None:
        """Display dataset metadata."""
        ds = self.dataset

        info = (
            f"Size: {ds.RasterXSize} x {ds.RasterYSize}\n"
            f"Bands: {ds.RasterCount}\n"
            f"Projection: {ds.GetProjection()}\n"
            f"Pixel resolution: {ds.GetGeoTransform()[1]}"
        )

        self.info_label.setText(info)

    def display_band(self) -> None:
        """Display the selected band and its histogram."""
        if not self.dataset:
            self._show_error("No file loaded")
            return

        try:
            band_index = int(self.band_edit.text())
            band = self.dataset.GetRasterBand(band_index)
            array = band.ReadAsArray()

            self._plot_data(array, band_index)

        except Exception as error:
            self._show_error(f"Error while displaying band: {error}")

    def _plot_data(self, array: np.ndarray, band_index: int) -> None:
        """Plot the image and its histogram."""
        self.figure.clear()

        # Image display
        ax_img = self.figure.add_subplot(1, 2, 1)
        im = ax_img.imshow(array, cmap="gray")
        ax_img.set_title(f"Band {band_index}")
        plt.colorbar(im, ax=ax_img)

        # Histogram
        ax_hist = self.figure.add_subplot(1, 2, 2)
        ax_hist.hist(array.flatten(), bins=50)
        ax_hist.set_title("Histogram")

        self.canvas.draw()

    # ===================== UTILS ===================== #
    def _show_error(self, message: str) -> None:
        """Display an error message dialog."""
        QMessageBox.warning(self, "Error", message)


def run():
    """Application entry point."""
    app = QApplication([])
    viewer = TiffViewer()
    viewer.show()
    app.exec_()


