"""
one line to give the program's name and a brief description
Copyright © 2016 yourname

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
