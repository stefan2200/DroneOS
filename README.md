# DroneOS
A python application for controlling a quadcopter using a Raspberry PI

This application uses 4 electronic speed controllers (ESCs), a Raspberry PI and the mpu6050 accelerometer for hovering.

After some PID finetuning the drone manages to stabilize mid air but there is still a lot to be done :)
The purpose of this application is mainly the development on a drone built from scratch with no expensive controller boards etc. (poor student :) )

Currently runs on a counter which means it does 100 run iterations before landing.

The top of body.py contains the setup for the ESC pins on your raspberry, this uses software PWM to control the motors using the pigpio binary.
Do not test this with a live drone it it may crash :)

This system requires the following commands to be run:
pip install mpu6050
sudo apt-get install pigpio

Also make sure your i2c is enabled before running, getting invalid data from the gyro may force all motors to go at full acceleration (happened to me :( )
