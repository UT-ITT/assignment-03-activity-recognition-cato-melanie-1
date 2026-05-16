#DONE
#read training data from csv files
#pre-process training data
#split into train and test dataset
#train ML classifier
#evaluate accuracy using test dataset
#try more preprocessing to get higher accuracy

#TODO
#design pyglet fitness app
#take sensor data from dippid and predict which activity is being done
#also predict if it is done correctly?

#document how our training data is structured in README

#note:
#put all functions that are not related to visualization in activity_recognizer
#and just call them here


# this program visualizes activities with pyglet
from activity_recognizer import ActivityRecognizer
from DIPPID import SensorUDP
import pyglet
from pyglet import window
import os

PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
win.set_caption("Fitness Trainer")

recognizer = ActivityRecognizer()
recognizer.train()


def update(dt):
    #todo
    #predict continuously
    #save last 200 values - 2s window

    #read sensor values
    acc_x = sensor.get_value('accelerometer')['x']
    acc_y = sensor.get_value('accelerometer')['y']
    acc_z = sensor.get_value('accelerometer')['z']
    gyro_x = sensor.get_value('gyroscope')['x']
    gyro_y = sensor.get_value('gyroscope')['y']
    gyro_z = sensor.get_value('gyroscope')['z']


@win.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        os._exit(0)


pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
