#!/usr/bin/env python3

import message_filters
import rospy
from std_msgs.msg import Empty
from sensor_msgs.msg import Image, Range
from geometry_msgs.msg import Pose, Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time

height = float()
t = 0
l = 0
hi_static = 0.35   #1.14  / 2.19:heighest alt  / 1.41:1stGate  / 0.35:LowestGetThrough
hi_tolerance = 0.02

class image_converter(object):
    def __init__(self):
        self.bridge = CvBridge()
        self.front = message_filters.Subscriber('/drone/front_camera/image_raw', Image)
        self.down = message_filters.Subscriber('/drone/down_camera/image_raw', Image)
        self.ctrl_c = False
        self.rate = rospy.Rate(10)

    def callback2(self, data2):
        #rospy.loginfo(data.range)
        global height
        height = data2.position.z

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
    def callback(self,front):
        global height, sonar_f, hi_static, hi_tolerance, moving
        self._pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._move_msg = Twist()

        cv_image_front = self.bridge.imgmsg_to_cv2(front, "bgr8")

        hi_current = float("{:.2f}".format(height))

        while not s == 1:
            self.take_off()
            self.stop_drone()
            s+=1
        
        if hi_current > (hi_static+hi_tolerance):
            print("DOWN")
            moving = "DOWN"
            self.move_down_drone()
            print(hi_current)
        if hi_current < (hi_static-hi_tolerance):
            print("UP")
            moving = "UP"
            self.move_up_drone()
        if (hi_current > hi_static-hi_tolerance) and (hi_current < hi_static+hi_tolerance):
            moving = "STATIC"
        
        print("HEIGHT:" + str(hi_current) +"\tZ-ACTION:"+ moving)
        
        cv2.imshow("Front_Cam", cv_image_front)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.signal_shutdown('Quit')
            cv2.destroyAllWindows()

def main():
    rospy.init_node('move_trick')
    move_trick = image_converter()
    sub2 = rospy.Subscriber("/drone/gt_pose", Pose, move_trick.callback2)
    try:
        ts = message_filters.ApproximateTimeSynchronizer([move_trick.down,move_trick.front],10,0.1)
        ts.registerCallback(move_trick.callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        print("Shutting down")
        pass

if __name__ == '__main__':
    main()
