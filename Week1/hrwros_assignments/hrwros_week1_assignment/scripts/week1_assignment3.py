#! /usr/bin/env python3

# This code has been adapted from the ROS Wiki actionlib tutorials
# to the context of this course.
# (http://wiki.ros.org/hrwros_msgs/Tutorials)

import rospy

import actionlib

from hrwros_msgs.msg import CounterWithDelayAction
from hrwros_msgs.msg import CounterWithDelayFeedback
from hrwros_msgs.msg import CounterWithDelayResult


class CounterWithDelayActionClass(object):
    # Create messages that are used to publish feedback/result
    _feedback = CounterWithDelayFeedback()
    _result = CounterWithDelayResult()

    def __init__(self, name):
        # This will be the name of the action server which clients
        # can use to connect to.
        self._action_name = name

        # Create a simple action server of the newly defined action type and
        # specify the execute callback where the goal will be processed.
        self._as = actionlib.SimpleActionServer(self._action_name,
                                                CounterWithDelayAction,
                                                execute_cb=self.execute_cb,
                                                auto_start=False)

        # Start the action server.
        self._as.start()
        rospy.loginfo("Action server started...")

    def execute_cb(self, goal):
        counter_delay_value = 1.0

        #####################################################################
        #  Assignment 3 - Part3                                             #
        #  modify counter delay using "counter_delay" a private parameter.  #

        if rospy.has_param("~counter_delay"):
            counter_delay_value = rospy.get_param("~counter_delay")
            rospy.loginfo("Parameter found on the parameter server "
                          " Using %.1fs for counter delay." %
                          (counter_delay_value))
        else:
            rospy.loginfo("Parameter not found on the parameter server "
                          "Using default value of 1.0s for counter delay.")

        # End of Assignment 3 - Part3                                       #
        #####################################################################

        # Variable for delay
        # Keep in mind a rate is in units 1/sec or Hz
        # We convert the counter_delay_value from seconds to Hz
        delay_rate = rospy.Rate(1 / counter_delay_value)

        # Variable to decide the final state of the action server.
        success = True

        # publish info to the console for the user
        rospy.loginfo('%s action server is counting up to %i '
                      'with %.1fs delay between each count' %
                      (self._action_name, goal.num_counts,
                       counter_delay_value))

        # Start executing the action
        for counter_idx in range(0, goal.num_counts):
            # Check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
                
            # Publish the feedback
            self._feedback.counts_elapsed = counter_idx
            self._as.publish_feedback(self._feedback)
            # Wait for counter_delay seconds before incrementing the counter.
            # If the rate is 5Hz, this will sleep for 1/5=0.2 seconds.
            delay_rate.sleep()

        if success:
            self._result.result_message = "Successfully counting - Delay is %.1f s" % (counter_delay_value)
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)


if __name__ == '__main__':
    # Initialize a ROS node for this action server.
    rospy.init_node('counter_with_delay')

    # Create an instance of the action server here.
    server = CounterWithDelayActionClass(rospy.get_name())
    rospy.spin()