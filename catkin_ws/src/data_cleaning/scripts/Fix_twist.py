#!/usr/bin/env python
import rospy
import message_filters
import sensor_msgs.msg
import geometry_msgs.msg
import ardrone_autonomy.msg
import rosgraph_msgs.msg
import std_msgs.msg

# since twist has no time, wrap twist into new msg with time stamp and twist
def fix_twist():

  # subscribe to twist
  rospy.init_node('twist_listener')
  t = rospy.Subscriber('/cmd_vel',geometry_msgs.msg.Twist)
  c = rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock)
  callback_pub(t,c)
  rospy.spin()


def callback_pub(time, twist):

  twist_data = twist
  time_header = time

  h = std_msgs.msg.Header()
  # h.stamp = time_header 
  h.stamp = rospy.get_rostime() 

# h = std_msgs.msg.Header()
# h.stamp = rospy.Time.now() # Note you need to call rospy.init_node() before this will work 
    
  # republish twist with time header
  pub = rospy.Publisher('/new_twist', std_msgs.msg.Header, queue_size=10)
  pub = rospy.Publisher('/new_twist', data_cleaning.msg.Fix_twist, queue_size=10)

  # rospy.init_node('new_twist_node')
  r = rospy.Rate(10) # 10 Hz, will need to change!!!!
  while not rospy.is_shutdown():
      pub.publish(h)
      # pub.publish(twist_data)
      r.sleep()


#  MainS
if __name__ == '__main__':
    fix_twist()
