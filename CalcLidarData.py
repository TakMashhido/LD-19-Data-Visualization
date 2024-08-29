import math

class LidarData:
    def __init__(self, FSA, LSA, CS, Speed, TimeStamp, Degree_angle, Angle_i, Distance_i):
        self.FSA = FSA  # Start angle of the LIDAR data packet (in degrees)
        self.LSA = LSA  # End angle of the LIDAR data packet (in degrees)
        self.CS = CS  # Checksum for data integrity verification
        self.Speed = Speed  # Rotational speed of the LIDAR (in degrees/second)
        self.TimeStamp = TimeStamp  # Timestamp when the data was captured (in milliseconds)
        self.Degree_angle = Degree_angle  # List of angles for the data points (in degrees)
        self.Angle_i = Angle_i  # List of angles for the data points (in radians)
        self.Distance_i = Distance_i  # List of distances for each angle (in meters)

def CalcLidarData(data_str):
    # Remove spaces from the input string
    data_str = data_str.replace(' ', '')
    
    # Extract the LIDAR's rotational speed from the first 4 characters (2 bytes), 
    # reversing the byte order and converting it to a decimal value. The speed is divided by 100.
    Speed = int(data_str[2:4] + data_str[0:2], 16) / 100

    # Extract the start angle (FSA) from the next 4 characters (2 bytes), 
    # reversing the byte order and converting it to a decimal value. The angle is divided by 100.
    FSA = float(int(data_str[6:8] + data_str[4:6], 16)) / 100

    # Extract the end angle (LSA) from the string. This is done similarly to FSA, 
    # taking the appropriate bytes from the end of the string.
    LSA = float(int(data_str[-8:-6] + data_str[-10:-8], 16)) / 100

    # Extract the timestamp from the last 4 bytes before the checksum, 
    # reversing the byte order and converting it to a decimal value.
    TimeStamp = int(data_str[-4:-2] + data_str[-6:-4], 16)

    # Extract the checksum (CS) from the last 2 characters (1 byte) of the string.
    CS = int(data_str[-2:], 16)

    # Initialize lists to store the confidence, angles (in radians), and distances.
    Degree_angle = list()  # Angles in degrees
    Angle_i = list()  # Angles in radians
    Distance_i = list()  # Distances in meters

    # Calculate the angular step between data points. If the end angle (LSA) is greater than the start angle (FSA),
    # simply subtract them. If not, account for the 360-degree wraparound.
    if LSA - FSA > 0:
        angleStep = float(LSA - FSA) / 12
    else:
        angleStep = float((LSA + 360) - FSA) / 12

    counter = 0
    # Define a lambda function to handle angles that might exceed 360 degrees.
    circle = lambda deg: deg - 360 if deg >= 360 else deg

    # Loop through the data points in the packet. Each data point is 6 characters (3 bytes) long.
    for i in range(0, 6 * 12, 6):
        # Extract the distance value from the appropriate bytes, reverse the byte order, 
        # convert it to a decimal value, and divide by 1000 to get meters.
        Distance_i.append(int(data_str[8+i+2 : 8+i+4] + data_str[8+i : 8+i+2], 16) / 1000)
        
        # Calculate the angle for each data point in degrees using the angular step and the start angle (FSA).
        # Store the angle in degrees and radians.
        Degree_angle.append(circle(angleStep * counter + FSA))
        Angle_i.append(circle(angleStep * counter + FSA) * math.pi / 180.0)
        
        counter += 1

    # Create a LidarData object with the extracted and calculated values.
    lidarData = LidarData(FSA, LSA, CS, Speed, TimeStamp, Degree_angle, Angle_i, Distance_i)
    
    # Return the LidarData object containing all the processed LIDAR data.
    return lidarData
