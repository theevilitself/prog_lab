#!/usr/bin/env python3
import math
import sys

try:
    input_value = sys.stdin.read().strip()

    input_value = input_value.replace(',', '.')

    try:
        number = float(input_value)
    except ValueError:
        raise ValueError("Получено некорректное число из stdin.")

    if number < 0:
        raise ValueError("Невозможно вычислить корень из отрицательного числа.")

    root = math.sqrt(number)

    print(root)

except ValueError as ve:
    print(f"Ошибка: {ve}", file=sys.stderr)
    sys.exit()

except Exception as e:
    print(f"Произошла неожиданная ошибка: {e}", file=sys.stderr)
    sys.exit()
