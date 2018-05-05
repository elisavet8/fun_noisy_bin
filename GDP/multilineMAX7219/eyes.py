
import time
import math
from random import randrange
import asyncio
# Import library
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import GFX_ON, GFX_OFF

class Eye:
    global flag
    def __init__(self):
        # Initialise library
        LEDMatrix.init()
        # Clear the whole display
        LEDMatrix.clear_all()
        # Reset brightness
        LEDMatrix.brightness(3)

    async def neutral(self):
        while Hi.flag:
            if Hi.flag:
            # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()
            # Set Iris 1 on
                self.set_iris(1)
            # Make the eye with the iris at neutral position appear on the matrices for 2 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(2)
            else:
                await self.happy()

            if Hi.flag:
  # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()

            # Set Iris Position 1 off
#                self.set_iris(1)
            # Set Iris Position 2 on
                self.set_iris(2)
            # Make the eye with the iris at left position appear on the matrices for 1 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(1)
            else:
                await self.happy()

            if Hi.flag:
  # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()
            # Set Iris Position 2 off
#                self.set_iris(2)
            # Set Iris Position 1 on
                self.set_iris(1)
            # Make the eye with the iris at neutral position appear on the matrices for 1 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(1)
            else:
                await self.happy()

            # Set off all the LEDs
            if Hi.flag:

                LEDMatrix.gfx_set_all(GFX_OFF)
                await self.set_blink()
                self.set_borders()
                self.set_iris(1)
            # Make the eye appear at neutral position on the matrices
                LEDMatrix.gfx_render()
                await asyncio.sleep(2)
            else:
                await self.happy()

            if Hi.flag:
  # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()
            # Set Iris Position 1 off
#                self.set_iris(1)
            # Set Iris Position 2 on
                self.set_iris(3)
            # Make the eye with the iris at left position appear on the matrices for 1 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(1)
            else:
                await self.happy()

            # Set Iris Position 2 off
            if Hi.flag:
  # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()
#                self.set_iris(3)
            # Set Iris Position 1 on
                self.set_iris(1)
            # Make the eye with the iris at neutral position appear on the matrices for 1 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(1)
            else:
                await self.happy()

            # Set off all the LEDs
            if Hi.flag:
                LEDMatrix.gfx_set_all(GFX_OFF)
                await self.set_blink()
            else:
                await self.happy()

    async def happy(self):
        happy_x = [28,28,28,29,29,29,29,29,30,30,30,30,30,30,31,31,31,31,31,31,16,16,16,16,16,16,17,17,17,17,17,18,18,18,13,13,13,14,14,14,14,14,15,15,15,15,15,15,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3]
        happy_y = [1,0,15,2,1,0,15,14,2,1,0,15,14,13,1,0,15,14,13,12,2,1,0,15,14,13,2,1,0,15,14,1,0,15,1,0,15,2,1,0,15,14,2,1,0,15,14,13,1,0,15,14,13,12,2,1,0,15,14,13,2,1,0,15,14,1,0,15]

        LEDMatrix.gfx_set_all(GFX_OFF)

        self.set_borders()

        for b in range(0,len(happy_x)):
            LEDMatrix.gfx_set_px(happy_x[b],happy_y[b])


        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()


        self.set_borders()
        for b in range(0,len(happy_x)):
            LEDMatrix.gfx_set_px(happy_x[b],happy_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()
        Hi.flag = True

    async def sad(self):
        sad_x = [29,29,30,30,31,16,16,17,17,14,14,15,15,0,1,1,2,2]
        sad_y = [1,13,0,14,15,0,14,1,13,1,13,0,14,15,0,14,1,13]

        for b in range(0,len(sad_x)):
            LEDMatrix.gfx_set_px(sad_x[b],sad_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()

        for b in range(0,len(sad_x)):
            LEDMatrix.gfx_set_px(sad_x[b],sad_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()
        self.neutral()

    def set_borders(self):
        # Create a list with the column numbers that create the borders of the eyes
        borders_col = [24, 25, 21, 22, 9, 10, 6, 7]
        # Create a list with the x and y coordinates of the LEDs needed to be set off
        # (previously set on by the columns) to create the corners of the borders of the eyes
        x_corners_off = [24,24,24,24,24,25,25,25,21,21,21,22,22,22,22,22,9,9,9,9,9,10,10,10,6,6,6,7,7,7,7,7]
        y_corners_off = [7,6,5,9,8,7,6,8,7,6,8,7,6,5,9,8,7,6,5,9,8,7,6,8,7,6,8,7,6,5,9,8]
        # Create a list with the x and y coordinates of the LEDs needed to complete the borders of the eyes 
        x_borders_on = [26,26,26,26,27,27,27,27,28,28,28,28,29,29,29,29,30,30,30,30,31,31,31,31,16,16,16,16,17,17,17,17,18,18,18,18,19,19,19,19,20,20,20,20,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,15,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5] 
        y_borders_on =[6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,6,5,10,9,] 

        # Set on the columns of the list borders_col
        for column in borders_col:
            LEDMatrix.gfx_set_col(column)
        # Set off the corners of the eye (previously set on by the columns)
        for b in range(0,len(x_corners_off)):
            LEDMatrix.gfx_set_px(x_corners_off[b],y_corners_off[b])
        # Set the rest of the LEDs that create the borders on
        for b in range(0,len(x_borders_on)):
            LEDMatrix.gfx_set_px(x_borders_on[b],y_borders_on[b])

    def set_iris(self, position):
        # Iris Position 1 - Neutral Position
        iris_1_x = [29,29,29,29,30,30,30,30,31,31,31,31,16,16,16,16,17,17,17,17,14,14,14,14,15,15,15,15,0,0,0,0,1,1,1,1,2,2,2,2]
        iris_1_y = [1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,1,0,15,14,]
        # Iris Position 2 - Iris positioned left
        iris_2_x = [27,27,27,27,28,28,28,28,29,29,29,29,30,30,30,30,31,31,31,31,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,15,0,0,0,0] 
        iris_2_y = iris_1_y
        # Iris Position 3 - Iris positioned right
        iris_3_x = [31,31,31,31,16,16,16,16,17,17,17,17,18,18,18,18,19,19,19,19,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
        iris_3_y = iris_1_y

        # Set Iris Position 1 on
        if position == 1:
            for b in range(0,len(iris_1_x)):
                LEDMatrix.gfx_set_px(iris_1_x[b],iris_1_y[b])
        elif position == 2:
            for b in range(0,len(iris_2_x)):
                LEDMatrix.gfx_set_px(iris_2_x[b],iris_2_y[b])
        else:
            for b in range(0,len(iris_3_x)):
                LEDMatrix.gfx_set_px(iris_3_x[b],iris_3_y[b])

    async def set_blink(self):
        # Create a list with the x and y coordinates of the eye when it blinks
        x_blink_on = [24,25,25,26,26,27,27,28,28,29,29,30,30,31,31,16,16,17,17,18,18,19,19,20,20,21,21,22,9,10,10,11,11,12,12,13,13,14,14,15,15,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7] 
        y_blink_on = [0,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,0,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0,15,0] 

        LEDMatrix.gfx_set_all(GFX_OFF)
        # Set the LEDs on for blinking position of the eye
        for b in range(0,len(x_blink_on)):
            LEDMatrix.gfx_set_px(x_blink_on[b],y_blink_on[b])

        # Make the eye blinking appear on the matrices for 0.12 secs
        LEDMatrix.gfx_render()
        await asyncio.sleep(0.12)

        # Set the blinking off
        for b in range(0,len(x_blink_on)):
            LEDMatrix.gfx_set_px(x_blink_on[b],y_blink_on[b])





class Hi:
    flag = True
    def __init__(self):
        pass
    async def print_letter(self):
        while True:
            print("blink")
            self.__class__.flag = False
            await asyncio.sleep(5)

loop = asyncio.get_event_loop()
eyes = Eye()
hello = Hi()



async def main(loop):
    asyncio.ensure_future(eyes.neutral())
    asyncio.ensure_future(hello.print_letter())
loop.run_until_complete(main(loop))
loop.run_forever()

