/*
 * Raspberry Pi からシリアルで角度を受け取り、9ピンのサーボを動かす。
 *
 * 配線:
 *   サーボ信号線 -> Arduino D9
 *   サーボ GND   -> Arduino GND（電源のGNDとも共通にする）
 *   サーボ VCC   -> 5V電源（SG90ならArduino 5Vでも可。大きなサーボは別電源）
 *
 * ラズパイとは USB ケーブルでつなぐ（シリアルは USB 経由）。
 *
 * 受信フォーマット（改行終わり）:
 *   90          -> 90度へ
 *   a:45        -> 45度へ
 *   center      -> 90度
 *   sweep       -> 0-180 を往復
 */

#include <Servo.h>

const int SERVO_PIN = 9;
const int BAUD = 115200;
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

Servo servo;
int currentAngle = 90;
String line;

void setup() {
  Serial.begin(BAUD);
  servo.attach(SERVO_PIN);
  servo.write(currentAngle);
  delay(300);
  Serial.println("READY pin=9");
}

void setAngle(int angle) {
  if (angle < MIN_ANGLE) angle = MIN_ANGLE;
  if (angle > MAX_ANGLE) angle = MAX_ANGLE;
  currentAngle = angle;
  servo.write(currentAngle);
  Serial.print("OK ");
  Serial.println(currentAngle);
}

void sweep() {
  Serial.println("SWEEP start");
  for (int a = 0; a <= 180; a += 2) {
    servo.write(a);
    delay(15);
  }
  for (int a = 180; a >= 0; a -= 2) {
    servo.write(a);
    delay(15);
  }
  currentAngle = 0;
  Serial.println("SWEEP done");
}

void handleLine(String cmd) {
  cmd.trim();
  cmd.toLowerCase();
  if (cmd.length() == 0) {
    return;
  }

  if (cmd == "center") {
    setAngle(90);
    return;
  }
  if (cmd == "sweep") {
    sweep();
    return;
  }
  if (cmd.startsWith("a:")) {
    cmd = cmd.substring(2);
  }

  int angle = cmd.toInt();
  if (cmd == "0" || angle > 0) {
    setAngle(angle);
    return;
  }

  Serial.print("ERR unknown: ");
  Serial.println(cmd);
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (line.length() > 0) {
        handleLine(line);
        line = "";
      }
    } else {
      line += c;
      if (line.length() > 32) {
        line = "";
        Serial.println("ERR too long");
      }
    }
  }
}
