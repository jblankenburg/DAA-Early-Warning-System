#!/usr/bin/env python
import rospy
import message_filters
import sensor_msgs.msg
import geometry_msgs.msg
import ardrone_autonomy.msg
import rosgraph_msgs.msg
import std_msgs.msg
import data_cleaning.msg


# global stuff to fix later
msg = geometry_msgs.msg.Twist()
count = 0

fname = open('data_cleaned.txt', 'w')

 # define listener for synchronizing data
def listener():
    rospy.init_node('cleaner')
    sub =[]
    sub.append(message_filters.Subscriber('/ardrone/image_raw', sensor_msgs.msg.Image))
    t = rospy.Subscriber('/cmd_vel',geometry_msgs.msg.Twist,callback2)
    sub.append(message_filters.Subscriber('/ardrone/navdata', ardrone_autonomy.msg.Navdata))
    ts = message_filters.ApproximateTimeSynchronizer(sub,5000,0.1)
    ts.registerCallback(callback)
    rospy.spin()


#  callback for listener
def callback(img,nav):
    global count
    global msg
    global fname
    # print(nav,msg)
    # print('count!!!!:', count)
    # print('\n\n\n\n\n\n\n\n')
    # count = count + 1

    # save data to correct format ----- what format is this?!?!?
    data = {'img': img, 'vel':msg, 'nav': nav}
    # print( data['img'],'\n' )
    # print( data['vel'],'\n' )
    # print( data['nav'],'\n','\n','\n' )
    # print('count!!!!:', count)
    # print('\n\n\n\n\n\n\n\n')
    # count = count + 1

    fname.write(str(data['nav']));
    fname.write('\n;\n');
    fname.write(str(data['vel']));
    fname.write('\n;\n');
    fname.write(str(data['img']));
    fname.write('\n;\n');



def callback2(msg_t):
  global msg
  msg = msg_t


# Main
if __name__ == '__main__':
    listener()
    print('THIS FINISHED????!!!')
    fname.close()


# 205099-202513 = 2586            bag time      rate
# 929915904-924660834 = 5255070   nsecs clock   rate





#### dont run rosbag play with -i only use -l or not enough storage/time to synch!!!!!