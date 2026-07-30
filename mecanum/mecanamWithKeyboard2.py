import pygame
from gpiozero import Motor

fl = Motor(forward=17, backward=18)
fr = Motor(forward=22, backward=23)
bl = Motor(forward=24, backward=25)
br = Motor(forward=5, backward=6)

font = pygame.font.SysFont(None, 48)

SPEED = 0.6

def stop():
    fl.stop()
    fr.stop()
    bl.stop()
    br.stop()

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

pygame.init()

# キー入力を受け取るための小さなウィンドウ
screen = pygame.display.set_mode((300, 100))
pygame.display.set_caption("Robot Controller")

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

        else:
            stop()

        # 画面更新
        screen.fill((30, 30, 30))
        text = font.render(command, True, (255, 255, 255))
        screen.blit(text, (20, 25))
        pygame.display.flip()

        if keys[pygame.K_ESCAPE]:
            running = False

        clock.tick(50)

finally:
    stop()
    pygame.quit()