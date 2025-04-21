#!/usr/bin/env bash

echo -e "Starting up innference_ros container \n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo -e "This container will access to the users home directory and log in as the user with their password and x sever access.\nYou will not own the workspace though, use sudo chown -R $USER /dev_ws"
echo -e "Source the workspace with source devel/setup.bash"

IP=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')

docker run -it --privileged \
    --user=$(id -u $USER):$(id -g $USER) \
    --group-add sudo \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --add-host=$(hostname)=$IP \
    --workdir="/dev_ws" \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/dev:/dev" \
    --net=host \
    --cap-add=sys_nice \
    gridworld_agent:latest
