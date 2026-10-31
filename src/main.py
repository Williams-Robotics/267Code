# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Vincent                                                        #
# 	Created:      10/31/2026, 11:23:48 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
'''
Controls: 

Left Stick:Forwards and Back
Right Stick: Rotation

Down DPAD: Toggle Reverse Driving(flip which way is forward, useful for grabbing vs scoring)
A:Toggle Tounge
B: Toggle Wing
X: Toggle Butt(Big Robot Only)
Y: Hold to enable strafing with left stick
'''
# Library imports
from vex import *


# Brain should be defined by default
brain = Brain()
controller = Controller(PRIMARY)
import math
#endregion
#region  MOTOR & PNEUMATICS CONFIGURATION 
# Configure your motor ports here
FRONT_LEFT_PORT = Ports.PORT10
FRONT_RIGHT_PORT = Ports.PORT20
BACK_LEFT1_PORT = Ports.PORT1
BACK_LEFT2_PORT = Ports.PORT1
BACK_RIGHT1_PORT = Ports.PORT11
BACK_RIGHT2_PORT = Ports.PORT11


# Configure motor reverse settings (True = reversed, False = normal)
FRONT_LEFT_REVERSE = True
FRONT_RIGHT_REVERSE = True
BACK_LEFT1_REVERSE = False
BACK_LEFT2_REVERSE = False
BACK_RIGHT1_REVERSE = False
BACK_RIGHT2_REVERSE = False

#endregion
#region  SENSOR CONFIG
AI_PORT=Ports.PORT20
INT_PORT=Ports.PORT21
#endregion
#region  DRIVE INIT
# Initialize motors with configured ports and reverse settings
front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_6_1, FRONT_LEFT_REVERSE)
front_right = Motor(FRONT_RIGHT_PORT, GearSetting.RATIO_6_1, FRONT_RIGHT_REVERSE)
back_left1 = Motor(BACK_LEFT1_PORT, GearSetting.RATIO_6_1, BACK_LEFT1_REVERSE)
back_left2= Motor(BACK_LEFT2_PORT, GearSetting.RATIO_6_1, BACK_LEFT2_REVERSE)
back_right1 = Motor(BACK_RIGHT1_PORT, GearSetting.RATIO_6_1, BACK_RIGHT1_REVERSE)
back_right2 = Motor(BACK_RIGHT2_PORT, GearSetting.RATIO_6_1, BACK_RIGHT2_REVERSE)
#endregion
#region  INTAKE FUNCS
back_left=MotorGroup(back_left1,back_left2)
back_right=MotorGroup(back_right1,back_right2)

def drive():
    forward = controller.axis3.position()  # Left stick Y-axis
    turn_val = controller.axis1.position() 
    if abs(turn_val)<10:turn=2*abs(turn_val)
    elif abs(turn_val)<60: turn=.006*((abs(turn_val)-10)**2)+20
    else: turn=40+((60/(math.exp(2)-1))*(math.exp(.05*(abs(turn_val)-60))-1))
    if turn_val<0: turn*=-1
    
    front_left_speed = forward + turn
    front_right_speed = forward - turn
    back_left_speed = forward + turn
    back_right_speed = forward - turn
    
    # Set motor velocities
    front_left.spin(FORWARD, front_left_speed, PERCENT)
    front_right.spin(FORWARD, front_right_speed, PERCENT)
    back_left.spin(FORWARD, back_left_speed, PERCENT)
    back_right.spin(FORWARD, back_right_speed, PERCENT)

#endregion'

#region  SENSOR INIT

# AI Classification Competition Element IDs - Push Back
# class GameElementsPushBack:
#     BLUE_BLOCK = 0
#     RED_BLOCK = 1
# # AI Vision Color Descriptions
# ai__BBLUE = Colordesc(1, 32, 154, 226, 10, 0.2)
# ai__BRED = Colordesc(2, 231, 42, 92, 10, 0.2)


# Initialize motors with configured ports and reverse settings
# front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)

ai = AiVision(AI_PORT, AiVision.ALL_AIOBJS,AiVision.ALL_TAGS)
int=Inertial(INT_PORT)
timer = Timer()

#endregion

#region DRIVETRAIN FUNCS
def ai_stuff():
    obj=ai.take_snapshot(AiVision.ALL_AIOBJS)
    for item in obj:
        print("Score: {}".format((item.score)))
        print("ID: {}".format((item.id)))
        print("X: {}, Y: {}".format(item.centerX, item.centerX))

def stop_drive():
    """Stop all drive motors."""
    front_left.stop(HOLD)
    front_right.stop(HOLD)
    back_left.stop(HOLD)
    back_right.stop(HOLD)

def wrap_angle(a):
    if a > 180: a -= 360
    if a < -180: a += 360
    return a


#region SENSOR FUNCS

def PID(desired_state,current_state,Kp,Ki,Kd,prev_error,total_error):
    #Blank PID Function, so we can use it everywhere
    '''
    ### PID Function
   
    desired_state-- What we want
    
    current_state-- where we are
    
    Kp,Ki,Kd: Tuning variables
    
    Prev_error: previous error
    
    total_error: total error
    '''
    
    '''## Desired position (adjust number based on what we need the robot to do)
    desired_state = 0

    ## Variables used in PID algo (adjust numbers based on what we need the robot to do)
    Kp = 0
    Ki = 0
    Kd = 0
    ## Remember to test each constants one at a time, this affects output of PID controller

    Ki_total = 0 # sum from integral
    prev_error = 0

    while True():'''
    ## get error
    error = desired_state - current_state
    ## Kp : proportional correction
    proportional = Kp * error
    ## Ki : integral correction
    total_error += error ## add current error to summation
    integral = Ki * total_error ## get Ki Result by applying tuning constant to total
    ## consider limits on Ki perchance?
    ## Kd : derivative
    derivative = Kd * (error - prev_error)
    prev_error = error
    ## sum P, I, and D
    PID_result = proportional + integral + derivative
    return PID_result, prev_error,total_error
    ## apply PID_result (sum) to the bot depending on which component we want it to adjust

def initialize():
    int.calibrate
    int.set_heading(0)
    wait(1500,MSEC)
    # gpsavg=[]


#other funcs here
#endregion 
#region  MAIN PROGRAM 
initialize()

brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")


def user_control():
    # COMMENT OUT FOR THE ACTUAL
    while True:
        controller.screen.clear_screen()
        ai_stuff()
        drive()
        wait(10, MSEC)
#endregion

# create competition instance
# comp = Competition(user_control, autonomous_v2_blue)

# actions to do when the program starts
brain.screen.clear_screen()
user_control()
# autonomous()