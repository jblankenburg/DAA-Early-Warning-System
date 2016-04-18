#!/usr/bin/env python
import rospy
import yaml
import rosbag
import message_filters
import sensor_msgs.msg
import geometry_msgs.msg
import ardrone_autonomy.msg
import rosgraph_msgs.msg
import std_msgs.msg
# import data_cleaning.msg


# global stuff to fix later
msg = geometry_msgs.msg.Twist()
count = 0

# fname = open('data_cleaned.txt', 'w')

 # define listener for synchronizing data
def listener(data_file_name, stop_time):
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
    global data_file_name
    global end_time

    # global fname
    # print(nav,msg)
    # print('count!!!!:', count)
    # print('\n\n\n\n\n\n\n\n')
    # count = count + 1

    # get time current time stamp
    time = rospy.get_time()
    # time = nav
    print(time, end_time, end_time - time)

    # if time >= stop_time shut down
    if end_time - time <= 0.4:

    #     # shut down this node?
        rospy.signal_shutdown("DONE!!!") 
        # rospy.shutdown("DONE!!!") 


    # save data to correct format ----- what format is this?!?!?
    data = {'img': img, 'vel':msg, 'nav': nav}
    # print( data['img'],'\n' )
    # print( data['vel'],'\n' )
    # print( data['nav'],'\n','\n','\n' )
    # print('count!!!!:', count)
    # print('\n\n\n\n\n\n\n\n')
    # count = count + 1

    data_file_name.write(str(data['nav']));
    data_file_name.write('\n;\n');
    data_file_name.write(str(data['vel']));
    data_file_name.write('\n;\n');
    data_file_name.write(str(data['img']));
    data_file_name.write('\n;\n');



def callback2(msg_t):
  global msg
  msg = msg_t


# Main
if __name__ == '__main__':

    global data_file_name
    global end_time

    # open bag file 
    bag_file_name = '/home/janelle/Documents/thesis/catkin_ws/src/data_cleaning/rosbag/bad/FlightBackward2.bag'

    # get start time, end time, and duration
    info_dict = yaml.load(rosbag.Bag(bag_file_name, 'r')._get_yaml_info())
    start_time = info_dict['start']
    end_time = info_dict['end']
    duration = info_dict['duration']

    print(start_time, end_time, duration)

    # read in and write data from bag file
    data_file_name = open('data_cleaned.txt', 'w')
    listener(data_file_name, end_time)

    # close file and finish
    print('THIS FINISHED????!!!')
    data_file_name.close()


# 205099-202513 = 2586            bag time      rate
# 929915904-924660834 = 5255070   nsecs clock   rate





#### dont run rosbag play with -i only use -l or not enough storage/time to synch!!!!!