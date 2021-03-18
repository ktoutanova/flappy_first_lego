#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

from replay_follow_line import line_following

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information

'''
Scorpion is the pull-up bar on the top of the robot. 
'''
class Scorpion:
    def __init__(self, ev3, port):
        '''
        Assume the initial position to be fully back
        It takes 520 degrees to go all the way
        '''
        self.tail = Motor(port)
        #print(self.tail.angle())

    # positive speed moving down
    def down(self, speed=800): 
        init_degree = self.tail.angle()
        print("Scorpion initial angle %s", init_degree)
        while True: 
            self.tail.run(speed)
            wait(5)
            if self.tail.angle()> init_degree + 300: 
                break
        print("Scorpion final angle %s", self.tail.angle())

    # speed needs to be negative
    def up(self, speed=-800): 
        init_degree = self.tail.angle()
        print("Scorpion initial angle %s", init_degree)
        while True: 
            self.tail.run(speed)
            wait(5)
            if self.tail.angle() < init_degree - 300: 
                break
        print("Scorpion final angle %s", self.tail.angle()) 

    def move(self, degrees, speed=None):
        if speed is None:
            speed = 300 if degrees >= 0 else -300
        if degrees * speed <= 0:
            return
        initial_angle = self.tail.angle()
        print("move, initial angle %s" % initial_angle)
        while True:
            angle = self.tail.angle()
            if speed < 0 and angle <= initial_angle + degrees:
                break
            if speed > 0 and angle >= initial_angle + degrees:
                break
            self.tail.run(speed)
            wait(5)
        self.tail.stop()
        print("after move, angle becomes %s" % self.tail.angle())

class Hand:
    def __init__(self, ev3, port):
        self.hand_motor = Motor(port)
        print(self.hand_motor.angle())

    # negative degrees are opening claws
    # negative speed for open
    def open_degrees(self, degrees, speed=-720):
        initial_angle = self.hand_motor.angle()
        print (initial_angle)
        while self.hand_motor.angle()>initial_angle+degrees: 
            self.hand_motor.run(speed)
            wait(100)
            print(self.hand_motor.angle())

        self.hand_motor.stop()
        print(self.hand_motor.angle())

    def close_degrees(self, degrees, speed=720):
        initial_angle = self.hand_motor.angle()
        print (initial_angle)

        while self.hand_motor.angle()<initial_angle+degrees: 
            self.hand_motor.run(speed)
            wait(100)
            print(self.hand_motor.angle())

        self.hand_motor.stop()
        print(self.hand_motor.angle())
    
    def run_time(self, dps, t):
        self.hand_motor.run_time(dps, t)
        print(self.hand_motor.angle)
    
    def raise_hand(self):
        self.hand_motor.run_until_stalled(250, duty_limit=50)


class Robot: 
    def __init__(self):
        self.ev3 = EV3Brick()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.C)
        self.drive_base = DriveBase(self.left_motor, self.right_motor, wheel_diameter=55.5, axle_track=104)
        self.hand = Hand(self.ev3, Port.D) 
        self.scorpion = Scorpion(self.ev3, Port.B) 
        self.line_sensor = ColorSensor(Port.S4)
#       self.gyro_sensor = calibrate_gyro(Port.S1)
#       self.ev3.speaker.say("Robot Initialized")


    def move_innovation_project(self):
        '''
        mission 1: right end of back bar at (5, 2) 
        '''
        self.drive_base.settings(turn_rate = 40, straight_speed=150)
        print (self.drive_base.state())
        self.drive_base.straight(730)
        self.drive_base.turn(-84) # -80 degrees before
        (distance, speed, angle, rotational_speed) = self.drive_base.state()
        print(self.drive_base.state())
        self.hand.open_degrees(-500)

    def move_step_counter(self):
        '''
            Mission 2
        '''
        #self.ev3.speaker.say("Step Counter")
        self.drive_base.stop()
        self.drive_base.settings(turn_rate=35, straight_speed=130)
        # TODO: Split this backup into two, one to get away from the
        # innovation project, then turn perpendicular to the wall, then
        # back up into the wall.
        self.drive_base.straight(-50)
        self.drive_base.turn(-15)
        self.drive_base.straight(-130) # Back up into the wall

        self.drive_base.stop()
        self.drive_base.settings(straight_speed=75)
        self.drive_base.straight(25)
        # TODO: Turn less here, to get closer to the wall,
        # but then turn a little more before the slow backup,
        # to keep the straight gear pressed slightly away from
        # the wall, so it's less likely to stick.
        self.drive_base.turn(-95)
        self.drive_base.straight(-90)
        self.drive_base.stop()
        self.drive_base.settings(straight_speed = 20)
        self.drive_base.straight(-205)
        self.hand.close_degrees(1900)
        
        #turn_to(0, gyro_sensor, robot)
        '''self.drive_base.straight(-100)
        line_following(speed=20, distance=310, robot=self.drive_base, line_sensor=self.line_sensor)
        print (self.drive_base.state())
        self.drive_base.stop()
        '''
    def treadmill(self):
        self.drive_base.stop()
        self.drive_base.settings(straight_speed = 115, turn_rate=90)
        #self.ev3.speaker.say("The Treadmill Mission.")
        #self.hand.close_degrees(1500)
        self.drive_base.straight(100)
        self.drive_base.turn(70)
        self.drive_base.straight(87)
        self.drive_base.turn(80)
        self.drive_base.stop()
        self.drive_base.settings(turn_rate=40)
        # speed 70 works
        # speed 100 is unreliable
        line_following(speed=70, distance=700, robot=robot.drive_base, 
            line_sensor=robot.line_sensor, proportional_gain=-3)
        self.drive_base.stop()
        self.drive_base.settings(straight_speed = 100)
        self.drive_base.straight(140)
        self.drive_base.stop()
        # when the speed is 500, there's a chance that 
        # the robot will drive off of the treadmill
        self.right_motor.run_time(speed=300, time=6700)
    '''
    def drag_blue_wheel(self):
        self.hand.open_degrees(-1500)
        self.drive_base.stop()
        self.drive_base.settings(straight_speed = 30)
        self.drive_base.straight(150)
        self.hand.close_degrees(200, speed=100)
        self.drive_base.straight(-100)
    '''
    def treadmill_exit(self):
        
        #self.ev3.speaker.say("Exiting treadmill.")
        self.drive_base.stop()
        self.drive_base.settings(straight_speed = 105, turn_rate = 80)
        self.drive_base.straight(-180)
        self.drive_base.turn(-90)
        self.drive_base.straight(-190)
        ''' #original code: 
        self.drive_base.turn(60)
        self.drive_base.straight(-100)
        self.drive_base.turn(-90)
        self.drive_base.straight(-80)
        self.hand.close_degrees(200, speed=100)
        self.drive_base.straight(-250)
        '''
        '''self.drive_base.straight(145)
        self.drive_base.turn(30)
        self.drive_base.straight(60)
        self.drive_base.turn(-50)
        self.drag_blue_wheel()
        '''
    def row_machine(self):
        self.drive_base.stop()
        self.drive_base.settings(straight_speed=70, turn_rate=35)
        #self.ev3.speaker.say("The Roe Machine")
        robot.hand.open_degrees(-2500)
        self.drive_base.straight(50)
        self.drive_base.turn(35)
        self.drive_base.straight(140)
        self.hand.close_degrees(1100)
        self.drive_base.turn(-40)
        self.drive_base.straight(-10)
        #wait(2000)
        '''
        Back up a little bit after Row Machine,
        then turn right to avoid hitting treadmill,
        then back up into wall
        '''
        self.hand.open_degrees(-1000)
        self.drive_base.straight(-40)
        self.drive_base.turn(48)
        self.drive_base.straight(-110)
        self.drive_base.turn(-46)
        self.drive_base.straight(-100)

    def phone(self):
        self.drive_base.stop()
        self.drive_base.settings(straight_speed=90, turn_rate=80)
        self.drive_base.straight(85)

        self.drive_base.turn(-30)
        self.drive_base.straight(170)

        self.drive_base.turn(30)
        self.drive_base.straight(400)

        self.drive_base.turn(-44)
        self.drive_base.straight(150)
        self.hand.close_degrees(2600)

    def phone_exit(self):
        self.drive_base.turn(-46)
        self.drive_base.straight(-470)

    def slide (self):
        self.drive_base.stop()
        self.drive_base.settings(straight_speed=120, turn_rate=80)
        self.drive_base.straight(400)
        self.drive_base.turn(-32)
        self.drive_base.straight(210)
        self.drive_base.stop()
        self.drive_base.settings(turn_rate=35)
        line_following(speed=70, distance=300, robot=robot.drive_base, 
            line_sensor=robot.line_sensor, proportional_gain=-3)
        #self.hand.close_degrees(1500)
        self.drive_base.turn(-25)
        self.drive_base.straight(40)
        self.hand.open_degrees(-50)
        self.drive_base.straight(-170)
        #robot.scorpion.move(1000, speed=800)
        #robot.scorpion.move(500, speed=800)

    def bench(self):
        self.drive_base.turn(24)
        self.drive_base.straight(820)
        self.drive_base.straight(-760)

    '''
    def pullup_bar(self):
        self.drive_base.straight(666)
        self.drive_base.turn(-90)
        self.drive_base.straight(550)
        self.drive_base.turn(-90)
        self.drive_base.straight(300)

        self.scorpion.move(450, speed=300)
        self.scorpion.tail.hold()
        wait(3000)
        self.scorpion.move(-450, speed=-300)
        self.drive_base.straight(-100)
        self.scorpion.move(500, speed=300)
        self.drive_base.straight(300)

    def bench(self):
        self.hand.close_degrees(100)
        self.drive_base.straight(-160)
        self.drive_base.turn(36)
        self.hand.open_degrees(-150)
        self.drive_base.straight(680)
        self.drive_base.turn(-40)
        self.drive_base.straight(140)
        #self.drive_base.turn(10)
        #line_following(speed=70, distance=400, robot=robot.drive_base, 
            #line_sensor=robot.line_sensor, proportional_gain=-3)

    def bench_pt2(self):
        self.hand.close_degrees(300)
        self.drive_base.straight(-50)
        self.drive_base.turn(40)
        self.drive_base.straight(110)
        self.drive_base.turn(-180)
        self.drive_base.straight(-210)
        self.drive_base.turn(90)
        self.drive_base.straight(-110)
        #self.drive_base.turn(-40)
        #self.drive_base.straight(50)
        #self.drive_base.turn(30)
        self.drive_base.straight(50)
        self.hand.open_degrees(-200)
        self.drive_base.straight(55)
        self.drive_base.turn(-5)
        self.hand.close_degrees(300)
    '''
    def pullup_bar(self):
        '''self.drive_base.straight(-250)
        self.drive_base.straight(200)
        self.drive_base.turn(-100)
        self.drive_base.straight(950)
        self.hand.close_degrees(600)
        self.drive_base.turn(95)
        self.drive_base.straight(400)
        self.drive_base.straight(-200)'''
        #self.hand.close_degrees(800)
        '''
        self.drive_base.turn(-205)
        self.drive_base.straight(830)
        self.drive_base.turn(100)
        self.drive_base.straight(350)
        self.drive_base.straight(-250)
        self.scorpion.up()
        self.drive_base.straight(200)
        self.scorpion.down()
        '''
        self.drive_base.stop()
        self.drive_base.settings(straight_speed=90, turn_rate=100)
        self.drive_base.turn(94)
        self.drive_base.straight(-300)
        self.scorpion.move(-450, speed=-300)
        self.drive_base.straight(115)
        self.scorpion.move(450, speed=300)
        self.scorpion.tail.hold()
        wait(120000)
        
    def go_home(self):
        self.drive_base.stop()
        self.drive_base.settings(straight_speed=200, turn_rate=115)
        self.drive_base.turn(-92)
        self.drive_base.straight(900)

def run_missions(): 
    robot.move_innovation_project()
    robot.move_step_counter()
    robot.treadmill()
    robot.treadmill_exit()
    robot.row_machine()
    robot.phone()
    robot.phone_exit()
    robot.slide()
    robot.bench()
    robot.pullup_bar()
    #robot.go_home() don't go home
    #robot.bench_pt2()
    #robot.pullup()

robot = Robot()
# Starting coordinate (5, 2)
run_missions()

#robot.hand.open_degrees(-1100)
#robot.hand.close_degrees(150)

'''
robot.move_step_counter()
robot.treadmill()
robot.treadmill_exit()
robot.row_machine()
robot.phone()
robot.phone_exit()

robot.slide()
robot.bench()
robot.pullup_bar()
'''

'''
Todo:
    [x] Faster Turning during innovation project mission
    [x] Faster backing up into the wall
    [x] Faster turning directly after step counter
    [x] Faster hand opening
    [x] Back up a little bit after Row Machine, then turn right to avoid hitting treadmill, then back up into wall
    [x] WAY Faster beginning
    [x] Speed up the robot when it's moving towards the step counter
    [x] Speed up Treadmill exit backup
    [x] Speed up Row Machine
    [x] speed up back up after innovation project
    [x] tighten robot hand (temporarily)
    [x] fix slide
    - pullup bar
    [x] turn less before grabbing row machine
    [x] close the hand more after backup after row machine
    [x] after step counter, transition onto the line faster
    - go home after pullup bar
    [x] turn more before step counter
    [x] drive more before treadmill
    [x] turn less while backing up after row machine
    [x] turn more before grabbing row machine
    [x] get farther away from treadmill
    [x] increase turn rate after step counter
    [x] back up less after treadmill
    [x] turn 90 after treadmill
    [x] go farther towards the row machine
    [x] back up more during pullup bar
    [x] go forward more at the pullup bar
'''