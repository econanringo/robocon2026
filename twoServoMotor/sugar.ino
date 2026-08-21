#include <Servo.h>

// ピンの定義
const int BUTTON_PIN = 2; // ボタンを接続したピン
const int SERVO_PIN  = 9; // サーボを接続したピン

// 角度の定義
const int ANGLE_START  = 0;   // 初期位置（0度） // TODO: 90
const int ANGLE_TARGET = 90;  // 回転後の位置（90度）// TODO: 150

Servo myServo;

bool isMoved = false;      // サーボが90度の位置にあるかどうかのフラグ
int lastButtonState = HIGH; // 前回のボタンの状態（INPUT_PULLUPのため初期値はHIGH）

void setup() {
  // ボタンピンを内部プルアップモードに設定（押すとLOWになる）
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // サーボモーターの設定と初期化
  myServo.attach(SERVO_PIN);
  myServo.write(ANGLE_START); // 最初は0度にセット
}

void loop() {
  // 現在のボタンの状態を取得
  int currentButtonState = digitalRead(BUTTON_PIN);

  // ボタンが「押された瞬間」（HIGHからLOWに変わった瞬間）を検知
  if (lastButtonState == HIGH && currentButtonState == LOW) {
    
    // スイッチのチャタリング（ノイズによる誤動作）防止のための微小待ち
    delay(50); 

    if (isMoved) {
      // 現在90度なら0度に戻す（時計回り）
      myServo.write(ANGLE_START);
      isMoved = false;
    } else {
      // 現在0度なら90度に動かす（反時計回り）
      myServo.write(ANGLE_TARGET);
      isMoved = true;
    }
  }

  // 次回の比較のために現在のボタン状態を記憶
  lastButtonState = currentButtonState;
}
