import keyboard
from time import sleep
from gpiozero import Motor

fl = Motor(forward=17, backward=18)
fr = Motor(forward=22, backward=23)
bl = Motor(forward=24, backward=25)
br = Motor(forward=5, backward=6)


def stop():
    fl.stop()
    fr.stop()
    bl.stop()
    br.stop()


def move_forward(speed=0.5):
    fl.forward(speed)
    fr.forward(speed)
    bl.forward(speed)
    br.forward(speed)


def move_backward(speed=0.5):
    fl.backward(speed)
    fr.backward(speed)
    bl.backward(speed)
    br.backward(speed)


def slide_right(speed=0.5):
    fl.forward(speed)
    fr.backward(speed)
    bl.backward(speed)
    br.forward(speed)


def slide_left(speed=0.5):
    fl.backward(speed)
    fr.forward(speed)
    bl.forward(speed)
    br.backward(speed)


def rotate_cw(speed=0.5):
    fl.backward(speed)
    fr.forward(speed)
    bl.backward(speed)
    br.forward(speed)


def rotate_ccw(speed=0.5):
    fl.forward(speed)
    fr.backward(speed)
    bl.forward(speed)
    br.backward(speed)

while True:
    if keyboard.is_pressed('w'):
        move_forward(SPEED)

    elif keyboard.is_pressed('s'):
        move_backward(SPEED)

    elif keyboard.is_pressed('a'):
        slide_left(SPEED)

    elif keyboard.is_pressed('d'):
        slide_right(SPEED)

    elif keyboard.is_pressed('q'):
        rotate_ccw(SPEED)

    elif keyboard.is_pressed('e'):
        rotate_cw(SPEED)

    else:
        stop()

    if keyboard.is_pressed('esc'):
        break

    sleep(0.02)

stop()