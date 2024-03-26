#!/usr/bin/env python3

import message_filters
import rospy
from std_msgs.msg import Empty
from sensor_msgs.msg import Image, Range
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import time

height = float()
t = 0
l = 0

class image_converter(object):
    def __init__(self):
        self.bridge = CvBridge()
        self.front = message_filters.Subscriber('/drone/front_camera/image_raw', Image)
        self.down = message_filters.Subscriber('/drone/down_camera/image_raw', Image)
        self.ctrl_c = False
        self.rate = rospy.Rate(10)

    def callback1(self, data1):
        #rospy.loginfo(data.range)
        global sonar_f
        sonar_f = data1.range
   
    def publish_once_in_cmd_vel(self, cmd):
        while not self.ctrl_c:
            connections = self._pub_cmd_vel.get_num_connections()
            if connections > 0:
                self._pub_cmd_vel.publish(cmd)
                # rospy.loginfo("Publish in cmd_vel...")
                break
            else:
                self.rate.sleep()

    # function that stops the drone from any movement
    def stop_drone(self):
        # rospy.loginfo("Stopping...")
        self._move_msg.linear.x = 0.0
        self._move_msg.linear.y = 0.0
        self._move_msg.linear.z = 0.0
        self._move_msg.angular.z = 0.0
        self.publish_once_in_cmd_vel(self._move_msg)
        # time.sleep(0.3)    

    def take_off(self):
        global t
        # rospy.loginfo("Take off...")
        self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self._takeoff_msg = Empty()
        while not t == 3:
            rospy.loginfo("Take off...")
            self._pub_takeoff.publish(self._takeoff_msg)
            rospy.loginfo('Taking off...')
            time.sleep(0.3)
            t += 1
        self.stop_drone()

    def landing(self):
        global l
        # rospy.loginfo("Landing...")
        self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
        self._land_msg = Empty()
        l=0
        while not l == 3:
            rospy.loginfo("Landing...")
            self._pub_land.publish(self._land_msg)
            rospy.loginfo('Landing...')
            time.sleep(1)
            l += 1

    # def move_trick(self):
    def callback(self, front):
        self._pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._move_msg = Twist()

        cv_image_front = self.bridge.imgmsg_to_cv2(front, "bgr8")

        son_current = float("{:.2f}".format(son_current))
        print("SONAR:" + str(son_current))
        
        cv2.imshow("Front_Cam", cv_image_front)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.signal_shutdown('Quit')
            cv2.destroyAllWindows()

def main():
    rospy.init_node('move_trick')
    move_trick = image_converter()
    sub1 = rospy.Subscriber("/drone/sonar", Range, move_trick.callback1)
    try:
        ts = message_filters.ApproximateTimeSynchronizer([move_trick.down,move_trick.front],10,0.1)
        ts.registerCallback(move_trick.callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        print("Shutting down")
        pass

if __name__ == '__main__':
    main()
