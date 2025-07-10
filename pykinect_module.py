"""
KinectAzureModule: Easy Control Interface for Azure Kinect RGB-D Camera

This class provides a simple and extensible interface for Azure Kinect camera operations, 
suitable for robotics, computer vision, and perception applications. 
It supports color and depth image acquisition, multi-resolution/mode configuration, 
and device calibration parameter retrieval.

Features:
---------
- Customizable color resolution and depth mode
- Simple device start and close functions
- Quick access to camera calibration and distortion parameters
- Efficient loop for synchronized color and depth image capture

Dependencies:
-------------
- cv2 (OpenCV)
- pykinect_azure (Azure Kinect Python wrapper)

Note:
-----
- Azure Kinect SDK and Python wrapper must be installed
- Use device_index for multi-camera scenarios
- Ensure device connectivity and driver installation before use

References:
-----------
- pyKinectAzure GitHub: https://github.com/ibaiGorordo/pyKinectAzure

Author: Yu-Peng, Yeh, 2025-07-10, nickyeh0415@gmail.com
"""

import cv2
import pykinect_azure as pykinect

class KinectAzureModule:
    """
    Main controller for Azure Kinect camera.

    Allows device selection, resolution/depth mode setting, and easy access to RGB and depth images.
    """
    def __init__(self, device_index=0, resolution="1080P", depth_mode="NFOV_2X2BINNED"):
        """
        Initialize the camera module.
        
        Args:
            device_index (int): Which camera to use (default 0)
            resolution (str): Color resolution, e.g., '1080P'
            depth_mode (str): Depth mode, e.g., 'NFOV_2X2BINNED'
        """
        self.device_index = device_index

        # Supported color resolutions mapping
        self.resolution_map = {
            "720P": pykinect.K4A_COLOR_RESOLUTION_720P,
            "1080P": pykinect.K4A_COLOR_RESOLUTION_1080P,
            "1440P": pykinect.K4A_COLOR_RESOLUTION_1440P,
            "1536P": pykinect.K4A_COLOR_RESOLUTION_1536P,
            "2160P": pykinect.K4A_COLOR_RESOLUTION_2160P,
            "3072P": pykinect.K4A_COLOR_RESOLUTION_3072P
        }

        # Supported depth modes mapping
        self.depth_mode_map = {
            "NFOV_2X2BINNED": pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED,
            "NFOV_UNBINNED": pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED,
            "WFOV_2X2BINNED": pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED,
            "WFOV_UNBINNED": pykinect.K4A_DEPTH_MODE_WFOV_UNBINNED,
            "PASSIVE_IR": pykinect.K4A_DEPTH_MODE_PASSIVE_IR
            # Add other depth modes here if necessary
        }
        self.set_resolution(resolution)
        self.set_depth_mode(depth_mode)

        # Initialize Azure Kinect libraries (must be called before use)
        pykinect.initialize_libraries()

    def set_resolution(self, resolution):
        """
        Set the color image resolution.

        Args:
            resolution (str): Resolution string, e.g., '1080P'
        """
        if resolution in self.resolution_map:
            self.resolution = self.resolution_map[resolution]
        else:
            print("Invalid resolution. Defaulting to 1080P.")
            self.resolution = self.resolution_map["1080P"]

    def set_depth_mode(self, depth_mode):
        """
        Set the depth image mode.

        Args:
            depth_mode (str): Depth mode string, e.g., 'NFOV_2X2BINNED'
        """
        if depth_mode in self.depth_mode_map:
            self.depth_mode = self.depth_mode_map[depth_mode]
        else:
            print("Invalid depth mode. Defaulting to NFOV_2X2BINNED.")
            self.depth_mode = self.depth_mode_map["NFOV_2X2BINNED"]

    def start_device(self):
        """
        Start the Azure Kinect device with the selected configuration.
        This must be called before capturing images.
        """
        self.device_config = pykinect.default_configuration
        self.device_config.color_resolution = self.resolution
        self.device_config.depth_mode = self.depth_mode
        self.device = pykinect.start_device(device_index=self.device_index, config=self.device_config)

    def param(self):
        """
        Get camera intrinsic matrix and distortion coefficients.

        Returns:
            matrix: Intrinsic matrix (numpy array)
            distortion: Distortion parameters (numpy array)
        """
        matrix = self.device.calibration.get_matrix(1)
        distortion = self.device.calibration.get_distortion()
        return matrix, distortion

    def capture_loop(self):
        """
        Capture one frame (RGB and depth) from the camera.

        Returns:
            ret_RGB (bool): True if RGB image captured successfully
            RGB_image (np.ndarray): RGB image array
            ret_depth (bool): True if depth image captured successfully
            depth_image (np.ndarray): Depth image array (aligned to color)
        """
        capture = self.device.update()
        ret_RGB, RGB_image = capture.get_color_image()
        ret_depth, depth_image = capture.get_transformed_depth_image()#get_transformed_colored_depth_image()
        return ret_RGB, RGB_image, ret_depth, depth_image
    
    def close_device(self):
        """
        Close the Azure Kinect device safely.
        Always call this when finished to release the device.
        """
        self.device.close()

if __name__ == "__main__":
    import numpy as np
    
    # Set desired color resolution and depth mode
    resolution = "1080P"
    depth_mode = "NFOV_2X2BINNED"

    # Initialize Kinect Azure module
    kinect = KinectAzureModule(resolution=resolution, depth_mode=depth_mode)
    kinect.start_device()

    cv2.namedWindow('Color Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)

    while True:
        # Capture a frame from the Kinect
        ret_rgb, color_img, ret_depth, depth_img = kinect.capture_loop()
        if not ret_rgb or not ret_depth:
            continue  # Skip if failed

        # Display color image (BGR)
        cv2.imshow('Color Image', color_img)
        # Normalize depth image for visualization (uint16 → uint8)
        if depth_img is not None:
            depth_vis = cv2.normalize(depth_img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            cv2.imshow('Depth Image', depth_vis)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    kinect.close_device()