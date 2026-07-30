#include <Servo.h>

Servo myservo1; // 1つ目のサーボモーター
Servo myservo2; // 2つ目のサーボモーターを追加

int pos = 0;

const int buttonPin = 2;
int buttonState = 0;
int lastButtonState = HIGH; // 前回のボタン状態を保存（初期値はHIGH）
bool isOpen = false; 

void setup() {
  myservo1.attach(9);  // 1つ目のサーボを9番ピンに接続
  myservo2.attach(10); // 2つ目のサーボを10番ピンに接続
  pinMode(buttonPin, INPUT_PULLUP); 
}

void loop() {
  buttonState = digitalRead(buttonPin);

  // 前回がHIGH（離されている）で、今回がLOW（押されている）の時だけ実行
  if (buttonState == LOW && lastButtonState == HIGH) { 
    delay(50); // チャタリング対策

    // 50ミリ秒待った後もまだ押されていたら、間違いなく押されたと判断
    if (digitalRead(buttonPin) == LOW) {
      isOpen = !isOpen;
    }
  }

  // 今回のボタンの状態を「前回の状態」として記録しておく
  lastButtonState = buttonState; 

  // 開閉状態に応じて2つのサーボを同時に動作させる
  if (isOpen) {
    myservo1.write(90); // 1つ目のサーボを90度に
    myservo2.write(90); // 2つ目のサーボも90度に
  } else {
    myservo1.write(0);  // 1つ目のサーボを0度に
    myservo2.write(0);  // 2つ目のサーボも0度に
  }
}