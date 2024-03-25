#!/usr/bin/env python3

import rospy
from turtlesim.msg import Color, Pose
from geometry_msgs.msg import Twist

red = green = blue = 0
x = y = theta = linear_vel = angular_vel = 0

def callback1(data1):
    global red, green, blue
    red = data1.r
    green = data1.g
    blue = data1.b
    rospy.loginfo("Received from topic1: red=%d, green=%d, blue=%d", red, green, blue)

def callback2(data2):
    global x, y, theta, linear_vel, angular_vel
    x = data2.x
    y = data2.y
    theta = data2.theta
    linear_vel = data2.linear_velocity
    angular_vel = data2.angular_velocity
    rospy.loginfo("Received from topic2: x=%.2f, y=%.2f, theta=%.2f, linear_vel=%.2f, angular_vel=%.2f",
                  x, y, theta, linear_vel, angular_vel)
    
def main():
    rospy.init_node('topic_subscriber_publisher_node', anonymous=True)
    rospy.Subscriber("/turtle1/color_sensor", Color, callback1)
    rospy.Subscriber("/turtle1/pose", Pose, callback2)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
    move_msg = Twist()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        move_msg.linear.x = 1.0  
        move_msg.angular.z = 0.5  
        pub.publish(move_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

