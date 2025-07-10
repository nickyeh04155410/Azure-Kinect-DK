# KinectAzureModule

A simple and extensible Python interface for Azure Kinect RGB-D cameras, designed for robotics, vision, and perception applications.

## Features

- Customizable color resolution and depth mode  
- Easy device start and close functions  
- Quick access to camera calibration and distortion parameters  
- Efficient synchronized color and depth image acquisition  

## Dependencies

- [OpenCV (cv2)](https://pypi.org/project/opencv-python/)
- [pyKinectAzure](https://github.com/ibaiGorordo/pyKinectAzure)  
  (requires Azure Kinect SDK and device drivers)

## Installation

1. **Install Azure Kinect SDK** from Microsoft and ensure your device is connected.
2. Install required Python packages:
   ```bash
   pip install opencv-python
   pip install numpy
   pip install pyKinectAzure
## Usage

Import `KinectAzureModule` from `pykinect_module.py` and use it to initialize, capture, and close the device as needed.

## Notes

- The Azure Kinect SDK and the corresponding Python wrapper must be properly installed and configured.
- Use `device_index` if you have multiple Azure Kinect cameras connected.
- Always call `close_device()` to safely release hardware resources after use.

## Reference

- [pyKinectAzure on GitHub](https://github.com/ibaiGorordo/pyKinectAzure)
- Follow additional setup steps in [pyKinectAzure GitHub](https://github.com/ibaiGorordo/pyKinectAzure) if needed.

## Author

Yu-Peng Yeh (<nickyeh0415@gmail.com>)  
2025-07-10
