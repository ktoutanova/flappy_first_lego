"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# follow the line at the speed for distance for this robot
def line_following(speed, distance, robot, line_sensor, proportional_gain):

    #(straight_speed, straight_acceleration, turn_rate, turn_acceleration) = robot.settings()
    #print ("%s %s %s %s" % (straight_speed, straight_acceleration, turn_rate, turn_acceleration))
    #return

    # Calculate the light threshold. Choose values based on your measurements.
    # We are using the green of color sensor's rgb()
    #BLACK = 3 #9
    #WHITE = 34 #85
    #threshold = (BLACK + WHITE) / 2

    threshold = 11

    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drivebase to 1.2 degrees per second.

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at (threshold * proportional_gain) degrees per second.

    target = robot.distance() + distance
    while robot.distance() < target:
        # Calculate the deviation from the threshold.
        print (line_sensor.rgb())
        deviation = line_sensor.rgb()[1] - threshold
        deviation = min (deviation, 5)
        deviation = max (deviation, -10)

        # Calculate the turn rate.
        turn_rate = proportional_gain * deviation

        # Set the drive base speed and turn rate.
        robot.drive(speed, turn_rate)

        # You can wait for a short time or do other things in this loop.
        wait(10)


