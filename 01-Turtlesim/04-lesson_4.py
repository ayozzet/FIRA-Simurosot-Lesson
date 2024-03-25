#!/usr/bin/env python3

import rospy
from turtlesim.msg import Color, Pose
from geometry_msgs.msg import Twist

class TurtleSubscriber:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0

    def callback2(self, data2):
        self.x = data2.x
        self.y = data2.y
        self.theta = data2.theta
        self.linear_vel = data2.linear_velocity
        self.angular_vel = data2.angular_velocity
        rospy.loginfo("Received from topic2: x=%.2f, y=%.2f, theta=%.2f, linear_vel=%.2f, angular_vel=%.2f",
                      self.x, self.y, self.theta, self.linear_vel, self.angular_vel)

def main():
    rospy.init_node('topic_subscriber_publisher_node', anonymous=True)
    turtle_subscriber = TurtleSubscriber()
    rospy.Subscriber("/turtle1/pose", Pose, turtle_subscriber.callback2)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
    move_msg = Twist()
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
        current_x = turtle_subscriber.x
        # rospy.loginfo("Current x value: %.2f", current_x)
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
    except rospy.ROSInterruptException:
        pass
