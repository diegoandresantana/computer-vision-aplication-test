# Computer Vision Application - pyAplicativo

> A desktop application for real-time computer vision processing using OpenCV, built with Python and Tkinter.

**Author**: Diego André Sant'Ana (diego.santana@ifms.br)  
**Version**: 1.0.0  
**License**: MIT  

---

## 📖 Overview

This project demonstrates various computer vision techniques applied to real-time video capture. The application provides an interactive GUI where users can select different image processing operations and adjust parameters dynamically.

### Key Features

- 🎥 Real-time webcam capture
- 🖼️ Side-by-side comparison (original vs processed)
- ⚙️ 12 different computer vision operations
- 🎛️ Adjustable parameters (kernel size, thresholds)
- 🖱️ User-friendly Tkinter interface

---

## 🛠️ Requirements

### System Dependencies

1. **Python 2.7** - [Download](https://www.python.org/downloads/)
2. **NVIDIA CUDA Libraries** - [Download](https://developer.nvidia.com/cuda-downloads) *(optional, for GPU acceleration)*
3. **NVIDIA cuDNN Libraries** - [Download](https://developer.nvidia.com/cudnn) *(optional)*

### Python Packages

Install the required packages:

```bash
pip install numpy opencv-python pillow scikit-image scikit-learn h5py
```

**Note**: TensorFlow or Theano backend may be required for some advanced features (tested with TensorFlow).

---

## 🚀 How to Use

1. **Clone or download** this repository
2. **Install all requirements** listed above
3. **Run the application**:

```bash
python pyAplicativo.py
```

*On Linux/Mac, you may need sudo privileges:*
```bash
sudo python pyAplicativo.py
```

4. **Click "Active Capture"** to start the webcam
5. **Select an operation** from the radio buttons
6. **Adjust parameters** using the spinboxes (Kernel, Min, Max values)

---

## 📋 Available Operations

### Filtering
- **Adaptive Threshold (Gaussian)** - Adaptive thresholding with Gaussian weighting
- **Adaptive Threshold (Mean)** - Adaptive thresholding with mean weighting

### Edge Detection
- **Find Contours** - Detect and draw object contours (adjust Min/Max values)
- **Canny Edge Detection** - Classic edge detection algorithm (adjust Min/Max values)

### Morphological Operations
- **Black Hat** - Difference between closing and original image
- **Erode** - Shrinks bright regions
- **Dilate** - Expands bright regions
- **Open** - Erosion followed by dilation
- **Close** - Dilation followed by erosion
- **Gradient** - Difference between dilation and erosion

### Segmentation
- **Threshold Binary Inverse** - Binary thresholding (inverted)
- **Threshold Binary** - Standard binary thresholding

---

## 📁 Project Structure

```
computer-vision-test/
├── pyAplicativo.py      # Main application script
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
└── docs/                # GitHub Pages documentation
    ├── index.html       # Interactive documentation page
    └── script.js        # Page functionality
```

---

## 🖼️ Interface Layout

The application window is divided into:

- **Left Panel**: Controls and options
  - Active Capture button
  - Operation selection (radio buttons)
  - Parameter adjustment (spinboxes for Kernel, Min, Max)
  
- **Right Panel**: Image display
  - Normal Cam (original feed)
  - Transformation Cam (processed feed)

---

## 🔧 Configuration Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| Kernel | Size of morphological operation kernel | 5 | 1-255 |
| Min | Minimum threshold value | 127 | 0-255 |
| Max | Maximum threshold value | 255 | 0-255 |

---

## 📝 Notes

- This application was developed for educational purposes in a Computer Vision course
- Some operations may require specific parameter ranges for optimal results
- GPU acceleration (CUDA/cuDNN) is optional but recommended for better performance

---

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🌐 Online Documentation

View the interactive documentation at: https://yourusername.github.io/computer-vision-test/

*Last updated: 2024*
