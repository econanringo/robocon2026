import pygame
from gpiozero import Motor

fl = Motor(forward=17, backward=18)
fr = Motor(forward=22, backward=23)
bl = Motor(forward=24, backward=25)
br = Motor(forward=5, backward=6)
ru = Motor(forward=19, backward=16)
# ps = Motor(forward=26, backward=21) ... GPIOピンが悪くてできないかった。あとでこのピンについて調べてみよう！
ps = Motor(forward=13, backward=12)
ph = Motor(forward=20, backward=4)


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

# ----------------------------
# pygame初期化
# ----------------------------
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((400, 120))
pygame.display.set_caption("Robot Controller")

font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

try:
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        else:
            stop()

        screen.fill((30, 30, 30))

        text = font.render(command, True, (255, 255, 255))
        screen.blit(text, (20, 35))

        pygame.display.flip()

        if keys[pygame.K_ESCAPE]:
            running = False

        clock.tick(50)

finally:
    stop()
    pygame.quit()
