#include<Servo.h>  // Library for servo motor communication
#include<Wire.h>   // Library for I2C communication with slave Arduino

Servo doorServoTop;          // Create servo object to control top door servo
Servo doorServoBottom;       // Create servo object to control bottom door servo

// Voltage monitoring
const float referenceVoltage = 4.74;                  // Arduino voltage in V (reading connecting multimeter to Aref - GND)
const float R1 = 10000;                               // Resistor 1 value in Ohms for voltage divider
const float R2 = 2000;                                // Resistor 2 value in Ohms for voltage divider
const float resistorFactor = 1023.0*(R2/(R1+R2));
const int batteryPin = 1;                             // Centre pin of voltage divider connected to A1
const float voltageThreshold = 5.0;                   // Battery voltage in V that trigers a signal to be sent to Raspi

//Standing mode switch
const int buttonPin = 10;                              // Switch to set robot to "Standing mode" connected to pin 10
int buttonState = 0;                                   // Flag for the state of the switch

// Obstacle Detection - Define a list with the ultrasonic sensors' pins
const int sensorCount_obstacle = 2;                    // Number of obstacle sensors
const int trigPins_obstacle[] = {4,6};                 // Trigger pins of ultrasonic sensor
const int echoPins_obstacle[] = {5,7};                 // Echo pins of ultrasonic sensor
int obstacle_count[] = {0,0};                          // Initialise distance measured

// Fill Level Monitoring - Ultrasonic sensor pins
const int sensorCount_fill = 1;                        // Number of fill sensors
const int trigPin_fill = 2;                            // Trigger pin of ultrasonic sensor 
const int echoPin_fill = 3;                            // Echo pin of ultrasonic sensor

// Door Sensor - Light Dependent Resistor (LDR)
const int lightPin = 0;                                // LDR connected to A0
const int min_light = 900;                             // Minimum wavelength of light expected (nm)
const int buzzerPin = 11;                             // Buzzer pin

// Door Servo motors
const int doorServoTop_pin = 8;                        // Top servo connected to pin 8                         
const int doorServoBottom_pin = 9;                     // Bottom servo connected to pin 9
int pos = 11;                                          // Initialise servo position counter

// Flags
boolean Stopped = true;       // Flag to check when motors are off
boolean CheckFill = false;    // Flag to check if the fill level needs to be checked
char message;                 // Variable to store message from Raspi

// Function prototypes
void voltage_read();
void obstacle_check();
void fillLevel_check();
void serial_read();
void ultrasonic_sensor(int, int, int&);
void open_door();


void setup() {
  Wire.begin();                                     // Join I2C bus
  Serial.begin(57600);                              // Initiate serial communication at 57600 bps
  
  // Set the trigPin as an output and echoPin as an input for ultrasonic sensors used for obstacle avoidance
  for (int Pin_o = 0; Pin_o < sensorCount_obstacle; Pin_o++) {
    pinMode(trigPins_obstacle[Pin_o], OUTPUT);
    pinMode(echoPins_obstacle[Pin_o], INPUT);
  }
  
  // Set the trigPin as an output and echoPin as an input for ultrasonic sensors used for fill level monitoring
  pinMode(trigPin_fill, OUTPUT);
  pinMode(echoPin_fill, INPUT);

  // Door servo motors
  doorServoTop.attach(doorServoTop_pin);           // Attach the top servo to pin 7 
  doorServoBottom.attach(doorServoBottom_pin);     // Attach the bottom servo to pin 8
  doorServoTop.write(11);                          // Send top servo to position 11                  
  doorServoBottom.write(170);                      // Send bottom servo to position 170
  
  pinMode(buttonPin, INPUT_PULLUP);                // Configure pi 10 of standing mode switch as an input and enable the internal pull-up resistor

  pinMode(buzzerPin, OUTPUT);
}  
 
void loop() {
  if (Serial.available() > 0) {                    // Check for incoming serial data
    buttonState = digitalRead(buttonPin);          // Check if standing mode button is on
    voltage_read();                                // Check battery voltage
    message = Serial.read();                       // Read the oldest byte in the serial buffer
    Serial.println(message);                       // Print message received
    
    if (message == 'M') {                          // Start moving from Raspberry Pi
      obstacle_check();                            // Check for obstacle
      while (Stopped == false) {                   // While no obstacle is detected
        if (buttonState == HIGH) {                 // If the button is not pressed send a message to the motor arduino
          Wire.beginTransmission(4);               // Transmit to device #4
          Wire.write('M');                         // Send M - move to motor arduino
          Wire.endTransmission();                  // Stop tramsitting
          delay(100);
        }
        obstacle_check();                          // Keep checking for obstacle
        voltage_read();                            // Keep checking voltage
      }
      
      if (buttonState == HIGH) {                   // If the button is not pressed send a message to the motor arduino
        Wire.beginTransmission(4);                 // Transmit to device #4
        Wire.write('S');                           // Send S - stop moving to motor arduino
        Wire.endTransmission();
        delay(100);
      }   
    
    delay(1000);
    
    Serial.println('I');                           // Start Interaction to Raspberry Pi
    }
    
    else if (message == 'D') {                     // Open door from Raspberry Pi
      open_door();
      delay(100);
    }
    
    else if (message == 'L') {                     // Check Fill level from Rapsberry Pi
      fillLevel_check();
      delay(100);  
    }
    
    else if (message == 'S') {                     // Stop motor
      if (buttonState == HIGH) {                   // If the button is not pressed send a message to the motor arduino
        Wire.beginTransmission(4);                 // Transmit to device #4
        Wire.write('S');                           // Send S - stop moving to motor arduino
        Wire.endTransmission();                      // Stop tramsitting
      }
      delay(100);
    }
  }
}

void voltage_read() {
/*Check battery voltage and send a message to Raspi if less than 5.0V*/  
  int sensorValue = analogRead(batteryPin);                           // Read the input on analog pin 0
  float voltage = sensorValue * (referenceVoltage / resistorFactor);  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V): 
  if (voltage < voltageThreshold) {                                   // Check if voltage has dropped
    Stopped = true;                                                   // Set Stopped flag to true
    Serial.println('V');                                              // Send a message to Raspberry Pi for Low Voltage
  }
  Serial.println(voltage);
}

void obstacle_check() {
/*Read ultrasonic sensor input and check if a person is approaching*/
  long duration[2];
  int distance[2];
  int max_distance;
  for (int Pin= 0; Pin < sensorCount_obstacle; Pin++) {
    ultrasonic_sensor(Pin, Pin, distance[Pin]);                       // Call ultrasonic sensor
    if (buttonState == HIGH) {
      max_distance = 200;                                             // Maximum distance at which sensor triggers when robot is in moving mode
    }
    else {
      max_distance = 100;                                             // Maximum distance at which sensor triggers when robot is in standing mode
    }  
    if (distance[Pin] <= max_distance || distance[Pin] >= 500) {      // Check the distance range
      obstacle_count[Pin] += 1;                                       // Increment the counter of obtacles measured
    }
    delay(60);
    if (obstacle_count[0] >= 1 && obstacle_count[1] >= 1) {           // If counter of obstacles measured is more than 1 for both sensors
      Stopped = true;                                                 // Set Stopped flag to true
      break;                                                          // Exit the function
    }
  }
} 

void fillLevel_check() {
/*Read ultrasonic sensor input and check if the bin is full*/
  int distance;
  ultrasonic_sensor(trigPin_fill, echoPin_fill, distance);
  if (distance < -1 || distance > 350) {                              // Check Fill Level
    Serial.println('F');                                              // Send F - full to Rapsberry Pi
    Serial.println(distance);
  }
  else {
    Serial.println('R');                                              // Send R - Ready to go to Rapsberry Pi
    Serial.println(distance);
  }
}


void open_door() {
/*Open and close the door of the bin*/
  int pos = 0;                                 // Variable to store the servo position

  // Opening the door
  doorServoTop.write(170);                     // Tell top servo to go to position 170
  doorServoBottom.write(11);                   // Tell bottom servo to go to position 11
  delay(15);
  
  delay(10000);                                // Wait for 10 secs
  
  Serial.println('C');                         // Send C - closing door to Raspberry Pi
  
  for (pos = 170; pos >= 11; pos -= 1) {       // Slowly closing the door while checking for hand interruption
    while (analogRead(lightPin) < min_light) {
      analogWrite(buzzerPin, 170);             // Turn on buzzer
      if (analogRead(lightPin) > min_light) {  // If light is interrupted stop the door from closing
        analogWrite(buzzerPin, 0);             // Turn off buzzer
        break;
      }
    }
    
    doorServoTop.write(pos);              
    doorServoBottom.write(181 - pos);
    delay(15);                                // Wait 15ms for the servos to reach the position
  }
}


void ultrasonic_sensor(int trigPin, int echoPin, int& distance) {
/*Read distance from ultrasonic sensor*/
  digitalWrite(trigPin, LOW);                 // Clear the trigger Pin
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);                // Set the trigPin on HIGH state for 10 micro seconds
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);     // Read the echoPin, return the sound wave travel time in microseconds
  distance = duration*0.034/2;                // Calculate distance
}


