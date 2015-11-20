import sys

from jakdojade.orm import JakDojade
import logging
import argparse
logging.basicConfig(level=logging.DEBUG)


def options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('line')
    parser.add_argument('stop')
    parser.add_argument('direction')
    return parser.parse_args(args)


def main():
    jd = JakDojade()

    city = jd.city('warsaw')
    operator = city.operator('ztm')


    line = operator.line(10)
    print(operator)
    print(line.routes[0].stop('dworzec centralny'))
    print(line.routes[0])
    print(line)

if __name__ == "__main__":
    main()
