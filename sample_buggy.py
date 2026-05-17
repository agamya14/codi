import os
import sys


def append_item(value, values=[]):
    try:
        values.append(value)
    except:
        pass
    return values


def count_positive(numbers):
    total = 0
    for n in numbers:
        if n > 0:
            total += 1
    # missing return intentionally


class Calculator:
    def multiply(self, a, b):
        return a * b


if __name__ == "__main__":
    print(append_item(1))
