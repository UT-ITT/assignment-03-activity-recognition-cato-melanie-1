#DONE
#read training data from csv files
#pre-process training data
#split into train and test dataset
#train ML classifier
#evaluate accuracy using test dataset
#try more preprocessing to get higher accuracy
#take sensor data from dippid and predict which activity is being done
#predict if it is done correctly
#document how to start the fitness App in README

#TODO
#design pyglet fitness app
    #1st screen: display all activities, explain how it works
    #if activity is recognized (0 or 1), switch to screen of that activity with correct text


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

#variables for displaying the correct screen
recognized_activity = "none"
#2 = nothing recognized, 1 = recognized, but not correct, 0 = recognized correctly executed movement
status = 2

recognizer = ActivityRecognizer()
print("starting up activity recognizer...\n")
recognizer.train()

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
win.set_caption("Fitness Trainer")

#images
#FIXME
jump_1 = pyglet.resource.image("img/jumpingjack_1.png")

#labels 
label_x = 10
label_y = WINDOW_HEIGHT - 20


label_0 = pyglet.text.Label(text=f"Good job on your {recognized_activity}, keep going!", x=label_x, y=label_y, align='center')
label_1 = pyglet.text.Label(text=f"It seems like you are trying to work on your fitness with {recognized_activity}, but you are not performing the exercise quite right. Take a closer look at the displayed activity and try to fix your form!", x=label_x, y=label_y, multiline=True, width=WINDOW_WIDTH-20, align="center")
label_2 = pyglet.text.Label(text="None of the displayed activities recognized. Pick one from the 4 displayed above and start moving. The app will automatically recognize your movement and display if you are doing the exercise correctly.", x=label_x, y=label_y, multiline=True, width=WINDOW_WIDTH-20, align="center")

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

    global input_df, status, recognized_activity
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
            status, recognized_activity = recognizer.predict(input_df)

            #reset/empy input data frame for next recognition
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

@win.event
def on_draw():
    global status, recognized_activity
    global label_0, label_1, label_2
    global jump_1

    win.clear()
    if status == 2:
        #start screen, none of the movements recognized
        label_2.draw()
        print(f"status: {status}, activity: {recognized_activity}")
    else:
        #display recognized activity
        ... #FIXME
        if status == 1:
            #movement not executed correctly
            label_1.text = f"It seems like you are trying to work on your fitness with {recognized_activity}, but you are not performing the exercise quite right. Take a closer look at the displayed activity and try to fix your form!"
            label_1.draw()
            print(f"status: {status}, activity: {recognized_activity}")
        else:
            #movement executed correctly
            label_0.text = f"Good job on your {recognized_activity}, keep going!"
            label_0.draw()
            print(f"status: {status}, activity: {recognized_activity}")
        





pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
