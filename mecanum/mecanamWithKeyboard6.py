import sys
from pathlib import Path

import pygame
from gpiozero import Motor

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pi-arduino-servo"))
from servo_control import find_port, open_arduino


"""
GPIOは全て変わる！！！
要注意！！！！！
"""

# ----------------------------
# モーター設定
# ----------------------------

fl = Motor(forward=4, backward=17)
fr = Motor(forward=18, backward=23)
bl = Motor(forward=27, backward=22)
br = Motor(forward=24, backward=25)

ru = Motor(forward=19, backward=26)

# GPIO 26, 21 は使用しない
ps = Motor(forward=13, backward=12)

sl = Motor(forward=5, backward=6)

SPEED = 0.6


# ----------------------------
# モーター停止
# ----------------------------

def stop():
    fl.stop()
    fr.stop()
    bl.stop()
    br.stop()
    ru.stop()
    ps.stop()
    sl.stop()


# ----------------------------
# 移動
# ----------------------------

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


# ----------------------------
# ローラー
# ----------------------------

def roll_up(speed=SPEED):
    ru.forward(speed)


def roll_down(speed=SPEED):
    ru.backward(speed)


# ----------------------------
# プッシャー
# ----------------------------

def push_forward1(speed=SPEED):
    ps.forward(speed)


def push_backward1(speed=SPEED):
    ps.backward(speed)


# ----------------------------
#slide
# ----------------------------

def slide_forward(speed=SPEED):
    sl.forward(speed)

def slide_backward(speed=SPEED):
    sl.backward(speed)

# ----------------------------
# Arduino サーボ
# ----------------------------

def set_arduino_servo(angle):
    if arduino_ser is None:
        return

    arduino_ser.write(f"{angle}\n".encode("ascii"))
    arduino_ser.flush()


# ----------------------------
# pygame 初期化
# ----------------------------

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((400, 120))
pygame.display.set_caption("Robot Controller")

font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()


# ----------------------------
# Arduino 接続
# ----------------------------

arduino_ser = None
arduino_at_90 = False

try:
    arduino_ser = open_arduino(find_port(None))
    set_arduino_servo(0)

except (SystemExit, OSError) as exc:
    print(f"Arduino サーボ未接続: {exc}")
    arduino_ser = None


# ----------------------------
# メイン処理
# ----------------------------

running = True

try:

    while running:

        arduino_command = None

        # ----------------------------
        # イベント処理
        # ----------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # 9キー：Arduinoサーボを0° / 90°切り替え
                if event.key == pygame.K_9:

                    if arduino_at_90:
                        set_arduino_servo(0)
                        arduino_at_90 = False
                        arduino_command = "9: ARDUINO 0"

                    else:
                        set_arduino_servo(90)
                        arduino_at_90 = True
                        arduino_command = "9: ARDUINO 90"


        # ----------------------------
        # キー入力
        # ----------------------------

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
            command = "1 : ROLL UP"

        elif keys[pygame.K_2]:

            roll_down()
            command = "2 : ROLL DOWN"

        elif keys[pygame.K_3]:

            push_forward1()
            command = "3 : PUSH FORWARD"

        elif keys[pygame.K_4]:

            push_backward1()
            command = "4 : PUSH BACKWARD"

        elif keys[pygame.K_5]:

            slide_forward()
            command = "5 : SLIDE FORWARD"

        elif keys[pygame.K_6]:

            slide_backward()
            command = "6 : SLIDE BACKWARD"
        else:

            stop()


        # ----------------------------
        # Arduinoコマンドを優先表示
        # ----------------------------

        if arduino_command:
            command = arduino_command


        # ----------------------------
        # 画面表示
        # ----------------------------

        screen.fill((30, 30, 30))

        text = font.render(
            command,
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 35))

        pygame.display.flip()


        # ----------------------------
        # ESCキー
        # ----------------------------

        if keys[pygame.K_ESCAPE]:
            running = False


        # 最大50FPS
        clock.tick(50)


finally:

    # ----------------------------
    # 終了処理
    # ----------------------------

    stop()

    if arduino_ser is not None:
        arduino_ser.close()

    pygame.quit()
