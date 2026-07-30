from gpiozero import Motor
from time import sleep

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


if __name__ == "__main__":
    try:
        move_forward(0.6)
        sleep(2)
        slide_right(0.6)
        sleep(2)
        stop()
    finally:
        stop()
