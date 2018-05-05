import os
import pygame
import random
import RPi.GPIO as GPIO
import asyncio
from time import sleep
import serial_asyncio
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import GFX_OFF, GFX_ON

class Arduino:
    def __init__(self, loop, led, button):
        self.LED = led
        self.button = button

    async def read_serial(self, loop):
        reader,writer = await serial_asyncio.open_serial_connection(loop=loop, url='/dev/ttyUSB0', baudrate=9600)
        self.reader = reader
        self.writer = writer
        arduino_flag = True
        self.arduino_flag = arduino_flag
        while self.arduino_flag:
            if await self.reader.readuntil() == b'Hi from Arduino:\r\n':
                print("This is what I read -->", await self.reader.readuntil())
                self.arduino_flag = False
                self.button.button_add_event()

    def write_serial(self, message):
        self.writer.write(message)

class Eye:
    def __init__(self):
        # Initialise library
        LEDMatrix.init()
        # Clear the whole display
        LEDMatrix.clear_all()
        # Reset brightness
        LEDMatrix.brightness(3)

    async def neutral(self):
        while Button.sad_flag==False and Button.happy_flag==False:
            if Button.sad_flag==False and Button.happy_flag==False:
            # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()
            # Set Iris 1 on
                self.set_iris(1)
            # Make the eye with the iris at neutral position appear on the matrices for 2 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(2)
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

            if Button.sad_flag==False and Button.happy_flag==False:
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
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

            if Button.sad_flag==False and Button.happy_flag==False:
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
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

            # Set off all the LEDs
            if Button.sad_flag==False and Button.happy_flag==False:

                LEDMatrix.gfx_set_all(GFX_OFF)
                await self.set_blink()
                self.set_borders()
                self.set_iris(1)
            # Make the eye appear at neutral position on the matrices
                LEDMatrix.gfx_render()
                await asyncio.sleep(2)
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

            if Button.sad_flag==False and Button.happy_flag==False:
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
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

            # Set Iris Position 2 off
            if Button.sad_flag==False and Button.happy_flag==False:
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
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

            # Set off all the LEDs
            if Button.sad_flag==False and Button.happy_flag==False:
                LEDMatrix.gfx_set_all(GFX_OFF)
                await self.set_blink()
            elif Button.happy_flag==True:
                await self.happy()
            else:
                await self.sad()

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
        Button.happy_flag = False

    async def sad(self):
        sad_x = [29,29,30,30,31,16,16,17,17,14,14,15,15,0,1,1,2,2]
        sad_y = [1,13,0,14,15,0,14,1,13,1,13,0,14,15,0,14,1,13]

        LEDMatrix.gfx_set_all(GFX_OFF)

        self.set_borders()

        for b in range(0,len(sad_x)):
            LEDMatrix.gfx_set_px(sad_x[b],sad_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()

        self.set_borders()
        for b in range(0,len(sad_x)):
            LEDMatrix.gfx_set_px(sad_x[b],sad_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()
        Button.sad_flag = False

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


class Display:
    screen = None;

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        os.putenv('SDL_FBDEV', '/dev/fb0')
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv('SDL_NOMOUSE', '1')

        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break
        if not found:
            raise Exception('No suitable video driver found!')
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Hide mouse cursor
        pygame.mouse.set_visible(False)
        # Initialise font support
        pygame.font.init()
        # Display initial picture
        self.load_image('adapiluv320x240.jpg')
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def load_image(self, image):
        "Loads the image to the screen"
        self.image = pygame.image.load(image).convert()
        # Reshapes the image to fit screen
        self.image = pygame.transform.scale(self.image, (800,480))
        # Creates rectangular border
        self.rect = self.image.get_rect()
        # Sets the position of the image
        self.rect = self.rect.move((0,0))
        self.screen.blit(self.image, self.rect)
        pygame.display.update()

class Speaker:
    def __init__(self):
        pygame.mixer.init(22050, -16, 2, 4096)

    async def play_sound(self, audio):
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
          await asyncio.sleep(0.25)

class Button:
    # Creates empty list to store buttons creates
    button_list = []
    button_flag = True
    sad_flag = False
    happy_flag = False
    def __init__(self, display, speaker, button_GPIO, led, image, audio_file):
        "Initialises the button interface"
        # Creates instance of class Display
        self.display = display
        self.button = button_GPIO
        self.image = image
        self.LED = led
        self.speaker = speaker
        self.audio_file = audio_file
        # Sets up the button
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Add the button to the list of buttons created
        self.__class__.button_list.append(self)

    # Adds event to button GPIOs. Waits until buttons are pressed, calls button_remove_event
    def button_add_event(self):
        for button_pin in range(0,len(self.__class__.button_list)):
            GPIO.add_event_detect(self.__class__.button_list[button_pin].button, GPIO.FALLING, callback=self.button_remove_event, bouncetime=300)
            print(self.__class__.button_list[button_pin].button)
        print("event added")
        audio_task = loop.create_task(self.speaker.play_sound("/home/pi/wonderful.wav"))
        blink = loop.create_task(self.LED.blink())
        self.blink = blink
        self.audio_task = audio_task

    # Removes event from button GPIOs. Sets the button_flag to false and calls look_up function by passing the GPIO of pressed button
    def button_remove_event(self, button_pin):
        for index in range(0,len(self.__class__.button_list)):
            GPIO.remove_event_detect(self.__class__.button_list[index].button)
        self.__class__.button_flag = False
        self.blink.cancel()
        self.audio_task.cancel()
        print("switch", button_pin, "on")
        self.look_up(button_pin)

    # Matches the Button pressed with its LED, image and sound
    def look_up(self, button_pin):
        print(button_pin, "from look up")
        for index_2 in range(0,len(self.__class__.button_list)):
            if button_pin == self.__class__.button_list[index_2].button:
                print(self.__class__.button_list[index_2].image, self.__class__.button_list[index_2].LED)
                index_look_up = index_2
        print("Button pin", button_pin)
        print("Index_", index_look_up)
        self.LED.stay_ON(index_look_up)
        self.display.load_image(self.__class__.button_list[index_look_up].image)
        print(self.__class__.button_list[index_look_up].audio_file)
        audio_task = loop.create_task(self.speaker.play_sound(self.__class__.button_list[index_look_up].audio_file))
        self.__class__.happy_flag = True
		#if index_look_up != 4:
#            self.arduino.write_serial(b"Open door")

class LED:
    # Creates empty list to store LEDs
    led_list = []
    def __init__(self, LED_GPIO):
        self.LED = LED_GPIO
        # Sets up the LEDs
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LED, GPIO.OUT)
        self.__class__.led_list.append(self)

    # Blinking LEDs until button_flag is set to false by button_remove_event function in Button Class
    async def blink(self):
        #print("blink")
        #print(button_flag)
        #print(self.__class__.led_list)
        while(Button.button_flag):
            for led_pin in range(0, len(self.__class__.led_list)):
        #        print("Here")
                GPIO.output(self.__class__.led_list[led_pin].LED, GPIO.HIGH)
        #        print(self.__class__.led_list[led_pin].LED)
            await asyncio.sleep(1)
            if Button.button_flag:
                print(Button.button_flag)
                for led_pin in range(0, len(self.__class__.led_list)):
                    GPIO.output(self.__class__.led_list[led_pin].LED, GPIO.LOW)
                await asyncio.sleep(1)

    def stay_ON(self, index_2):
        print("here")
        for pin in range(0, len(self.__class__.led_list)):
            print(pin)
            if pin==index_2 :
                print("I'm in if ", pin)
                GPIO.output(self.__class__.led_list[pin].LED, GPIO.HIGH)
            else:
                print("I'm in else/", pin)
                GPIO.output(self.__class__.led_list[pin].LED, GPIO.LOW)

    def stay_OFF(self):
        for pin in range(0, len(self.__class__.led_list)):
            GPIO.output(self.__class__.led_list[pin].LED, GPIO.LOW)



#Creates instance of class Display
display = Display()
# Creates instance of class Speaker
speaker = Speaker()
#Creates instance of class Button
LED1 = LED(22)
LED2 = LED(11)

button1 = Button(display, speaker, 16, LED1,'unnamed.jpg', "/home/pi/bourbon.wav")
button2 = Button(display, speaker, 18, LED2,'TEXTXSERVICEX2-800x480.jpg', "/home/pi/piano2.wav")

loop = asyncio.get_event_loop()

arduino = Arduino(loop, LED1, button1)
eye = Eye()

async def main(loop):
    asyncio.ensure_future(arduino.read_serial(loop))
    asyncio.ensure_future(eye.neutral())

loop.run_until_complete(main(loop))
loop.run_forever()
GPIO.cleanup()
