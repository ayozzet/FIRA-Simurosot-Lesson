#!/usr/bin/env python3

import message_filters
import rospy
from std_msgs.msg import Empty
from sensor_msgs.msg import Image, Range
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import time

class ImageConverter:
    def __init__(self):
        # Initialize the CvBridge and ROS message filters
        self.bridge = CvBridge()
        self.front = message_filters.Subscriber('/drone/front_camera/image_raw', Image)
        self.down = message_filters.Subscriber('/drone/down_camera/image_raw', Image)
        
        # Initialize publishers and control variables
        self._pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
        
        self._move_msg = Twist()
        self.ctrl_c = False
        self.rate = rospy.Rate(10)
        self.sonar_f = 0.0  # Initialize sonar reading
        
        # Tracking variables for takeoff and landing
        self.t = 0
        self.l = 0

    def callback1(self, data1):
        """Sonar data callback to update current sonar reading."""
        self.sonar_f = data1.range  # Store the sonar range value

    def publish_once_in_cmd_vel(self, cmd):
        """Publish a Twist message until it succeeds."""
        while not self.ctrl_c:
            connections = self._pub_cmd_vel.get_num_connections()
            if connections > 0:
                self._pub_cmd_vel.publish(cmd)
                break  # Exit the loop once published
            else:
                self.rate.sleep()

    def stop_drone(self):
        """Stop the drone by setting all velocities to zero."""
        self._move_msg.linear.x = 0.0
        self._move_msg.linear.y = 0.0
        self._move_msg.linear.z = 0.0
        self._move_msg.angular.z = 0.0
        self.publish_once_in_cmd_vel(self._move_msg)

    def take_off(self):
        """Command the drone to take off."""
        self._takeoff_msg = Empty()
        while self.t < 3:
            rospy.loginfo("Taking off...")
            self._pub_takeoff.publish(self._takeoff_msg)
            time.sleep(0.3)
            self.t += 1
        self.stop_drone()

    def landing(self):
        """Command the drone to land."""
        self._land_msg = Empty()
        self.l = 0  # Reset landing counter
        while self.l < 3:
            rospy.loginfo("Landing...")
            self._pub_land.publish(self._land_msg)
            time.sleep(1)
            self.l += 1

    def callback(self, front, down):
        """Callback for synchronized camera images."""
        # Convert the front camera image from ROS Image message to OpenCV format
        cv_image_front = self.bridge.imgmsg_to_cv2(down, "bgr8")
        cv_image_down = self.bridge.imgmsg_to_cv2(front, "bgr8")

        # Display the sonar reading
        son_current = float("{:.2f}".format(self.sonar_f))
        rospy.loginfo(f"SONAR: {son_current}")

        # Show the front camera feed in an OpenCV window
        cv2.imshow("Front_Cam", cv_image_front)
        cv2.imshow("Down_Cam", cv_image_down)

        # Handle the shutdown when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.signal_shutdown('Quit')
            cv2.destroyAllWindows()

def main():
    rospy.init_node('move_trick')  # Initialize the ROS node

    # Create an instance of the ImageConverter class
    move_trick = ImageConverter()

    # Subscribe to the sonar topic
    rospy.Subscriber("/drone/sonar", Range, move_trick.callback1)

    # Synchronize the front and down camera feeds
    ts = message_filters.ApproximateTimeSynchronizer(
        [move_trick.down, move_trick.front], 10, 0.1
    )
    ts.registerCallback(move_trick.callback)

    # Keep the node running until interrupted
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Shutting down")

if __name__ == '__main__':
    main()
