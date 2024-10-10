#!/usr/bin/python3
from math import sqrt

def main():
    try:
        num = int(input())
        res: float = sqrt(num)

        with open("output.txt", "a") as file:
            file.write(f"{res}\n")

    except ValueError:
        with open("error.txt", "a") as file:
            file.write(traceback.format_exc())

main()
