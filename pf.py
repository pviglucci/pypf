#!/usr/bin/env python3
"""This is the docstring."""
from argparse import ArgumentParser
from pypf.chart import PFChart
from pypf.instrument import Security

import logging
# TODO(me): Make colored output an option


def main():
    """Program entry."""
    parser = __get_option_parser()
    options = parser.parse_args()
    logging.basicConfig(format='[%(asctime)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=options.verbosity)
    __process_options(options)


def __get_option_parser():
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        action="store_const",
                        const=logging.INFO, dest="verbosity",
                        help="increase status messages to stdout")
    parser.add_argument("--force-cache",
                        action="store_true", dest="force_cache",
                        help="use cached data [default: False]")
    parser.add_argument("--force-download",
                        action="store_true", dest="force_download",
                        help="force download data [default: False]")

    # Top level commands
    subparsers = parser.add_subparsers(help='description',
                                       metavar="command",
                                       dest='command')
    subparsers.required = True
    pf_parser = subparsers.add_parser('pf',
                                      help='create point and figure charts')

    pf_parser.add_argument("--pf-box-size",
                           action="store", dest="pf_box_size",
                           type=float, default=.01,
                           metavar="SIZE",
                           help='set the %% box size [default: %(default)s]')
    pf_parser.add_argument("--pf-method",
                           action="store",
                           dest="pf_chart_method",
                           choices=['HL', 'C'], default='HL',
                           metavar="METHOD",
                           help="specify High/Low (HL) or Close (C) \
                                 [default: %(default)s]")
    pf_parser.add_argument("--pf-period",
                           action="store", dest="pf_period",
                           type=float, default=1,
                           metavar="PERIOD",
                           help="set the period [default: %(default)s]")
    pf_parser.add_argument("--pf-reversal",
                           action="store", dest="pf_reversal",
                           type=int, default=3,
                           metavar="REVERSAL",
                           help="set the %% reversal [default: %(default)s]")
    pf_parser.add_argument("--style",
                           action="store_true", dest="style_output",
                           help="Use color and style in terminal output [default: False]")                           
    pf_parser.add_argument("symbol", metavar='SYMBOL',
                           help='the symbol of the security to chart')

    return parser


def __process_options(options):
    for option in vars(options):
        logging.info(option + ': ' + str(vars(options)[option]))

    force_download = options.force_download
    force_cache = options.force_cache
    pf_box_size = options.pf_box_size
    pf_method = options.pf_chart_method
    pf_period = options.pf_period
    pf_reversal = options.pf_reversal
    style_output = options.style_output

    symbol = options.symbol
    security = Security(symbol, force_download, force_cache)

    chart = PFChart(security, pf_period, pf_box_size, pf_reversal, pf_method, style_output)
    chart.create_chart(dump=True)


if __name__ == "__main__":
    main()
