
#use : docker build -t ros2-base-image .
# then run the docker run command with mounted folder: docker run -it -v $(pwd)/<source directory to mount>:/<destination directory to mount> arm64v8/ros:humble-ros-base


#start from official ROS2 image for arm64 based boards - raspberry pi 3 b+ model
FROM ros:humble-ros-base

#avoid prompts during installation
ENV UBUNTU_FRONTEND = noninteractive

#Install tools
RUN apt update && apt install -y \
build-essential \
python3.12 \
python3-pip \
nano \
ssh \
git \
wget \
curl \
ros-dev-tools \
ssh \

#create a working directory
RUN mkdir -p src

#set the woeking directory
WORKDIR /ros2_ws/

#use bash as the default shell
CMD ["bash"]
