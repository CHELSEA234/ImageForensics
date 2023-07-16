# ImageForensics

## Overview
The main purpose of this demo is deciding if a given image by the user has any fake (edited parts) using the given algorithm below.

This code uses the algorithm HiFi_Net for image editing detection and localization, as well as the diffusion model attribution which is accepted by CVPR, and titled as "Hierarchical Fine-Grained Image Forgery Detection and Localization".

HiFi_Net repository can be found [here](https://github.com/CHELSEA234/HiFi_IFDL/tree/main)

Example interface:

<img width="980" alt="Screenshot 2023-07-16 at 7 49 23 PM" src="https://github.com/baranmanti/ImageForensics/assets/70177697/355dbd9d-3fef-40fb-a416-50541b7b9ff4">


## Usage 
Create a conda environment: 

`conda env create -f environment.yml`

Install:

`Python 3.x`

`PyQt5 - pip3 install PyQt5`

Run **interface.py**:

Input : image provided by the user

Output : 8 windows including:
   * Drop Box
   * Feature Map 1
   * Feature Map 2
   * Feature Map 3
   * Feature Map 4
   * Binary Mask
   * TSNE Result

## Interface
Using PyQt5, this code creates a straightforward image gallery. A graphical user interface (GUI) window is made, which shows the photographs in a predetermined order. The GUI is composed of a main window that is split into two parts: a left side with a large image titled "Gallery Box" and a right side with smaller images and corresponding labels.

The user can select between images and display it and then press 'OK' to proceed.

The GUI elements are created by the code using the PyQt5 package. For the layout and display of the photos, it imports important modules like QMainWindow, QVBoxLayout, QLabel, and QPixmap.

The MyGUI class, which descended from QMainWindow, houses the majority of the code's functionality. The main window and its core widget are initialized, and the layout structure is specified, in the constructor __init__.







