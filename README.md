# pytrl_demo
PyTLR - Python Traffic Research Library

Convenience library to boost the traffic research and education at AAU. It is planned to implement following tasks:

## Content
- **data drivers** - create the driver module for converting raw data to represenative formats understood by all algorithms.
    * obtaining data popular benchmark datasets for object detection, multi object tracking
    * obtaining data and applying callibration with well known sensors, cameras with intrisics parameters, lidars with given specifications, radars, etc.
- **metrics** - module for comparison metrics between the ground truth and the results of object detection and tracking. Get inspiration from KITTI dataset and other benchmarks used to compare tracking algrithms and object detection datasets.
    * MOTA, MOTP, GOSPA
    * IoU, whatever else

- **object detection** - list of object detection algorithms
    * RGB/Thermal
    * LIDAR
    * RADAR

- **tracking**
    * Point methods for object defined by single detection
    * Extended methods for objects defined by more than 1 detection

- **documentation/examples** - automatically generated documentation with examples and references to papers for different methods
- CD/CI/tests - to ensure the stable version is available 24/7

- **visualization**
    * multiview video, fx RGB + bird view with trajectories
    * visauls for trajectories, predictions, uncertainities

- **utils** - utility functions for main modules
    - motion models
    - settings classes
    - loggers

- **3rd party software utils / post processing**
    * ruba
    * urban tracker
    * pylidartracker

## Potential dependencies
- General numerical tools - scipy/numpy
- ML/DL - scikit-learn, keras
- Computer Vision - cv2 / scikit-image
- Filters/Estimators - filterpy
- Metrics - motmetrics
- Assignment - murty

## How not to fail?
- Careful including too many things here, this one is for **visual traffic data post-processing**
- Make extra effort on easines of distribution with a good setup.py
- Make extra effort on organizing CI and writting test early
