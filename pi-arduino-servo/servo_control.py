#!/usr/bin/env python3
"""Raspberry Pi から Arduino の 9ピンサーボをシリアルで動かす。"""

from __future__ import annotations

import glob
import sys
import time

import serial


BAUD = 115200
DEFAULT_PORTS = (
    "/dev/ttyACM0",
    "/dev/ttyUSB0",
    "/dev/ttyACM1",
    "/dev/ttyUSB1",
)
DEMO_ANGLES = (0, 90, 180, 90)


def find_port() -> str:
    candidates = []
    for pattern in ("/dev/ttyACM*", "/dev/ttyUSB*"):
        candidates.extend(sorted(glob.glob(pattern)))
    for path in DEFAULT_PORTS:
        if path not in candidates:
            candidates.append(path)

    for path in candidates:
        try:
            with serial.Serial(path, BAUD, timeout=0.2):
                return path
        except serial.SerialException:
            continue

    raise SystemExit(
        "Arduino のシリアルポートが見つかりません。USB 接続を確認してください。"
    )


def open_arduino(port: str) -> serial.Serial:
    # Arduino はシリアルオープン時にリセットされることが多いので、READY を待つ。
    ser = serial.Serial(port, BAUD, timeout=1)
    time.sleep(2.0)
    ser.reset_input_buffer()
    return ser


def send(ser: serial.Serial, command: str) -> str:
    ser.write((command.strip() + "\n").encode("ascii"))
    ser.flush()
    reply = ser.readline().decode("ascii", errors="replace").strip()
    if not reply:
        raise SystemExit("Arduino から応答がありません。配線とスケッチを確認してください。")
    return reply


def main() -> None:
    port = find_port()
    print(f"接続: {port} @ {BAUD}")

    with open_arduino(port) as ser:
        for angle in DEMO_ANGLES:
            print(send(ser, str(angle)))
            time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
