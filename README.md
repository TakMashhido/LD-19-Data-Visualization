# LD-19 LiDAR Data Visualization

This repository contains a Python project for real-time processing and visualization of LIDAR data. The code reads LIDAR data packets from a serial connection, processes the data to extract angles and distances, and plots the results on a polar coordinate system using Matplotlib.

## Features

- **Real-time Data Processing:** Continuously reads and processes LIDAR data from the specified COM port.
- **Polar Plot Visualization:** Visualizes the LIDAR scan in a polar coordinate system, commonly used in radar maps.
- **Customizable:** Easily adjust parameters like point size and color.
- **Event-Driven Exit:** Press 'E' to exit the visualization.

## Requirements

The project relies on the following Python packages, listed in `requirements.txt`:

- `cycler==0.10.0`
- `kiwisolver==1.3.1`
- `matplotlib==3.3.4`
- `numpy==1.20.1`
- `Pillow==8.1.2`
- `pyparsing==2.4.7`
- `pyserial==3.5`
- `python-dateutil==2.8.1`
- `six==1.15.0`

You can install all the dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. **Connect the LIDAR Sensor:**
   - Connect your LD19 LIDAR sensor to your computer via the specified COM port (e.g., `COM5`).

2. **Run the Script:**
   - Use the following command to run the script:

   ```bash
   python main.py
   ```
3. **View the Visualization:**

    - The LIDAR data will be visualized on a polar plot. The points represent the distance and angle measurements from the LIDAR.

4. **Exit the Visualization:**

    - Press the 'E' key to exit the visualization.

