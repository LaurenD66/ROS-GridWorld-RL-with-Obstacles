ARG ROS_DISTRO=noetic

FROM ros:$ROS_DISTRO-ros-base

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Install essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ssh \
    git \
    curl \
    wget \
    build-essential \
    cmake \
    python3-pip \
    python3-flake8 \
    terminator \
    pkg-config \
    python3-catkin-tools \
    python3-rosdep \
    python3-rosinstall-generator \
    iputils-ping \
    ros-$ROS_DISTRO-rqt \
    ros-$ROS_DISTRO-rqt-common-plugins \
    ros-$ROS_DISTRO-rqt-robot-plugins \
    ros-$ROS_DISTRO-roslint \
    ros-$ROS_DISTRO-rqt-gui \
    ros-$ROS_DISTRO-rqt-gui-py \
    ros-$ROS_DISTRO-rqt-py-common \
    ros-$ROS_DISTRO-rviz \
    ros-$ROS_DISTRO-ecl-threads \
    ros-$ROS_DISTRO-ecl-geometry \
    ros-$ROS_DISTRO-ecl-streams \
    ros-$ROS_DISTRO-diagnostics \
    ros-$ROS_DISTRO-turtlesim \
    ros-$ROS_DISTRO-ros-tutorials \
    ros-$ROS_DISTRO-rospy \
    xvfb \
    python3-opengl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && pip3 install --no-cache-dir \
    argcomplete \
    flake8-blind-except \
    flake8-builtins \
    flake8-comprehensions \
    flake8-deprecated \
    flake8-return \
    flake8-length \
    flake8-todo \
    flake8-quotes \
    black \
    importlib-metadata \
    setuptools \
    requests \
    ws4py \
    numpy==1.22.0 \
    opencv-python \
    pygame \
    pyquaternion \
    pyyaml \
    pytransform3d \
    pyvirtualdisplay \
    gymnasium \
    pygame \
    matplotlib \
    tqdm

# Setup workspace
RUN mkdir -p /dev_ws/src
COPY . /dev_ws/src/
WORKDIR /dev_ws

RUN /bin/bash -c "source /opt/ros/$ROS_DISTRO/setup.bash && \
    catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    catkin build"

RUN cp /dev_ws/src/.docker/entrypoint.sh /entrypoint.sh && chmod +x /entrypoint.sh
RUN cp /dev_ws/src/.docker/setup.bash /dev_ws/setup.bash && chmod +x /dev_ws/setup.bash

ENTRYPOINT ["bash", "/entrypoint.sh"]
CMD ["bash"]

