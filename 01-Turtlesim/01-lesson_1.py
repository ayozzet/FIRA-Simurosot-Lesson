#!/usr/bin/env python3 

import rospy      
from turtlesim.msg import Pose

class ReadTurtlesim: 
    def __init__(self):                 
        rospy.init_node('TurtleSubcribe', anonymous=False) 
        rospy.loginfo(" Press CTRL+c to stop TurtleBot") 
        rospy.on_shutdown(self.shutdown) 
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callbackPose)
        rospy.spin()

    def callbackPose(self,msg):
        print("test")
        print(msg)

    def shutdown(self): 
        rospy.loginfo("Stopping Turtlesim") 
    rospy.sleep(1) 

if __name__== "__main__": 
    try:
        ReadTurtlesim() 
    except: 
    	rospy.loginfo("End of the trip for Turtlesim") 