class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def success(message):
    return "{0}{1}{2}".format(bcolors.OKGREEN, message, bcolors.ENDC)

def failure(message):
    return "{0}{1}{2}".format(bcolors.FAIL, message, bcolors.ENDC)

def warning(message):
    return "{0}{1}{2}".format(bcolors.WARNING, message, bcolors.ENDC)