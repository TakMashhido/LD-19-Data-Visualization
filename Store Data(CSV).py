import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math
import csv

# Create a figure using pyplot from matplotlib
fig = plt.figure(figsize=(8,8))

# Create a subplot on the figure
ax = fig.add_subplot(111, projection='polar')
ax.set_title('Lidar LD19 (exit: Key E)', fontsize=18)

# Define the COM port for serial communication
com_port = "COM3"

# Create an event listener for pyplot
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

# Create and open a CSV file for writing
csv_file = open('lidar_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
# Write the header to the CSV file
csv_writer.writerow(['Angle', 'Distance'])

i = 0
while True:
    loopFlag = True
    flag2c = False

    if (i % 40 == 39):
        if ('line' in locals()):
            line.remove()

        # Update the plot
        print(len(angles))
        line = ax.scatter(angles, distances, c="blue", s=5)
        ax.set_theta_offset(math.pi / 2)
        plt.pause(0.01)
        
        # Write the angles and distances to the CSV file
        for angle, distance in zip(angles, distances):
            csv_writer.writerow([angle, distance])

        # Clear the lists of angles and distances
        angles.clear()
        distances.clear()

        i = 0

    while loopFlag:
        b = ser.read()
        tmpInt = int.from_bytes(b, 'big')

        if (tmpInt == 0x54):
            tmpString += b.hex() + " "
            flag2c = True
            continue

        elif (tmpInt == 0x2c and flag2c):
            tmpString += b.hex()

            if (not len(tmpString[0:-5].replace(' ','')) == 90):
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            lidarData = CalcLidarData(tmpString[0:-5])
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)

            tmpString = ""
            loopFlag = False
        else:
            tmpString += b.hex() + " "

        flag2c = False

    i += 1

# Close the serial connection and the CSV file
ser.close()
csv_file.close()
