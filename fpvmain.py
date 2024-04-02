import pigpio
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((100, 100))

pi = pigpio.pi()
if not pi.connected:
    exit()

servo_pin = 18  # Existing servo
new_servo_pin = 24  # Additional servo on GPIO pin 24
esc_pin = 23

neutral_pulse_esc = 1500
neutral_pulse_servo = 1500

def control_esc(speed):
    pulse_width = int(((speed + 100) / 200) * (2000 - 1000) + 1000)
    pi.set_servo_pulsewidth(esc_pin, pulse_width)

def set_servo_angle(servo, angle):
    # Function now requires servo pin to specify which servo is being controlled
    pulsewidth = int(((angle + 90) / 180) * (2500 - 500) + 500)
    pi.set_servo_pulsewidth(servo, pulsewidth)

# Initialize both servos to neutral position
set_servo_angle(servo_pin, 0)
set_servo_angle(new_servo_pin, 0)
control_esc(0)  # Initialize ESC to neutral

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                control_esc(13)  # Forward
            elif event.key == pygame.K_s:
                control_esc(-29)  # Reverse, note about speed limit
            elif event.key == pygame.K_a:
                set_servo_angle(servo_pin, -40)  # Left
            elif event.key == pygame.K_d:
                set_servo_angle(servo_pin, 40)  # Right
            elif event.key == pygame.K_z:
                set_servo_angle(new_servo_pin, -70)  # New servo left
            elif event.key == pygame.K_x:
                set_servo_angle(new_servo_pin, 70)  # New servo right
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s]:
                control_esc(0)  # Stop ESC
            elif event.key in [pygame.K_a, pygame.K_d, pygame.K_z, pygame.K_x]:
                set_servo_angle(servo_pin, 0)  # Center the first servo
                set_servo_angle(new_servo_pin, 0)  # Center the new servo

# Cleanup
pi.set_servo_pulsewidth(esc_pin, neutral_pulse_esc)
pi.set_servo_pulsewidth(servo_pin, neutral_pulse_servo)
pi.set_servo_pulsewidth(new_servo_pin, neutral_pulse_servo)  # Ensure new servo is also neutral
pi.stop()
pygame.quit()
