"""
Adapted from 'Python in Practice by Mark Summerfield'
Chapter 2: Structural Design Patterns - Decorator, validate


"""

import re
import numbers


# Adapted from 'Python in Practice by Mark Summerfield'
# Chapter 2: Structural Design Patterns - Decorator, validate
class Ensure:

    def __init__(self, validate, doc=None):
        self.validate = validate
        self.doc = doc


def do_ensure(Class):
    """Pattern to make sure that the property and assigned values of the of the
    instance are valid before being instanciated.
    """
    def make_property(name, attribute):
        privateName = "__" + name

        def getter(self):
            return getattr(self, privateName)

        def setter(self, value):
            attribute.validate(name, value)
            setattr(self, privateName, value)
        return property(getter, setter, doc=attribute.doc)

    for name, attribute in Class.__dict__.items():
        if isinstance(attribute, Ensure):
            setattr(Class, name, make_property(name, attribute))

    return Class


### Validators #################################################################

def is_non_empty_str(name, value):

    if not isinstance(value, str):
        raise ValueError("{} must be of type str".format(name))
    if not bool(value):
        raise ValueError("{} may not be empty".format(name))


def is_non_empty_int(name, value):

    if not isinstance(value, int):
        raise ValueError("{} must be of type int".format(name))
    if not bool(value):
        raise ValueError("{} may not be empty".format(name))


def is_in_range(minimum=None, maximum=None):
    assert minimum is not None or maximum is not None

    def is_in_range(name, value):
        if not isinstance(value, numbers.Number):
            raise ValueError("{} must be a number".format(name))
        if minimum is not None and value <= minimum:
            raise ValueError("{} {} is too small".format(name, value))
        if maximum is not None and value >= maximum:
            raise ValueError("{} {} is too big".format(name, value))
    return is_in_range


def is_valid_key(name, key):
    assert len(str(key)) != 3, ("invalid key '{0}'".format(key))


def is_valid_postcode(name, postcode):
    # TODO: This validation can be improved.
        if not isinstance(postcode, numbers.Number):
            raise ValueError("{} must be a number".format(name))
        if len(str(postcode)) != 4:
            raise ValueError("{} {} is of incorrect fixed length".format(
                name, postcode))


def is_valid_phone_number(name, phone_number):

    if not isinstance(phone_number, int):
        raise ValueError("{} must be of type int".format(name))

    # TODO: add regex
    # if len(str(int(phone_number))) != 10:
    #     raise ValueError("{} is not a valid Phone Number".format(phone_number))
