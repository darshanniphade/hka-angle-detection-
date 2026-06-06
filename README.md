# HKA Angle Detection using YOLO

## Overview

This project presents an automated Hip-Knee-Ankle (HKA) angle detection system for lower-limb X-ray images. The objective is to accurately measure the mechanical alignment of the lower extremity by identifying key anatomical landmarks and computing the angle formed by the femoral and tibial mechanical axes.

The system combines deep learning–based object detection with geometric analysis to provide precise and reproducible HKA angle measurements.

## Problem Statement

The HKA angle is an important orthopedic measurement used to evaluate lower-limb alignment, knee deformities, and outcomes of corrective surgeries such as Total Knee Arthroplasty (TKA).

Traditional manual measurement is time-consuming and subject to inter-observer variability. This project aims to automate the process using computer vision techniques.

## Methodology

### 1. Landmark Detection using YOLO

A custom YOLO model was trained on annotated lower-limb X-ray images to detect key anatomical landmarks required for HKA angle calculation.

The model identifies:

* Femoral head center
* Knee joint center
* Ankle joint center

YOLO was selected because of:

* Fast inference speed
* High localization accuracy
* Robust performance on medical images
* Ability to detect multiple landmarks simultaneously

The trained model predicts bounding boxes around anatomical structures, from which center coordinates are extracted.

### 2. Coordinate Extraction

After detection, the center point of each predicted bounding box is computed.

These coordinates represent:

* Hip point (H)
* Knee point (K)
* Ankle point (A)

The extracted coordinates serve as inputs for geometric calculations.

### 3. Mechanical Axis Construction

Two mechanical axes are generated:

#### Femoral Mechanical Axis

A line connecting:

* Hip Center
* Knee Center

#### Tibial Mechanical Axis

A line connecting:

* Knee Center
* Ankle Center

These axes represent the load-bearing alignment of the lower limb.

### 4. HKA Angle Computation

Using the detected coordinates, vectors are formed along the femoral and tibial mechanical axes.

The angle between these vectors is computed using vector geometry and trigonometric relationships.

The resulting value represents the Hip-Knee-Ankle (HKA) angle.

### 5. Visualization

The system visualizes:

* Detected landmarks
* Femoral mechanical axis
* Tibial mechanical axis
* Calculated HKA angle

This provides an interpretable output that can be verified by clinicians and researchers.

## Results

The developed pipeline successfully:

* Detects anatomical landmarks automatically
* Constructs mechanical axes accurately
* Computes HKA angles without manual intervention
* Produces visual outputs for validation and analysis

The approach significantly reduces measurement time while maintaining consistency and reproducibility.

## Applications

* Orthopedic diagnosis
* Knee alignment assessment
* Pre-operative planning
* Post-operative evaluation
* Medical image analysis research
* Clinical decision support systems

## Technologies Used

* Python
* YOLO
* OpenCV
* NumPy
* Matplotlib
* Pandas

## Conclusion

This project demonstrates an automated framework for HKA angle measurement using YOLO-based landmark detection and geometric analysis. By combining deep learning with mathematical angle computation, the system provides an efficient and reliable solution for lower-limb alignment assessment in orthopedic applications.
