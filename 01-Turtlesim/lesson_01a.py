#!/usr/bin/env python3

import rospy 
from turtlesim.msg import Color 

class ReadTurtlesim:
    def __init__(self):
        rospy.init_node('Penyu', anonymous=False) 
        rospy.on_shutdown(self.shutdown)
        self.pose_sub = rospy.Subscriber('/turtle1/color_sensor', Color, self.callbackColor)
        rospy.spin()
    
    def callbackColor(self, data):
        print("------------")
        print(data)
    
    def shutdown(self):
        rospy.loginfo("Stopping..")
    
    rospy.sleep(1)

if __name__ == "__main__":
    try:
        ReadTurtlesim()
    except:
        rospy.loginfo("END of node")