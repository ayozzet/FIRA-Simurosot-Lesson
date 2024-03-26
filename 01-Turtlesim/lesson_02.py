#!/usr/bin/env python3 

import rospy	
from geometry_msgs.msg import Twist    	


class ControlTurtlesim: 
	def __init__(self): 
		rospy.init_node('ControlTurtlesim', anonymous=False) 
		rospy.on_shutdown(self.shutdown) 
		self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
		rate = rospy.Rate(10);
		move_cmd = Twist() 
		move_cmd.linear.x = 0.3 
		move_cmd.angular.z = 0.3 
		while not rospy.is_shutdown(): 
			self.cmd_vel.publish(move_cmd) 
			rate.sleep() 

	def shutdown(self):
		rospy.loginfo("Stopping Turtlesim")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1) 

if __name__== "__main__": 
    try:
        ControlTurtlesim() 
    except: 
    	rospy.loginfo("End of Node") 