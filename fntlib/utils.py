from enum import Enum
from typing import Any, Optional
import re


class Value():
    """A main class to specify a value/field in `fntlib`.

    This should NOT be used by end users."""

    type: type = None
    value: Any = None
    enum: Enum = None

    def __init__(self, value: Any = None, **kwargs) -> None:
        for name, member in kwargs.items():
            setattr(self, name, member)

        self.value = value

    def to_string(self) -> str:
        return (str(self) if not issubclass(type(self.value), Enum) else str(self.value.value)) if not type(self.value) == bool and not self.type == bool else str(int(self.value))

    def __repr__(self) -> str:
        return str(self.type(self.value)) if self.value and self.type else str(self.value)


class IntValue(Value):
    def __init__(self, value: Any = None, **kwargs) -> None:
        super().__init__(value, **kwargs)
        self.type = int


class BoolValue(Value):
    def __init__(self, value: Any = None, **kwargs) -> None:
        super().__init__(value, **kwargs)
        self.type = bool


class StrValue(Value):
    def __init__(self, value: Any = None, **kwargs) -> None:
        super().__init__(value, **kwargs)
        self.type = str


class EnumValue(Value):
    def __init__(self, value: Any = None, enum: Enum = None, **kwargs) -> None:
        super().__init__(value, **kwargs)
        self.type = enum


class ListValue(Value):
    def __init__(self, value: Any = None, type: type = None, **kwargs) -> None:
        super().__init__(value, **kwargs)
        self.type = list[type]


class DefaultClass():
    """A class that other classes inherit from.
    It has functions to use `Value` classes and to convert itself to string.

    This shold NOT be used by end users."""

    def __init__(self, args: Optional[dict[str, Any]] = None) -> None:
        if args:
            for name, value in args.items():
                if hasattr(self, name):
                    setattr(self, name, type(getattr(self, name))(value))

    def __setattr__(self, __name: str, __value: Any) -> None:
        if issubclass(type(__value), Value) or not issubclass(type(self.__getattribute__(__name)), Value):
            value = __value
        else:
            value = Value(value=__value, enum=self.__getattribute__(
                __name).enum, type=self.__getattribute__(__name).type)

        object.__setattr__(self, __name, value)

    def __repr__(self) -> str:
        # I know this expression is kind of extreme but ¯\_(ツ)_/¯
        return f'<{self.__class__.__name__} ' + \
            " ".join(
                [
                    x + "=" + (chr(0x22) if hasattr(self.__getattribute__(x), "type") and self.__getattribute__(
                        x).type == str and self.__getattribute__(x).value != None else "")
                    + str(self.__getattribute__(x))
                    + (chr(0x22) if hasattr(self.__getattribute__(x), "type") and self.__getattribute__(
                        x).type == str and self.__getattribute__(x).value != None else "")
                    for x in dir(self) if not x.startswith("__") and not type(getattr(self, x)).__name__ == "method"
                ]
            ) + \
            '>'

    def to_string(self, replacements: dict[str, str] = None) -> str:
        if not replacements:
            replacements = {}

        return ' '.join([
            replacements.get(x, x) + "=" + (chr(0x22) if hasattr(getattr(self, x), "type") and getattr(self, x).type == str and self.__getattribute__(x).value != None else "") +
            (str(getattr(self, x)) if not "to_string" in dir(
                getattr(self, x)) else getattr(self, x).to_string())
            + (chr(0x22) if hasattr(getattr(self, x), "type") and getattr(self,
               x).type == str and self.__getattribute__(x).value != None else "")
            for x in self.__dict__
            if not x.startswith("__") and not type(getattr(self, x)).__name__ == "method" and str(getattr(self, x)) != "None"
        ])


def replace_dict_key(dict: dict[str, Any], old_key: str, new_key: str) -> dict[str, Any]:
    """This func is used to replace value names from font to pythonised class names."""

    # This could be a way but it messes up attributes order for 'to_string'

    # if old_key in dict.keys():
    #     dict[new_key] = dict.pop(old_key)
    # return dict

    return {new_key if k == old_key else k: v for k, v in dict.items()}


def get_pairs(line: str) -> dict[str, str]:
    """This is a main function to get values from the font file"""
    return {y[0]: y[1] for y in [x.replace("\"", "").split("=") for x in re.split(r"\s+", line)][1:]}
