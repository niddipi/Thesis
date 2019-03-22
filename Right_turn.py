import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from drone_status import DroneStatus
from ardrone_autonomy.msg import Navdata

class Drone_movements():
	def __init__(self):
		self.pub_takeoff = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10)
		self.pub_land = rospy.Publisher("ardrone/land", Empty, queue_size=10)
		self.pub_twist = rospy.Publisher("cmd_vel", Twist, queue_size=10)
		self.subNavdata = rospy.Subscriber('/ardrone/navdata',Navdata,self.ReceiveNavdata)
		self.Pitch = 0
		self.Roll = 0
		self.Yaw_velocity = 0 
		self.Z_velocity = 0
		self.rate = rospy.Rate(20)
		self.command = Twist()
		self.status = -1
	def ReceiveNavdata(self,navdata):
		self.status = navdata.state
	def SetCommand(self,roll,pitch,yaw_velocity,z_velocity):
		self.command.linear.x  = pitch
		self.command.linear.y  = roll
		self.command.linear.z  = z_velocity
		self.command.angular.z = yaw_velocity
		return
	
	def move_left(self):
		#self.Yaw_velocity = -1
		self.Yaw_velocity = -0.6
		self.SetCommand(self.Roll, self.Pitch, self.Yaw_velocity, self.Z_velocity)
		self.pub_twist.publish(self.command)
		return
	def move_right(self):
		#self.Yaw_velocity = 1
		self.Yaw_velocity = 0.6
		self.SetCommand(self.Roll, self.Pitch, self.Yaw_velocity, self.Z_velocity)
		self.pub_twist.publish(self.command)
		return
	def move_backward(self):
		#self.Yaw_velocity = 1
		self.Pitch = -0.5
		self.SetCommand(self.Roll, self.Pitch, self.Yaw_velocity, self.Z_velocity)
		self.pub_twist.publish(self.command)
		return
	def move_forward(self):
		#self.Yaw_velocity = 1
		self.Pitch = 0.5
		self.SetCommand(self.Roll, self.Pitch, self.Yaw_velocity, self.Z_velocity)
		self.pub_twist.publish(self.command)
		return
	def hower(self):
		self.SetCommand(0,0,0,0)
		self.pub_twist.publish(self.command)
		return
	def leftright(self):
		Lcount = 0
		Rcount = 0
		Begin = rospy.get_time()
		start_time = rospy.get_time()
		while not rospy.is_shutdown():
			if(self.status == DroneStatus.Landed):
				print("Hit")
				self.pub_takeoff.publish(Empty())
				while rospy.get_time() <= start_time+3.0:
					print(" OK ")
				start_time = rospy.get_time()
			elif rospy.get_time() <= start_time+0.05:
				self.move_forward()
			
			elif rospy.get_time() <= start_time+0.10:
				self.move_left()
				Lcount += 1
			'''
			elif rospy.get_time() <= start_time+0.10:
				self.move_right()
				Lcount += 1
			'''
			if rospy.get_time() > Begin+7.5:
				print(rospy.get_time()) 
				print(Begin+10)
				self.hower()
				self.hower()
				self.pub_land.publish(Empty())
				print("Lcount ",Lcount)
				print("Rcount ",Rcount)
				break
			self.rate.sleep()
				
if __name__=='__main__':
	import sys
	rospy.init_node('ardrone', anonymous=True)
	drone      = Drone_movements()
	drone.leftright()
	rospy.spin()
	sys.exit()
