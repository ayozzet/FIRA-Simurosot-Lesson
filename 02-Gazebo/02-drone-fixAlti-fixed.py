#!/usr/bin/env python3

import message_filters
import rospy
from std_msgs.msg import Empty
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time

height = float()
t = 0
l = 0
hi_static = 0.35
hi_tolerance = 0.02
s = 0  # Added missing variable `s`
moving = ""  # Initialize `moving` to prevent issues

class ImageConverter:
    def __init__(self):
        self.bridge = CvBridge()
        self.front = message_filters.Subscriber('/drone/front_camera/image_raw', Image)
        self.down = message_filters.Subscriber('/drone/down_camera/image_raw', Image)
        self._pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)

        self.ctrl_c = False
        self.rate = rospy.Rate(10)
        self._move_msg = Twist()
        self._takeoff_msg = Empty()
        self._land_msg = Empty()

    def callback2(self, data2):
        global height
        height = data2.position.z

    def publish_once_in_cmd_vel(self, cmd):
        while not self.ctrl_c:
            connections = self._pub_cmd_vel.get_num_connections()
            if connections > 0:
                self._pub_cmd_vel.publish(cmd)
                break
            else:
                self.rate.sleep()

    def stop_drone(self):
        self._move_msg.linear.x = 0.0
        self._move_msg.linear.y = 0.0
        self._move_msg.linear.z = 0.0
        self._move_msg.angular.z = 0.0
        self.publish_once_in_cmd_vel(self._move_msg)

    def take_off(self):
        global t
        while t < 3:
            rospy.loginfo("Take off...")
            self._pub_takeoff.publish(self._takeoff_msg)
            time.sleep(0.3)
            t += 1
        self.stop_drone()

    def landing(self):
        global l
        while l < 3:
            rospy.loginfo("Landing...")
            self._pub_land.publish(self._land_msg)
            time.sleep(1)
            l += 1

    def move_up_drone(self):
        self._move_msg.linear.z = 0.5  # Example value
        self.publish_once_in_cmd_vel(self._move_msg)

    def move_down_drone(self):
        self._move_msg.linear.z = -0.5  # Example value
        self.publish_once_in_cmd_vel(self._move_msg)

    def callback(self, front, down):
        global height, hi_static, hi_tolerance, s, moving

        cv_image_front = self.bridge.imgmsg_to_cv2(front, "bgr8")
        hi_current = float("{:.2f}".format(height))

        if s == 0:
            self.take_off()
            s += 1

        if hi_current > (hi_static + hi_tolerance):
            moving = "DOWN"
            self.move_down_drone()
        elif hi_current < (hi_static - hi_tolerance):
            moving = "UP"
            self.move_up_drone()
        else:
            moving = "STATIC"

        rospy.loginfo(f"HEIGHT: {hi_current}\tZ-ACTION: {moving}")

        cv2.imshow("Front_Cam", cv_image_front)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.signal_shutdown('Quit')
            cv2.destroyAllWindows()

def main():
    rospy.init_node('move_trick')
    move_trick = ImageConverter()

    rospy.Subscriber("/drone/gt_pose", Pose, move_trick.callback2)

    ts = message_filters.ApproximateTimeSynchronizer(
        [move_trick.front, move_trick.down], 10, 0.1
    )
    ts.registerCallback(move_trick.callback)

    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Shutting down")

if __name__ == '__main__':
    main()
