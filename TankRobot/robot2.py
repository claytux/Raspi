import pygame
import RPi.GPIO as GPIO
import os
import time
from datetime import datetime

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode([240, 160])

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins for the DF2301Q module
MOTOR_LEFT_FORWARD = 7
MOTOR_LEFT_BACKWARD = 11
MOTOR_RIGHT_FORWARD = 13
MOTOR_RIGHT_BACKWARD = 15
LED_PIN = 29

# Define GPIO pins for voice recognition commands
VOICE_FORWARD = 31
VOICE_BACKWARD = 33
VOICE_LEFT = 35
VOICE_RIGHT = 37
VOICE_STOP = 32
VOICE_SHUTDOWN = 36
VOICE_START_RECORDING = 38
VOICE_STOP_RECORDING = 40

# Set up GPIO pins
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.setup(VOICE_FORWARD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_BACKWARD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_STOP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_START_RECORDING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(VOICE_STOP_RECORDING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Flash LEDs to indicate the system is ready
for _ in range(4):
    GPIO.output(LED_PIN, False)
    time.sleep(0.5)
    GPIO.output(LED_PIN, True)
    time.sleep(0.5)

# Initialize recording state
record = 0

try:
    while True:
        if GPIO.input(VOICE_SHUTDOWN) == GPIO.HIGH:
            os.system('sudo shutdown now')

        if GPIO.input(VOICE_START_RECORDING) == GPIO.HIGH:
            if record == 0:
                record = 1
                moment = datetime.now()
                GPIO.output(LED_PIN, False)
                camera.start_recording(f'/home/pi/Videos/vid_{moment.hour:02d}_{moment.minute:02d}_{moment.second:02d}.mjpg')

        if GPIO.input(VOICE_STOP_RECORDING) == GPIO.HIGH:
            if record == 1:
                record = 0
                GPIO.output(LED_PIN, True)
                camera.stop_recording()

        if GPIO.input(VOICE_FORWARD) == GPIO.HIGH:
            GPIO.output(MOTOR_LEFT_FORWARD, True)
            GPIO.output(MOTOR_LEFT_BACKWARD, False)
            GPIO.output(MOTOR_RIGHT_FORWARD, True)
            GPIO.output(MOTOR_RIGHT_BACKWARD, False)

        elif GPIO.input(VOICE_BACKWARD) == GPIO.HIGH:
            GPIO.output(MOTOR_LEFT_FORWARD, False)
            GPIO.output(MOTOR_LEFT_BACKWARD, True)
            GPIO.output(MOTOR_RIGHT_FORWARD, False)
            GPIO.output(MOTOR_RIGHT_BACKWARD, True)

        elif GPIO.input(VOICE_LEFT) == GPIO.HIGH:
            GPIO.output(MOTOR_LEFT_FORWARD, False)
            GPIO.output(MOTOR_LEFT_BACKWARD, True)
            GPIO.output(MOTOR_RIGHT_FORWARD, True)
            GPIO.output(MOTOR_RIGHT_BACKWARD, False)

        elif GPIO.input(VOICE_RIGHT) == GPIO.HIGH:
            GPIO.output(MOTOR_LEFT_FORWARD, True)
            GPIO.output(MOTOR_LEFT_BACKWARD, False)
            GPIO.output(MOTOR_RIGHT_FORWARD, False)
            GPIO.output(MOTOR_RIGHT_BACKWARD, True)

        elif GPIO.input(VOICE_STOP) == GPIO.HIGH:
            GPIO.output(MOTOR_LEFT_FORWARD, False)
            GPIO.output(MOTOR_LEFT_BACKWARD, False)
            GPIO.output(MOTOR_RIGHT_FORWARD, False)
            GPIO.output(MOTOR_RIGHT_BACKWARD, False)

        # Ensure all motors are stopped if no voice commands are detected
        time.sleep(0.1)  # Add a small delay to avoid high CPU usage

finally:
    # Clean up GPIO
    GPIO.cleanup()
