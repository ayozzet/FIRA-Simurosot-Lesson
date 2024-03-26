#!/usr/bin/env python3

import rospy
from turtlesim.msg import Color, Pose
from geometry_msgs.msg import Twist

red = green = blue = 0
x = y = degree = l_vel = a_vel = 0

def callback1(data1):
    global red, green, blue
    red = data1.r
    green = data1.g
    blue = data1.b
    print(red, green, blue)

def callback2(data2):
    global x, y, degree, l_vel, a_vel
    x = data2.x
    y = data2.y
    degree = data2.theta
    l_vel = data2.linear_velocity
    a_vel = data2.angular_velocity

    x = float("{:.2f}".format(x))
    y = float("{:.2f}".format(y))
    degree = float("{:.2f}".format(degree))
    l_vel = float("{:.2f}".format(l_vel))
    a_vel = float("{:.2f}".format(a_vel))

    print(x, "\t", y, "\t", degree, "\t", l_vel, "\t", a_vel)


def main():
    rospy.init_node('Penyu_berlari', anonymous=False)
    rospy.Subscriber("/turtle1/color_sensor", Color, callback1)
    rospy.Subscriber("/turtle1/pose", Pose, callback2)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
    move_msg=Twist()

    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        move_msg.linear.x = 0.8
        move_msg.angular.z = 0.5
        pub.publish(move_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except:
        pass