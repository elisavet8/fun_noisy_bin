import os
import signal
import sys
import time
import subprocess
import pygame
import random
import RPi.GPIO as GPIO
import asyncio
from time import sleep
import serial_asyncio
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import GFX_OFF, GFX_ON

class Flag:
    "Class Flag contains the flags used in the program to start or terminate a task"
    def __init__(self):
        pass
    arduino_read = True
    sad_eye = False
    happy_eye = False
    full_eye = False
    LED_blink = True
    end_time = False
    got_rubbish = False

class State:
    "Class State contains functions that define the behaviour of the bin at different states of the operation cycle."
    def __init__(self, arduino, speaker, display, flag, button, led):
        "Initialises class State."
        self.arduino = arduino
        self.speaker = speaker
        self.display = display
        self.flag = flag
        self.LED = led
        self.button = button
        for button in Button.button_list:
            button.state = self
        arduino.state = self

    async def end_interaction(self):
        "Define the steps to be taken once the interaction with the bin is over."
        # Display "Thank you" image
        self.LED.stay_OFF()
        if self.flag.got_rubbish == True:
            self.display.load_image('/home/pi/Images/Thank.png')
            # Audio output "Thank you"
            await self.speaker.play_sound('/home/pi/Sounds/thankyou.wav')
            # Send a message to Arduino to check fill level
            await self.arduino.write_serial(b'L\r\n')
            # Display welcome screen
            self.flag.got_rubbish = False
        else:
            self.flag.sad_eye = False
            await self.arduino.write_serial(b'M\r\n')
        self.display.load_image('/home/pi/Images/Hello.png')
        await asyncio.sleep(1)
        #self.button.audio_task2.cancel()
        #print(self.button.audio_task2.cancelled())
        #print("Cancelled")
        #await asyncio.sleep(2)
        #if self.flag.end_time == True:
        #    self.flag.end_time = False
        #    self.button.end_task.cancel()
        #if self.flag.got_rubbish == True:
        #    self.flag.got_rubbish = False
        #    self.button.write_task.cancel()

    async def full(self):
        # Eyes
        self.flag.full_eye = True
        await self.speaker.play_sound('/home/pi/Sounds/unbelievable.wav')

    async def exit_service(self):
        "Stop movement, clean up matrices and GPIO and send a stop message to Arduino. Service is stopped from listen_for_shutdown.service"
        # Stop Movement - Send message to Arduino
#        await write_serial(b'S\r\n')
        # Clear LED Matrices
        LEDMatrix.clear_all()
        # Clear GPIO
        GPIO.cleanup()
        # Shutdown raspberry pi
        sys.exit(0)

    def low_voltage_shutdown(self):
        LEDMatrix.clear_all()
        # Clear GPIO
        GPIO.cleanup()
        command = "/usr/bin/sudo /sbin/shutdown now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

class Arduino:
    def __init__(self, loop, led, button):
        self.LED = led
        self.button = button
        for button in Button.button_list:
            button.arduino = self

    async def read_serial(self, loop):
        reader,writer = await serial_asyncio.open_serial_connection(loop=loop, url='/dev/ttyACM0', baudrate=57600)
        self.reader = reader
        self.writer = writer
        await asyncio.sleep(5)
        await self.write_serial(b'M\r\n')
        print("sent smth")
        #arduino_flag = True
        #self.arduino_flag = arduino_flag
        while True: #Flag.arduino_read:
            print("I'm waiting")
            message = await self.reader.readuntil()
            print("rec smth")
            print(message)
            # Receive a message from Arduino when it stops moving
            if message == b'I\r\n':
                print("This is what I read -->", message)
                #Flag.arduino_read = False
                self.button.button_add_event()
            if message == b'C\r\n':
                print("This is what I read -->", message)
                #Flag.arduino_read = False
                await self.state.end_interaction()
            if message == b'F\r\n':
                print("This is what I read -->", message)
                #Flag.arduino_read = False
                await self.state.full()
            if message == b'R\r\n':
                print("This is what I read -->", message)
                #Flag.arduino_read = False
                Flag.full_eye = False
                await self.write_serial(b'M\r\n')
            if message == b'V\r\n':
                print("This is what I read -->", message)
                #Flag.arduino_read = False
                self.state.low_voltage_shutdown()

    async def write_serial(self, message):
        self.writer.write(message)
        print("I wrote: ", message)
        #Flag.arduino_read  = True
        await asyncio.sleep(2)

class Eye:
    def __init__(self, state, flag):
        self.state = state
        self.flag = flag
        # Initialise library
        LEDMatrix.init()
        # Clear the whole display
        LEDMatrix.clear_all()
        # Reset brightness
        LEDMatrix.brightness(3)

    async def neutral(self):
        while self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
            # Set off all LEDs of the LED Matrices
                LEDMatrix.gfx_set_all(GFX_OFF)
            # Set borders on
                self.set_borders()
            # Set Iris 1 on
                self.set_iris(1)
            # Make the eye with the iris at neutral position appear on the matrices for 2 secs
                LEDMatrix.gfx_render()
                await asyncio.sleep(2)
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
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
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
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
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

            # Set off all the LEDs
            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
                LEDMatrix.gfx_set_all(GFX_OFF)
                await self.set_blink()
                self.set_borders()
                self.set_iris(1)
                # Make the eye appear at neutral position on the matrices
                LEDMatrix.gfx_render()
                await asyncio.sleep(2)
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
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
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

            # Set Iris Position 2 off
            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
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
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

            # Set off all the LEDs
            if self.flag.sad_eye==False and self.flag.happy_eye==False and self.flag.full_eye==False:
                LEDMatrix.gfx_set_all(GFX_OFF)
                await self.set_blink()
            elif self.flag.happy_eye==True:
                await self.happy()
            elif self.flag.sad_eye==True:
                await self.sad()
            else:
                await self.full()

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
        self.flag.happy_eye = False

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
        #await self.set_blink()
        await self.state.end_interaction()


    async def full(self):
        full_x = [24,24,24,24,9,9,9,9,25,25,10,10,26,26,26,26,26,26,26,26,26,11,11,11,11,11,11,11,11,11,27,27,12,12,28,28,28,28,13,13,13,13,29,29,29,29,29,29,29,14,14,14,14,14,14,14,30,30,30,30,30,15,15,15,15,15,31,31,31,31,31,0,0,0,0,0,16,16,16,16,1,1,1,1,17,17,17,17,17,17,17,2,2,2,2,2,2,2,18,18,18,18,18,3,3,3,3,3,20,20,20,20,20,20,20,20,20,5,5,5,5,5,5,5,5,5,21,21,21,6,6,6,22,22,22,22,7,7,7,7]
        full_y = [6,4,10,8,6,4,10,8,5,9,5,9,6,4,1,0,15,14,13,10,8,6,4,1,0,15,14,13,10,8,1,15,1,15,6,4,10,8,6,4,10,8,5,1,0,15,14,13,9,5,1,0,15,14,13,9,6,4,13,10,8,6,4,13,10,8,1,0,15,14,13,1,0,15,14,13,6,4,10,8,6,4,10,8,5,1,0,15,14,13,9,5,1,0,15,14,13,9,6,4,13,10,8,6,4,13,10,8,6,4,1,0,15,14,13,10,8,6,4,1,0,15,14,13,10,8,5,13,9,5,13,9,6,4,10,8,6,4,10,8]

        LEDMatrix.gfx_set_all(GFX_OFF)

        for b in range(0,len(full_x)):
            LEDMatrix.gfx_set_px(full_x[b],full_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()

        for b in range(0,len(full_x)):
            LEDMatrix.gfx_set_px(full_x[b],full_y[b])

        LEDMatrix.gfx_render()
        await asyncio.sleep(3)
        await self.set_blink()


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
    "Class Display handles the screen output. It initialises the screen by using the framebuffer" 
    "Images passed to this class are reshaped and loaded on the screen"
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
        self.load_image('/home/pi/Images/Hello.png')
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def load_image(self, image):
        "Loads the image to the screen"
        self.image = pygame.image.load(image).convert()
        # Reshape the image to fit screen
        self.image = pygame.transform.scale(self.image, (800,480))
        # Create rectangular border
        self.rect = self.image.get_rect()
        # Set the position of the image
        self.rect = self.rect.move((0,0))
        self.screen.blit(self.image, self.rect)
        # Update display
        pygame.display.update()

class Speaker:
    "Class Speaker initialises the speakers."
    "Sound files passed to this class are loaded and output from the speakers"
    def __init__(self):
        "Initialises mixer and plays 'hello'"
        pygame.mixer.init(22050, -16, 2, 4096)
        hello = loop.create_task(self.play_sound('/home/pi/Sounds/hello.wav'))

    async def play_sound(self, audio):
        "Outputs sound from the speakers and tracks when the sound is finished playing."
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
          await asyncio.sleep(0.25)

class Button:
    # Create empty list to store buttons creates
    button_list = []
    #button_flag = True
    #sad_flag = False
    #happy_flag = False
    def __init__(self, flag, display, speaker, button_GPIO, led, image, audio_file):
        "Initialises the button interface"
        # Create instance of classes Speaker, Display and LED
        self.speaker = speaker
        self.display = display
        self.LED = led
        self.button = button_GPIO
        self.image = image
        self.audio_file = audio_file
        self.flag = flag
        for led in LED.led_list:
            led.button = self
        # Set up the button
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Add the button to the list of buttons created
        self.__class__.button_list.append(self)

    def button_add_event(self):
        "Adds event to button GPIOs. Waits until buttons are pressed, calls button_remove_event"
        for button_pin in range(0,len(self.__class__.button_list)):
            GPIO.add_event_detect(self.__class__.button_list[button_pin].button, GPIO.FALLING, callback=self.button_remove_event, bouncetime=300)
            print(self.__class__.button_list[button_pin].button)
        print("event added")
        # *************Instructions - change audio file. Add display for instructions******************
        audio_task = loop.create_task(self.speaker.play_sound('/home/pi/Sounds/who-is-this.wav'))
        self.audio_task = audio_task
        self.flag.LED_blink = True
        blink = loop.create_task(self.LED.blink())
        self.blink = blink
        print("Blink task created")

    def button_remove_event(self, button_pin):
        end_task = None
        write_task = None
        "Removes event from button GPIOs. Sets the button_flag to false and calls look_up function by passing the GPIO of pressed button"
        print("Remove called")
        for index in range(0,len(self.__class__.button_list)):
            GPIO.remove_event_detect(self.__class__.button_list[index].button)
            print("Removing event")
        self.flag.LED_blink = False
        print("Flag set to false", self.flag.LED_blink)
        print(button_pin)
        if button_pin != 4:
            self.blink.cancel()
            print("The blink task is cancelled ",self.blink.cancelled()) 
            self.audio_task.cancel()
            print("The audio task is cancelled ",self.audio_task.cancelled())
            print("switch", button_pin, "on")
            self.look_up(button_pin)
        else:
            print("I'm called from LED blink. I will terminate interaction")
            self.flag.end_time = True
            end_task = loop.create_task(self.state.end_interaction())
            #self.end_task = end_task

    def look_up(self, button_pin):
        "Matches the Button pressed with its LED, image and sound"
        audio_task2 = None
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
        audio_task2 = loop.create_task(self.speaker.play_sound(self.__class__.button_list[index_look_up].audio_file))
        #self.audio_task2 = audio_task2
        #await self.speaker.play_sound(self.__class__.button_list[index_look_up].audio_file)
        if index_look_up != 3:
            msg = b'D\r\n'
            write_task = loop.create_task(self.arduino.write_serial(msg)) # Open door
            self.flag.got_rubbish = True
            #self.write_task = write_task
            #await self.arduino.write_serial(msg)
            self.flag.happy_eye = True
        else:
            self.flag.sad_eye = True

class LED:
    # Creates empty list to store LEDs
    led_list = []
    def __init__(self, LED_GPIO, flag):
        self.LED = LED_GPIO
        self.flag = flag
        # Sets up the LEDs
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LED, GPIO.OUT)
        self.__class__.led_list.append(self)

    # Blinking LEDs until button_flag is set to false by button_remove_event function in Button Class
    async def blink(self):
        print("blink")
        print("flag ", self.flag.LED_blink)
        #print(self.__class__.led_list)
        endTime = time.time() + 30
        print(endTime)
        while(self.flag.LED_blink):
            for led_pin in range(0, len(self.__class__.led_list)):
                print("Here")
                GPIO.output(self.__class__.led_list[led_pin].LED, GPIO.HIGH)
        #        print(self.__class__.led_list[led_pin].LED)
            await asyncio.sleep(1)
            if self.flag.LED_blink:
                for led_pin in range(0, len(self.__class__.led_list)):
                    GPIO.output(self.__class__.led_list[led_pin].LED, GPIO.LOW)
                await asyncio.sleep(1)
            if time.time() >= endTime and self.flag.LED_blink:
                print(time.time())
                #self.flag.LED_blink = False
                self.button.button_remove_event(4)

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

# Catch SIGHUP to avoid stopping the execution of the program on boot
def SIGHUP_handler(signal, frame):
    pass
try:
    signal.signal(signal.SIGHUP, SIGHUP_handler)
except AttributeError:
    # Windows compatibility
    pass

# Pins used for components
LED1_pin = 32
LED2_pin = 36
LED3_pin = 38
LED4_pin = 40
button1_pin = 31
button2_pin = 33
button3_pin = 35
button4_pin = 37

loop = asyncio.get_event_loop()

# Create instance of class Display. Screen initialises and the welcome graphic appears.
display = Display()
flag = Flag()

# Create instance of class Speaker. Initialise the speakers.
speaker = Speaker()
# Create instance of class State. Pass the pin that the power switch is connected to.
# Create instance of class Eye.
# Create instance of class Flag.


# Create instance of class LED. Four LED objects are defined. The GPIO of the LED is passed to the class.
LED1 = LED(LED1_pin, flag)
LED2 = LED(LED2_pin, flag)
LED3 = LED(LED3_pin, flag)
LED4 = LED(LED4_pin, flag)
# Create instance of class Button. Four button objects are defined. The class display and speaker are passed on.
# The GPIO of the button and its respective LED GPIO, along with the picture and audio file correlated to
# the button are passed to the class.
button1 = Button(flag, display, speaker, button1_pin, LED1,'/home/pi/Images/Cans.png', '/home/pi/Sounds/this-is-delicious.wav')
button2 = Button(flag, display, speaker, button2_pin, LED2,'/home/pi/Images/Paper.png', '/home/pi/Sounds/unbelievable.wav')
button3 = Button(flag, display, speaker, button3_pin, LED3,'/home/pi/Images/Plastics.png', '/home/pi/Sounds/woohoo.wav')
button4 = Button(flag, display, speaker, button4_pin, LED4,'/home/pi/Images/Everything_else.png', '/home/pi/Sounds/oops.wav')
# Define asynchronous loop
# Create instance of class Arduino by passing the asynchronous loop and the instances of class LED and Button.
arduino = Arduino(loop, LED2, button2)
state = State(arduino, speaker, display, flag, button2, LED2)
eye = Eye(state, flag)


def exit_service(signal, frame):
    LEDMatrix.clear_all()
    GPIO.cleanup()
    time.sleep(1)
    sys.exit()

# Check for SIGTERM. When SIGTERM is raised the program will exit.
async def interruption_check():
    signal.signal(signal.SIGTERM, exit_service)
    signal.signal(signal.SIGINT, exit_service)
    await asyncio.sleep(1)
# Main function that contains the asynchronous tasks.
async def main(loop):
    asyncio.ensure_future(arduino.read_serial(loop))
    asyncio.ensure_future(eye.neutral())
    asyncio.ensure_future(interruption_check())

# Run asynchronous loop until the program is exited.
loop.run_until_complete(main(loop))
loop.run_forever()
