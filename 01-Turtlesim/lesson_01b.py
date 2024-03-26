#!/usr/bin/env python3

import rospy 
from turtlesim.msg import Color, Pose 

class ReadTurtlesim:
    def __init__(self):
        rospy.init_node('Penyu', anonymous=False) 
        rospy.on_shutdown(self.shutdown)
        self.color_sub = rospy.Subscriber('/turtle1/color_sensor', Color, self.callbackColor)
        self.pose_sub = rospy.Subscriber('/turtle1/pose', Pose, self.callbackPose)
        rospy.spin()
    
    def callbackColor(self, data1):
        print("------------")
        print(data1)
    
    def callbackPose(self, data2):
        print("------------")
        print(data2)
    
    def shutdown(self):
        rospy.loginfo("Stopping..")
    
    rospy.sleep(1)

if __name__ == "__main__":
    try:
        ReadTurtlesim()
    except:
        rospy.loginfo("END of node")