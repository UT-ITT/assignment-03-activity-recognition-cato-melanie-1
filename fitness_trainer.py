#DONE
#read training data from csv files
#pre-process training data
#split into train and test dataset
#train ML classifier
#evaluate accuracy using test dataset
#try more preprocessing to get higher accuracy
#take sensor data from dippid and predict which activity is being done

#TODO
#design pyglet fitness app
    #1st screen: display all activities, explain how it works
    #activity recognition starts after pressing button? (otherwise 1st screen is gone too fast)
#also predict if it is done correctly?

#document how to start the fitness App in README


# this program visualizes activities with pyglet
from activity_recognizer import *
from DIPPID import SensorUDP
import pyglet
from pyglet import window
import os

PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

recognizer = ActivityRecognizer()
print("starting up activity recognizer...\n")
recognizer.train()

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
win.set_caption("Fitness Trainer")
print("fitness app ready")

input = {
    "acc_x": [],
    "acc_y": [],
    "acc_z": [],
    "gyro_x": [],
    "gyro_y": [],
    "gyro_z": []
}
input_df = pd.DataFrame(input)

def update(dt):

    global input_df
    size = len(input_df)

    #read sensor data if received
    if not sensor.get_capabilities() == []:
        acc_x = sensor.get_value('accelerometer')['x']
        acc_y = sensor.get_value('accelerometer')['y']
        acc_z = sensor.get_value('accelerometer')['z']
        gyro_x = sensor.get_value('gyroscope')['x']
        gyro_y = sensor.get_value('gyroscope')['y']
        gyro_z = sensor.get_value('gyroscope')['z']

        #fill 2s window with input data
        if size < 200:
            input_df.loc[size] = [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
        #predict recognized movement every two seconds
        else: #size = 200
            print(recognizer.predict(input_df)) #FIXME use prediction in fitness app
            input = {
                "acc_x": [],
                "acc_y": [],
                "acc_z": [],
                "gyro_x": [],
                "gyro_y": [],
                "gyro_z": []
            }
            input_df = pd.DataFrame(input)

    else:
        raise Exception("Sorry, there seems to be a problem with the data input. Did you start the DIPPID app and set it to the correct IP and Port?")
        


@win.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        os._exit(0)


pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
