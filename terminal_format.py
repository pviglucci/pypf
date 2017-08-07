class Colors:
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'


class Styles:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def black(message):
    return Colors.BLACK + str(message) + Colors.ENDC


def red(message):
    return Colors.RED + str(message) + Colors.ENDC


def green(message):
    return Colors.GREEN + str(message) + Colors.ENDC


def yellow(message):
    return Colors.YELLOW + str(message) + Colors.ENDC


def blue(message):
    return Colors.BLUE + str(message) + Colors.ENDC


def magenta(message):
    return Colors.MAGENTA + str(message) + Colors.ENDC


def cyan(message):
    return Colors.CYAN + str(message) + Colors.ENDC


def white(message):
    return Colors.WHITE + str(message) + Colors.ENDC


def bold(message):
    return Styles.BOLD + str(message) + Styles.ENDC


def underline(message):
    return Styles.UNDERLINE + str(message) + Styles.ENDC