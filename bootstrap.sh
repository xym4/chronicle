#!/bin/bash

sudo yum install python3 -y
sudo yum install git -y
sudo amazon-linux-extras install docker -y
sudo usermod -a -G docker ec2-user
service docker start