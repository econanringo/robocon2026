#include <Servo.h>

Servo myServo;

void setup() {
  Serial.begin(9600);

  // サーボをD9に接続
  myServo.attach(9);

  // 最初は90度
  myServo.write(90);

  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    int angle = data.toInt();

    // 0～180度に制限
    if (angle >= 0 && angle <= 180) {
      myServo.write(angle);

      Serial.print("ANGLE:");
      Serial.println(angle);
    }
  }
}
