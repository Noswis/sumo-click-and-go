from sumopy.interface import SumoController
from constants import *
import math
import sys
import time
from PIL import Image
import numpy as np
import StringIO

# transform screen coordinates to local coordinates relative to the sumo
def screen_to_local(pixel_x, pixel_y):
	return (pixel_x - IMAGE_WIDTH / 2, IMAGE_HEIGHT - pixel_y)

# calculate the distance in the y axis
def distance_y(pixels):
	d = (1.0 / (float(pixels * A1) + B1)) * C1 + D1
	return 1.0 / d

# calculate the distance in the x axis
def distance_x(pixels_x, pixels_y):
	# There is no D since we want the asymptote to be the x axis
	pixels_per_cm = (1.0 / (float(pixels_y * A2) + B2)) * C2
	return pixels_x / pixels_per_cm

# this should roughly give the correct distance
def get_distance(speed, time):
	return (speed * DISTANCE_CONSTANT) * time + speed * STOP_CONSTANT

# a rewrite of the above formula
def get_duration(speed, distance):
	return float(distance - (speed * STOP_CONSTANT)) / float(speed * DISTANCE_CONSTANT)

# calculate the turnspeed
def get_turnspeed(angle_per_sec):
	return BASIC_TURNSPEED * angle_per_sec

# take a picture from the sumo
def picture(controller):
	
	# TODO this is the problem
	controller.store_pic()
	pic = controller.get_pic()
	
	
	
	#convert pic to Image
	pilImage = Image.open(StringIO.StringIO(pic));
	
		
	# convert to numpy matrix
	npImage = np.array(pilImage)
	return npImage

# angle in radians
def slow_turn(controller, angle, chain=False):
	turn_speed = SLOW_TURN
	duration = TURN_CONSTANT_A *abs(angle) + TURN_CONSTANT_B

	# if a move command is issued after a turn, chain has to be on.
	# if not, the sumo will turn less than the specfied angle
	if chain:
		duration += TURN_CONSTANT_B*-1
		
	if duration < DURATION_THRESHHOLD:
		print "WARNING: Angle is too small, sumo will not turn"
		return
	
	if angle < 0:
		turn_speed *= -1
	
	controller.move(0, turn_speed, duration)

def move_to_point(controller, delta_x, delta_y, drive_speed, verbose=False):
	# the total angle we need to turn
	angle = math.atan(float(delta_x) / float(delta_y))
			
	distance = math.sqrt(delta_y**2 + delta_x**2)
	drive_duration = get_duration(drive_speed, distance)	

	slow_turn(controller, angle, chain=True)
	print "Starting to Drive"
	controller.move(drive_speed, 0, drive_duration)
	
if __name__ == "__main__":
  #turn(controller, math.pi/2.0, 20)
  #move_to_point(50, 540, 20)
  controller = SumoController()
  #angle = math.pi/4.0
  #slow_turn(controller, math.pi/15.0)
  move_to_point(controller, 100, 100, 20)



# 4,  0.2 = 15
# 4,  0.55 = 22.5
# 4 , 1.6 = 45
# 4 , 3.6 = 90
# 4 , 7.8 = 180

#115
#173

