from gpiozero import AngularServo
import pygame
import sys

# Initialize servo on GPIO 17 with standard pulse widths (500-2500us)
servo = AngularServo(17, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)

# Initialize Pygame and set up a small dummy window to capture key events
pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("Servo Control")

# Start servo at middle position (90 degrees)
current_angle = 90
servo.angle = current_angle

print("Use Left/Right arrow keys to move servo. Close window to exit.")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_angle = max(0, current_angle - 10)  # Decrease angle by 10
                servo.angle = current_angle
                print(f"Angle: {current_angle}")
                
            elif event.key == pygame.K_RIGHT:
                current_angle = min(180, current_angle + 10) # Increase angle by 10
                servo.angle = current_angle
                print(f"Angle: {current_angle}")
