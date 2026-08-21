#include <Servo.h>

const int SERVO_PIN = 9;
const int ANGLE_START  = 0 /* 90 */
const int ANGLE_TARGET = 150;

Servo myServo;
bool isMoved = false;

void setup() {
  Serial.begin(9600);
  myServo.attach(SERVO_PIN);
  myServo.write(ANGLE_START);
  
  // 起動確認用メッセージ
  Serial.println("--- Ready! Type 'b' and press Enter ---");
}

void loop() {
  if (Serial.available() > 0) {
    char key = Serial.read();

    // 改行文字（Enterキーのノイズ）以外を画面に表示して確認
    if (key != '\n' && key != '\r') {
      Serial.print("Input Key: ");
      Serial.println(key);
    }

    if (key == 'b' || key == 'B') {
      if (isMoved) {
        myServo.write(ANGLE_START);
        isMoved = false;
        Serial.println("-> Servo: 0 deg");
      } else {
        myServo.write(ANGLE_TARGET);
        isMoved = true;
        Serial.println("-> Servo: 150 deg");
      }
    }
  }
}
