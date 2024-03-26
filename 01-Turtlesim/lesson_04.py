#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class NinjaTurtle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0

    def callback1(self, data1):
        self.x = data1.x
        self.y = data1.y
        self.theta = data1.theta
        self.linear_vel = data1.linear_velocity
        self.angular_vel = data1.angular_velocity

def main():
    rospy.init_node('Ninja_Turtle', anonymous=True)
    ninja_turtle = NinjaTurtle()
    rospy.Subscriber("/turtle1/pose", Pose, ninja_turtle.callback1)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
    move_msg=Twist()
    
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        current_x = ninja_turtle.x
        current_x = float("{:.2f}".format(current_x))
        print(current_x)

        move_msg.linear.x = 1.0
        move_msg.angular.z = 0.5
        pub.publish(move_msg)

        if current_x > 6.0:
            move_msg.linear.x = 1.0
            move_msg.angular.z = -0.5
            pub.publish(move_msg)
            rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
