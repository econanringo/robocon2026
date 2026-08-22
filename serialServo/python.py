import serial
import time

# Arduinoに接続
arduino = serial.Serial(
    "/dev/ttyACM0",
    9600,
    timeout=1
)

# USBシリアル接続時、Arduinoがリセットされることがある
time.sleep(2)

def move_servo(angle):
    if 0 <= angle <= 180:
        arduino.write(f"{angle}\n".encode())

        response = arduino.readline().decode().strip()
        print(response)


try:
    while True:
        angle = int(input("角度(0～180): "))

        if 0 <= angle <= 180:
            move_servo(angle)
        else:
            print("0～180の範囲で入力してください")

except KeyboardInterrupt:
    print("\n終了")

finally:
    arduino.close()
