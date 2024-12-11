#!/usr/bin/env python3
import random

try:
    A = random.randint(-10, 10)

    print(A)

except Exception as e:
    import sys
    print(f"Произошла ошибка: {e}", file=sys.stderr)
