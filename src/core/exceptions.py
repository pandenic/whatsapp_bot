"""Describe exceptions."""


class WrongBotTimeFormat(Exception):
    """If text does not match an allowed time format."""

    pass


class WrongBotDateFormat(Exception):
    """If text does not match an allowed date format."""

    pass


class WrongBotReminderCreateFormat(Exception):
    """If text does not match a reminder creation format."""

    pass


class WrongSelectorValue(Exception):
    """If a chosen menu selector number is wrong."""

    pass


class WrongReminderNumber(Exception):
    """If a chosen reminder number is wrong."""

    pass
