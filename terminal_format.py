"""Classes to simplify formatting terminal output."""


class Colors(object):
    """Define colors."""

    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'


class Styles(object):
    """Define styles."""

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def black(message):
    """Set color to black."""
    return Colors.BLACK + str(message) + Colors.ENDC


def red(message):
    """Set color to red."""
    return Colors.RED + str(message) + Colors.ENDC


def green(message):
    """Set color to green."""
    return Colors.GREEN + str(message) + Colors.ENDC


def yellow(message):
    """Set color to yellow."""
    return Colors.YELLOW + str(message) + Colors.ENDC


def blue(message):
    """Set color to blue."""
    return Colors.BLUE + str(message) + Colors.ENDC


def magenta(message):
    """Set color to magenta."""
    return Colors.MAGENTA + str(message) + Colors.ENDC


def cyan(message):
    """Set color to cyan."""
    return Colors.CYAN + str(message) + Colors.ENDC


def white(message):
    """Set color to white."""
    return Colors.WHITE + str(message) + Colors.ENDC


def bold(message):
    """Set style to bold."""
    return Styles.BOLD + str(message) + Styles.ENDC


def underline(message):
    """Set style to underline."""
    return Styles.UNDERLINE + str(message) + Styles.ENDC
