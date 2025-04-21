cmake_minimum_required(VERSION 3.0.2)
project(gridworld_agent)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  turtlesim
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs geometry_msgs turtlesim
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/node_01.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
