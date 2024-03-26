#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from geometry_msgs.msg import Twist

bridge = CvBridge()
twist = Twist()

class AV:   
      
    def image_callback(msg):
        try:
            cmd_vel_pub = rospy.Publisher('/catvehicle/cmd_vel_safe',Twist, queue_size=1)
            image = bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
        except CvBridgeError as e:
            print(e)        
        
def main():
    rospy.init_node('AV_node', anonymous=True)
    image_sub = rospy.Subscriber('/catvehicle/camera_front/image_raw_front',Image, AV.image_callback)
    rospy.spin()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
