import optparse
from urlunshort import resolve

def entrypoint_urlunshort():
    parser = optparse.OptionParser(usage="%prog url")
    options, args = parser.parse_args();
    if args:
        print resolve(args[0])

