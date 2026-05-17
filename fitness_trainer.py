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
#design pyglet fitness app
    #1st screen: display all activities, explain how it works
    #if activity is recognized (0 or 1), switch to screen of that activity with correct text


#TODO
#test some more
#make design prettier (e.g. nicer font, better image placement)

# this program visualizes activities with pyglet
from activity_recognizer import *
from DIPPID import SensorUDP
import pyglet
from pyglet import window
from pyglet.gl import glClearColor
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
glClearColor(1, 1, 1, 1) #background color white

#images
#load
img_jumpingjack_1 = pyglet.resource.image("img/jumpingjack_1.png")
img_jumpingjack_2 = pyglet.resource.image("img/jumpingjack_2.png")
img_rowing_1 = pyglet.resource.image("img/rowing_1.png")
img_rowing_2 = pyglet.resource.image("img/rowing_2.png")
img_running_1 = pyglet.resource.image("img/running_1.png")
img_running_2 = pyglet.resource.image("img/running_2.png")
img_lifting_1 = pyglet.resource.image("img/lifting_1.png")
img_lifting_2 = pyglet.resource.image("img/lifting_2.png")

#create drawable sprites
jump_1 = pyglet.sprite.Sprite(img=img_jumpingjack_1)
jump_2 = pyglet.sprite.Sprite(img=img_jumpingjack_2)
row_1 = pyglet.sprite.Sprite(img=img_rowing_1)
row_2 = pyglet.sprite.Sprite(img=img_rowing_2)
run_1 = pyglet.sprite.Sprite(img=img_running_1)
run_2 = pyglet.sprite.Sprite(img=img_running_2)
lift_1 = pyglet.sprite.Sprite(img=img_lifting_1)
lift_2 = pyglet.sprite.Sprite(img=img_lifting_2)

#labels 
label_x = 10
label_y = WINDOW_HEIGHT - 50
label_color = (0,0,0)
label_font_size = 20

label_0 = pyglet.text.Label(text=f"Good job on your {recognized_activity}, keep going!", x=label_x, y=label_y, align='center', color=label_color, font_size = label_font_size)
label_1 = pyglet.text.Label(text=f"It seems like you are trying to work on your fitness with {recognized_activity}, but you are not performing the exercise quite right. Take a closer look at the displayed activity and try to fix your form!", x=label_x, y=label_y, multiline=True, width=WINDOW_WIDTH-20, align="center", color=label_color, font_size = label_font_size)
label_2 = pyglet.text.Label(text="None of the displayed activities recognized. Pick one from the 4 displayed above and start moving. The app will automatically recognize your movement and display if you are doing the exercise correctly.", x=label_x, y=label_y, multiline=True, width=WINDOW_WIDTH-20, align="center", color=label_color, font_size = label_font_size)

print("fitness app ready")

#set up empty data frame to collect input from DIPPID app
input = {
    "acc_x": [],
    "acc_y": [],
    "acc_z": [],
    "gyro_x": [],
    "gyro_y": [],
    "gyro_z": []
}
input_df = pd.DataFrame(input)

#collect input data every ms and update status and recognized activity every 2s
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
        

#stop on q
@win.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        os._exit(0)

#stop on clicking x
@win.event
def on_close():
    os._exit(0)

#draw text and images in window
@win.event
def on_draw():
    global status, recognized_activity
    global label_0, label_1, label_2
    global jump_1

    win.clear()

    if status == 2:
        #start screen, none of the movements recognized
        label_2.draw()
        start_scale = 0.15
        spacer = 50

        row_1.x = 10
        row_1.y = 10
        row_1.scale = start_scale - 0.05
        row_2.x = row_1.width + spacer
        row_2.y = 10
        row_2.scale = start_scale - 0.05
        row_1.draw()
        row_2.draw()

        lift_1.x = WINDOW_WIDTH/2 + spacer
        lift_1.y = 10
        lift_1.scale = start_scale
        lift_2.x = WINDOW_WIDTH/2 + lift_1.width + 2*spacer
        lift_2.y = 10
        lift_2.scale = start_scale
        lift_1.draw()
        lift_2.draw()

        jump_1.x = 10
        jump_1.y = row_1.height + spacer
        jump_1.scale = start_scale
        jump_2.x = jump_1.width + spacer
        jump_2.y = row_2.height + spacer
        jump_2.scale = start_scale
        jump_1.draw()
        jump_2.draw()

        run_1.x = WINDOW_WIDTH/2 + spacer
        run_1.y = lift_1.height + spacer
        run_1.scale = start_scale
        run_2.x = WINDOW_WIDTH/2 + run_1.width + 2* spacer
        run_2.y = lift_2.height + spacer
        run_2.scale = start_scale
        run_1.draw()
        run_2.draw()


        #print(f"status: {status}, activity: {recognized_activity}")
    else:
        recognized_scale = 0.2

        #display recognized activity
        if recognized_activity == "jumpingjacks":
            jump_1.x = 100
            jump_1.y = 10
            jump_1.scale = recognized_scale
            jump_2.x = WINDOW_WIDTH/2 + 100
            jump_2.y = 10
            jump_2.scale = recognized_scale
            jump_1.draw()
            jump_2.draw()
        elif recognized_activity == "running":
            run_1.x = 100
            run_1.y = 10
            run_1.scale = recognized_scale
            run_2.x = WINDOW_WIDTH/2 + 100
            run_2.y = 10
            run_2.scale = recognized_scale
            run_1.draw()
            run_2.draw()
        elif recognized_activity == "rowing":
            row_1.x = 10
            row_1.y = 10
            row_1.scale = recognized_scale
            row_2.x = WINDOW_WIDTH/2 + 10
            row_2.y = 10
            row_2.scale = recognized_scale
            row_1.draw()
            row_2.draw()
        elif recognized_activity == "lifting":
            lift_1.x = 100
            lift_1.y = 10
            lift_1.scale = recognized_scale
            lift_2.x = WINDOW_WIDTH/2 + 100
            lift_2.y = 10
            lift_2.scale = recognized_scale
            lift_1.draw()
            lift_2.draw()
        if status == 1:
            #movement not executed correctly
            label_1.text = f"It seems like you are trying to work on your fitness with {recognized_activity}, but you are not performing the exercise quite right. Take a closer look at the displayed activity and try to fix your form!"
            label_1.draw()
            #print(f"status: {status}, activity: {recognized_activity}")
        else:
            #movement executed correctly
            label_0.text = f"Good job on your {recognized_activity}, keep going!"
            label_0.draw()
            #print(f"status: {status}, activity: {recognized_activity}")
        





pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
