#!/usr/bin/python3
from random import randint

def main():
    try:
        a = int(input())
        b = randint(-10, 10)

        res = a / b
        print(res)

    except (ZeroDivisionError, ValueError) as exception:
        with open("error.txt", "a") as file:
            file.write(exception)

    main()