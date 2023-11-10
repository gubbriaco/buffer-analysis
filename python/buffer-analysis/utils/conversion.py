from enum import Enum


class Order(Enum):
    FEMTO = 1
    PICO = 2
    MICRO = 3


def get_order(number):
    if number == 0:
        return 0

    order = 0
    while abs(number) >= 10:
        number /= 10
        order += 1
    while abs(number) < 1:
        number *= 10
        order -= 1

    return order


def to_order(old_number, new_order_instance):
    if old_number == 0:
        raise ValueError("Number is equal to zero.")

    new_order = 0
    if new_order_instance == Order.FEMTO:
        new_order = -15
    elif new_order_instance == Order.PICO:
        new_order = -12
    elif new_order_instance == Order.MICRO:
        new_order = -6

    old_order = get_order(old_number)

    scale_order = 0
    if old_order < 0 and new_order < 0:
        scale_order = abs(old_order) + new_order
    elif old_order < 0 and new_order > 0:
        scale_order = abs(old_order) + abs(new_order)
    elif old_order > 0 and new_order < 0:
        scale_order = -(abs(old_order) + abs(new_order))
    elif old_order > 0 and new_order > 0:
        scale_order = abs(new_order) - old_order

    scale_factor = 10 ** (scale_order)

    new_number = old_number * scale_factor

    new_number_str = str(new_number)
    new_number_str = new_number_str[:-4]
    new_number = float(new_number_str) / scale_factor
    return new_number
