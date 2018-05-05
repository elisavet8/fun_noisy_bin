
import time
import math
from random import randrange

# Import library
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import DISSOLVE, GFX_ON, GFX_OFF, GFX_INVERT

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

#try:
	# Clear the whole display and reset brightness
LEDMatrix.clear_all()
LEDMatrix.brightness(3)
while True:
	LEDMatrix.gfx_set_all(GFX_OFF)

	LEDMatrix.gfx_set_col(24)
	LEDMatrix.gfx_set_col(25)
	LEDMatrix.gfx_set_col(21)
	LEDMatrix.gfx_set_col(22)
	LEDMatrix.gfx_set_col(9)
	LEDMatrix.gfx_set_col(10)
	LEDMatrix.gfx_set_col(6)
	LEDMatrix.gfx_set_col(7)

	# Eye borders
	x_coord_off = [24,24,24,24,24,25,25,25,21,21,21,22,22,22,22,22,9,9,9,9,9,10,10,10,6,6,6,7,7,7,7,7]
	y_coord_off = [7,6,5,9,8,7,6,8,7,6,8,7,6,5,9,8,7,6,5,9,8,7,6,8,7,6,8,7,6,5,9,8]

	x_coord_on = [26,26,26,26,27,27,27,27,28,28,28,28,29,29,29,29,30,30,30,30,31,31,31,31,16,16,16,16,17,17,17,17,18,18,18,18,19,19,19,19,20,20,20,20,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,15,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5] 
	y_coord_on =[6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,] 

	# Set off the corners of the eye (previously set on by the columns)
	for i in range(0,len(x_coord_off)):
		LEDMatrix.gfx_set_px(x_coord_off[i],y_coord_off[i])

	for a in range(0,len(x_coord_on)):
		LEDMatrix.gfx_set_px(x_coord_on[a],y_coord_on[a])

	# Iris Position 1
	iris_1_x = [29,29,29,29,30,30,30,30,31,31,31,31,16,16,16,16,17,17,17,17,14,14,14,14,15,15,15,15,0,0,0,0,1,1,1,1,2,2,2,2]
	iris_1_y = [1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,]

	# Iris Position 2
	iris_2_x = [27,27,27,27,28,28,28,28,29,29,29,29,30,30,30,30,31,31,31,31,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,15,0,0,0,0] 
	iris_2_y = [3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0]

	# Iris Position 3
	iris_3_x = [31,31,31,31,16,16,16,16,17,17,17,17,18,18,18,18,19,19,19,19,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
	iris_3_y = [15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12,15,14,13,12]

	# Iris Position 4
	iris_4_x = iris_2_x
	iris_4_y = iris_1_y

	# Iris Position 5
	iris_5_x = iris_3_x
	iris_5_y = iris_1_y
	# Set Iris 1 ON
	for b in range(0,len(iris_1_x)):
		LEDMatrix.gfx_set_px(iris_1_x[b],iris_1_y[b])

	LEDMatrix.gfx_render()
	time.sleep(1)

	# Set Iris 1 OFF
	for b in range(0,len(iris_1_x)):
		LEDMatrix.gfx_set_px(iris_1_x[b],iris_1_y[b])

	# Set Iris 2 ON
	for b in range(0,len(iris_5_x)):
		LEDMatrix.gfx_set_px(iris_5_x[b],iris_5_y[b])

	LEDMatrix.gfx_render()



	time.sleep(1)

	# Set Iris 1 OFF
	for b in range(0,len(iris_5_x)):
		LEDMatrix.gfx_set_px(iris_5_x[b],iris_5_y[b])

	# Set Iris 2 ON
	for b in range(0,len(iris_4_x)):
		LEDMatrix.gfx_set_px(iris_4_x[b],iris_4_y[b])


	LEDMatrix.gfx_render()
	time.sleep(1)



	LEDMatrix.gfx_set_all(GFX_OFF)

#	x_close_on = [24,25,25,26,26,27,27,28,28,29,29,30,30,31,31,16,16,17,17,18,18,19,19,20,20,21,21,22,9,10,10,11,11,12,12,13,13,14,14,15,15,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7] 
#	y_close_on = [10,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,10,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10,9,10] 

	x_close_on = [24,25,25,26,26,27,27,28,28,29,29,30,30,31,31,16,16,17,17,18,18,19,19,20,20,21,21,22,9,10,10,11,11,12,12,13,13,14,14,15,15,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7] 
	y_close_on = [0,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,0,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0] 

	for b in range(0,len(x_close_on)):
		LEDMatrix.gfx_set_px(x_close_on[b],y_close_on[b])

	LEDMatrix.gfx_render()
	time.sleep(0.12)

	for b in range(0,len(x_close_on)):
		LEDMatrix.gfx_set_px(x_close_on[b],y_close_on[b])

	LEDMatrix.gfx_set_col(24)
	LEDMatrix.gfx_set_col(25)
	LEDMatrix.gfx_set_col(21)
	LEDMatrix.gfx_set_col(22)
	LEDMatrix.gfx_set_col(9)
	LEDMatrix.gfx_set_col(10)
	LEDMatrix.gfx_set_col(6)
	LEDMatrix.gfx_set_col(7)

	# Set off the corners of the eye (previously set on by the columns)
	for i in range(0,len(x_coord_off)):
		LEDMatrix.gfx_set_px(x_coord_off[i],y_coord_off[i])

	for a in range(0,len(x_coord_on)):
		LEDMatrix.gfx_set_px(x_coord_on[a],y_coord_on[a])

	# Set Iris 1 ON
	for b in range(0,len(iris_1_x)):
		LEDMatrix.gfx_set_px(iris_1_x[b],iris_1_y[b])

	LEDMatrix.gfx_render()
	time.sleep(1)

	for b in range(0,len(iris_1_x)):
		LEDMatrix.gfx_set_px(iris_1_x[b],iris_1_y[b])


	happy_x = [28,28,28,29,29,29,29,29,30,30,30,30,30,30,31,31,31,31,31,31,16,16,16,16,16,16,17,17,17,17,17,18,18,18,13,13,13,14,14,14,14,14,15,15,15,15,15,15,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3]
	happy_y = [1,0,15,2,1,0,15,14,2,1,0,15,14,13,1,0,15,14,13,12,2,1,0,15,14,13,2,1,0,15,14,1,0,15,1,0,15,2,1,0,15,14,2,1,0,15,14,13,1,0,15,14,13,12,2,1,0,15,14,13,2,1,0,15,14,1,0,15]

	for b in range(0,len(happy_x)):
		LEDMatrix.gfx_set_px(happy_x[b],happy_y[b])

	LEDMatrix.gfx_render()
	time.sleep(3)
	# Continuous marquee display
#	LEDMatrix.clear_all()

#except KeyboardInterrupt:
    # reset array
#    LEDMatrix.scroll_message_horiz(["","Goodbye!",""], 1, 8)
