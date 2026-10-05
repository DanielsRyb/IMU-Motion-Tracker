# IMU Motion Tracker

A personal project for learning embedded systems, signal processing, and robotics.

## Goal

Build a simple system that collects, processes, and visualizes IMU motion data.

## Current Status

modularize the functions

## Technologies

- Python
- C++
- Git
- GitHub

## To note :

- The balance between delay and the smooth window size
- The current implementation uses a causal moving-average filter suitable for real-time processing. A centered moving average could be considered for offline signal analysis.  
- The current version of std_deviation_calculate in file Analysis.py is false.
  Extra challenge: how to filter the useable datas when analysing the standard deviation? The noises must be considered¹ but how to tell if the data has a huge change at the time stamp² and if we consider to collect the stable stages³, how can we then collect the datas with relative stable slopes⁴, for example, when the object has an uniform acceleration