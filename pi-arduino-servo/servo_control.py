#!/usr/bin/env python3
"""Raspberry Pi から Arduino の 9ピンサーボをシリアルで動かす。"""

from __future__ import annotations

import argparse
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


def find_port(preferred: str | None) -> str:
    if preferred:
        return preferred

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
        "Arduino のシリアルポートが見つかりません。"
        " USB 接続を確認するか --port /dev/ttyACM0 を指定してください。"
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
    parser = argparse.ArgumentParser(
        description="Arduino D9 のサーボをシリアルで動かす"
    )
    parser.add_argument(
        "angle",
        nargs="?",
        help="0-180 の角度。省略すると対話モード。center / sweep も可",
    )
    parser.add_argument("--port", help="例: /dev/ttyACM0")
    args = parser.parse_args()

    port = find_port(args.port)
    print(f"接続: {port} @ {BAUD}")

    with open_arduino(port) as ser:
        if args.angle is not None:
            print(send(ser, args.angle))
            return

        print("角度を入力 (0-180 / center / sweep)。終了は q")
        while True:
            try:
                command = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not command or command.lower() in {"q", "quit", "exit"}:
                break
            try:
                print(send(ser, command))
            except SystemExit as exc:
                print(exc)


if __name__ == "__main__":
    sys.exit(main())
