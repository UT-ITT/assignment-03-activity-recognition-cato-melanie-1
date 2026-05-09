from DIPPID import SensorUDP
from time import sleep, time
import pandas as pd

PORT = 5700
sensor = SensorUDP(PORT)


name = input("Name: ")
activity = input("Activity: ")

data = []

def callback():
    acc_x = sensor.get_value('accelerometer')['x']
    acc_y = sensor.get_value('accelerometer')['y']
    acc_z = sensor.get_value('accelerometer')['z'] 

    gyro_x = sensor.get_value('gyroscope')['x']
    gyro_y = sensor.get_value('gyroscope')['y']
    gyro_z = sensor.get_value('gyroscope')['z']

    current_time = time()

    row = {'id': len(data), 'timestamp': current_time, 
           'acc_x': acc_x, 'acc_y': acc_y, 'acc_z': acc_z,
           'gyro_x': gyro_x, 'gyro_y': gyro_y, 'gyro_z': gyro_z}
    
    data.append(row)


for i in range(5):

    print("Press Button 1 to start recording")

    while sensor.get_value("button_1") != 1:
        sleep(0.01)

    print("Recording...")

    data = []
    
    start_time = time()

    while (time() - start_time) < 10:
        callback()
        sleep(0.01)


    filename = f'{name}-{activity}-{i+1}.csv'
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


print(f'Recording {activity} done')
print("CSV files saved")
