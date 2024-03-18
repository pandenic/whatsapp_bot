"""Define constants for a project."""
import enum


class ExtendedEnum(enum.Enum):
    """Extend Enum class."""

    @classmethod
    def get_list(cls):
        """Return a list of Enum's entities."""
        return [value for value in cls]

    @classmethod
    def get_numbered_str(cls, start=0):
        """Return a numbered list of Enum's values."""
        return "\n".join(
            [str(i) + ": " + value.value for i, value in enumerate(cls)][
                start:
            ],
        )


class RepeatInterval(ExtendedEnum):
    """Define choices for reminders' repeat interval."""

    NON_REPEAT = "Non-repeatable"
    EVERYDAY = "Everyday"
    EVERY_WEEK = "Every week"
    EVERY_MONTH = "Every month"
    EVERY_YEAR = "Every year"


class Selector(ExtendedEnum):
    """Define choices for a menu selector."""

    GREETING = "Greeting"
    CREATE_REMINDER = "Create reminder"
    SHOW_ACTIVE_REMINDERS = "Show active reminders"
    DELETE_REMINDER = "Delete reminder"
    CREATE_REPEATABLE_REMINDER = "Create repeatable reminder"


class RegexPatterns:
    """Define regex patterns for validation."""

    BOT_TIME = r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
    BOT_DATE = (
        r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|"
        r"(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2"
        r"))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29("
        r"\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:"
        r"0[48]|[2468][048]|[13579][26])|(?:(?:16|"
        r"[2468][048]|[3579][26])00))))$|^(?:0?[1-9]"
        r"|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])"
        r"|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
    )
