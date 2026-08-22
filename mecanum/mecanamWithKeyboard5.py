import sys
from pathlib import Path

import pygame
from gpiozero import Motor, Servo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pi-arduino-servo"))
from servo_control import find_port, open_arduino

"""
GPIOは全て変わる！！！
要注意！！！！！
"""

fl = Motor(forward=17, backward=18)
fr = Motor(forward=22, backward=23)
bl = Motor(forward=24, backward=25)
br = Motor(forward=5, backward=6)
ru = Motor(forward=19, backward=16)
# ps = Motor(forward=26, backward=21) ... GPIOピンが悪くてできないかった。あとでこのピンについて調べてみよう！
ps = Motor(forward=13, backward=12)
ph = Motor(forward=20, backward=4)
servo = Servo(pin=13, initial_value=0)

SPEED = 0.6


def stop():
    fl.stop()
    fr.stop()
    bl.stop()
    br.stop()
    ru.stop()
    ps.stop()
    ph.stop()


def move_forward(speed=SPEED):
    fl.forward(speed)
    fr.forward(speed)
    bl.forward(speed)
    br.forward(speed)


def move_backward(speed=SPEED):
    fl.backward(speed)
    fr.backward(speed)
    bl.backward(speed)
    br.backward(speed)


def slide_right(speed=SPEED):
    fl.forward(speed)
    fr.backward(speed)
    bl.backward(speed)
    br.forward(speed)


def slide_left(speed=SPEED):
    fl.backward(speed)
    fr.forward(speed)
    bl.forward(speed)
    br.backward(speed)


def rotate_cw(speed=SPEED):
    fl.backward(speed)
    fr.forward(speed)
    bl.backward(speed)
    br.forward(speed)


def rotate_ccw(speed=SPEED):
    fl.forward(speed)
    fr.backward(speed)
    bl.forward(speed)
    br.backward(speed)
    
def roll_up(speed=SPEED):
    ru.forward(speed)
    
def roll_down(speed=SPEED):
    ru.backward(speed)
    
def push_forward1(speed=SPEED):
    ps.forward(speed)

def push_backward1(speed=SPEED):
    ps.backward(speed)
    
def push_forward2(speed=SPEED):
    ph.forward(speed)

def push_backward2(speed=SPEED):
    ph.backward(speed)

def open_servo():
    servo.value = 30

def close_servo():
    servo.value = 0


def set_arduino_servo(angle):
    if arduino_ser is None:
        return
    arduino_ser.write(f"{angle}\n".encode("ascii"))
    arduino_ser.flush()

# ----------------------------
# pygame初期化
# ----------------------------
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((400, 120))
pygame.display.set_caption("Robot Controller")

font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

arduino_ser = None
arduino_at_90 = False
try:
    arduino_ser = open_arduino(find_port(None))
    set_arduino_servo(0)
except (SystemExit, OSError) as exc:
    print(f"Arduino サーボ未接続: {exc}")
    arduino_ser = None

try:
    running = True

    while running:
        arduino_command = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                if arduino_at_90:
                    set_arduino_servo(0)
                    arduino_at_90 = False
                    arduino_command = "9: ARDUINO 0"
                else:
                    set_arduino_servo(90)
                    arduino_at_90 = True
                    arduino_command = "9: ARDUINO 90"

        keys = pygame.key.get_pressed()

        command = "STOP"

        if keys[pygame.K_w]:
            move_forward()
            command = "W : FORWARD"

        elif keys[pygame.K_s]:
            move_backward()
            command = "S : BACKWARD"

        elif keys[pygame.K_a]:
            slide_left()
            command = "A : LEFT"

        elif keys[pygame.K_d]:
            slide_right()
            command = "D : RIGHT"

        elif keys[pygame.K_q]:
            rotate_ccw()
            command = "Q : ROTATE LEFT"

        elif keys[pygame.K_e]:
            rotate_cw()
            command = "E : ROTATE RIGHT"
            
        elif keys[pygame.K_1]:
            roll_up()
            command = "1: ROLL UP"
        elif keys[pygame.K_2]:
            roll_down()
            command = "2: ROLL DOWN"
        elif keys[pygame.K_3]:
            push_forward1()
            command = "3: PUSH FORWARD"
        elif keys[pygame.K_4]:
            push_backward1()
            command = "4: PUSH BACKWARD"
        elif keys[pygame.K_5]:
            push_forward2()
            command = "5: PUSH FORWARD2"
        elif keys[pygame.K_6]:
            push_backward2()
            command = "6: PUSH BACKWARD2"
        elif keys[pygame.K_7]:
            open_servo()
            command = "7: OPEN SERVO"
        elif keys[pygame.K_8]:
            close_servo()
            command = "8: CLOSE SERVO"

        else:
            stop()

        if arduino_command:
            command = arduino_command

        screen.fill((30, 30, 30))

        text = font.render(command, True, (255, 255, 255))
        screen.blit(text, (20, 35))

        pygame.display.flip()

        if keys[pygame.K_ESCAPE]:
            running = False

        clock.tick(50)

finally:
    stop()
    if arduino_ser is not None:
        arduino_ser.close()
    pygame.quit()
