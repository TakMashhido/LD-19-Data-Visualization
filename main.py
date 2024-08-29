import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math

# Create a figure using pyplot from matplotlib
# A figure is like a canvas on which multiple plots can be drawn
fig = plt.figure(figsize=(8,8))

# Create a subplot on the figure
# At position (1, 1) with an index of 1 on the figure
# Use a polar coordinate system, which is circular and often used for radar maps
ax = fig.add_subplot(111, projection='polar')
# Set the title for the plot
ax.set_title('Lidar LD19 (exit: Key E)', fontsize=18)

# Define the COM port for serial communication
com_port = "COM3"

# Create an event listener for pyplot
# 'key_press_event': event triggered by pressing a key
# This lambda function exits the program if the 'e' key is pressed
plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

# Establish a serial connection
ser = serial.Serial(port=com_port,
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

# Initialize variables
tmpString = ""
angles = list()
distances = list()

i = 0
while True:
    loopFlag = True
    flag2c = False

    # Every 40 iterations, update the plot
    if (i % 40 == 39):
        if ('line' in locals()):
            # Remove the previous plot line
            line.remove()

        # Plot a scatter plot (a plot of points)
        # Typically used to show the correlation between two values, in this case, angle and distance
        # 'c' is color, 's' is size of points
        print(len(angles))
        line = ax.scatter(angles, distances, c="blue", s=5)
        # Set the offset for the position of 0 degrees in the polar coordinate system
        # In Lidar's coordinate system, 0 degrees corresponds to the 0y axis, so set the offset to pi / 2
        ax.set_theta_offset(math.pi / 2)
        # Update the figure or delay for a short period
        plt.pause(0.01)
        # Clear the lists of angles and distances
        angles.clear()
        distances.clear()

        i = 0

    # Loop to read data from the serial port
    while loopFlag:
        # Read a byte of data from the serial connection
        b = ser.read()
        # Convert the byte to an integer
        # 'big' byte order means the most significant bits are at the start
        tmpInt = int.from_bytes(b, 'big')

        # 0x54 indicates the beginning of a data packet (as per the LD19 document)
        if (tmpInt == 0x54):
            tmpString += b.hex() + " "
            flag2c = True
            continue

        # 0x2c is a fixed value of VerLen (as per the LD19 document)
        elif (tmpInt == 0x2c and flag2c):
            tmpString += b.hex()

            # Check if the length of the data packet (excluding the last 5 characters) is 90
            if (not len(tmpString[0:-5].replace(' ','')) == 90):
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            # After reading a full LIDAR data packet of size 90, process the string with CalcLidarData()
            lidarData = CalcLidarData(tmpString[0:-5])
            # Retrieve the angle and distance values
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)

            # Clear the temporary string and exit the loop
            tmpString = ""
            loopFlag = False
        else:
            # Append the byte to the temporary string if it doesn't match 0x54 or 0x2c
            tmpString += b.hex() + " "

        flag2c = False

    i += 1

# Close the serial connection
ser.close()
