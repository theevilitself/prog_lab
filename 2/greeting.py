#!/usr/bin/env python3
import sys

def name_check(name):
    if not name[0].isupper():
        raise ValueError(f"Name '{name}' needs to start in uppercase!")

    if not name.isalpha():
        invalid_chars = [sym for sym in name if not sym.isalpha()]
        raise ValueError(f"Name '{name}' contains invalid characters: {', '.join(invalid_chars)}")

def greet_user(name):
    print(f"Nice to see you, {name}!")


def main():
    input_method = sys.stdin if not sys.stdin.isatty() else None

    def process_input(name):
        try:
            name_check(name.strip())
            greet_user(name.strip())
        except ValueError as e:
            sys.stderr.write(f"Error: {e}\n")

    if input_method:
        for name in input_method:
            process_input(name)
    else:
        try:
            while True:
                name = input("Hey, what's your name?\n")
                process_input(name)
        except KeyboardInterrupt:
            print("\nGoodbye!")

main()
