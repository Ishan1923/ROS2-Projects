
#use : docker build -t ros2-base-image .
# then run the docker run command with mounted folder: docker run -it -v $(pwd)/<source directory to mount>:/<destination directory to mount> arm64v8/ros:humble-ros-base


#start from official ROS2 image for arm64 based boards - raspberry pi 3 b+ model
FROM ros:humble-ros-base

#avoid prompts during installation
ENV DEBIAN_FRONTEND = noninteractive

#Install tools
RUN apt update && apt install -y \
build-essential \
python3-pip \
git \
wget \
curl \
ros-dev-tools \
nano \
ssh \

#create a working directory
RUN mkdir -p /ros2_ws/src

#set the woeking directory
WORKDIR /ros2_ws

RUN mkdir -p /.ssh/key/

#use bash as the default shell
CMD ["bash"]
