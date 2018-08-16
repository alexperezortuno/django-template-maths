# -*- coding: utf-8 -*-
import math
import logging
from django import template

try:
    from cdecimal import Decimal
except ImportError:
    from decimal import Decimal, ROUND_DOWN

logger = logging.getLogger(__name__)
register = template.Library()


def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg

    try:
        return int(arg)
    except ValueError:
        if ',' in arg:
            arg = arg.replace(',', '.')

        return float(arg)
    except Exception as e:
        logger.exception("Is not valid Number: {0}".format(e))


def handle_numbers(number, number_op):
    number = valid_numeric(number)
    number_op = valid_numeric(number_op)

    if type(number) != type(number_op):
        logger.warning('Unsafe operation: {0} {1}.'.format(number, number_op))

    return Decimal(number), Decimal(number_op)


@register.filter(name='add', is_safe=True)
def add(number=None, arg=None):
    """
    Adds values on either side of the operator
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_add = handle_numbers(number, arg)

        return number + number_add
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='sub', is_safe=True)
def sub(number=None, arg=None):
    """
    Subtracts right hand operand from left hand operand
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_sub = handle_numbers(number, arg)

        return number - number_sub
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='div', is_safe=True)
def div(number=None, arg=None):
    """
    Divides left hand operand by right hand operand
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_division = handle_numbers(number, arg)

        return number / number_division
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='mul', is_safe=True)
def mul(number=None, arg=None):
    """
    Multiplies values on either side of the operator
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_multiply = handle_numbers(number, arg)

        return number * number_multiply
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='mod', is_safe=True)
def mod(number=None, arg=None):
    """
    Divides left hand operand by right hand operand and returns remainder
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_modulus = handle_numbers(number, arg)

        return number % number_modulus
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='exp', is_safe=True)
def exp(number=None, arg=None):
    """
    Performs exponential (power) calculation on operators
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_exponent = handle_numbers(number, arg)

        return number ** number_exponent
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='flr', is_safe=True)
def flr(number=None, arg=None):
    """
    Floor Division - The division of operands where the result is the quotient in which the digits
    after the decimal point are removed. But if one of the operands is negative, the result is
    floored, i.e., rounded away from zero (towards negative infinity)
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number, number_exponent = handle_numbers(number, arg)

        return number // number_exponent
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='sqr', is_safe=True)
def sqr(number=None):
    """
    Divides left hand operand by right hand operand
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        number = valid_numeric(number)

        return math.sqrt(number)
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='add_decimal', is_safe=True)
def add_decimal(number=None, arg=None):
    """
    Add decimals to number
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        decimal_places = Decimal(10) ** -arg

        if isinstance(number, (float, int, str)):
            number = Decimal(number)

        return number.quantize(decimal_places)
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='remove_decimal', is_safe=True)
def remove_decimal(number=None):
    """
    Add decimals to number
    :param number:
    :return number|string:
    """

    try:
        if isinstance(number, (Decimal, float, int, str)):
            return str(number).split('.')[0]

    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='separator', is_safe=True)
def separator(number=None, arg=None):
    """
    Format number with commas or dots
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        if isinstance(number, (Decimal, float)):
            number = "{:,}".format(number)

        if arg == 'comma':
            if ',' in number:
                return number
            else:
                return "{:,}".format(int(number))
        elif arg == 'dot':
            if ',' in number:
                number, decimal = number.split('.')
                return '{0},{1}'.format(number.replace(',', '.'), decimal)
            else:
                return "{:,}".format(int(number)).replace(',', '.')
        else:
            return 'NaN'
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
        return 'NaN'


@register.filter(name='percent_of_number', is_safe=True)
def percent_of_number(number_one=None, number_two=None):
    """
    Calculate the percent of a given number
    :param number:
    :param arg:
    :return number|string:
    """
    try:
        return float(number_one) / float(number_two) * 100
    except Exception as e:
        logger.error('Error operation: {error}.'.format(error=e))
    return 'NaN'
