#!/usr/bin/env python3
import random
import sys

try:
    input_value = sys.stdin.read().strip()

    try:
        A = float(input_value)
    except ValueError:
        raise ValueError("Получено некорректное число из stdin.")

    B = random.uniform(-10, 10)

    if B == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")

    result = A / B
    print(result)

except ValueError as ve:
    print(f"Ошибка ввода: {ve}", file=sys.stderr)

except ZeroDivisionError as zde:
    print(f"Ошибка: {zde}", file=sys.stderr)

except Exception as e:
    print(f"Произошла неожиданная ошибка: {e}", file=sys.stderr)
