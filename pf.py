#!/usr/bin/env python3
"""Script to create point and figure charts at the command line."""
from argparse import ArgumentParser
from pypf.chart import PFChart
from pypf.instrument import Security


def main():
    """Program entry."""
    parser = __get_option_parser()
    options = parser.parse_args()
    __process_options(options)


def __get_option_parser():
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug",
                        action="store_true", dest="debug",
                        help="print debug messages to stdout")
    parser.add_argument("--interval",
                        action="store",
                        dest="interval",
                        choices=['1d', '1wk', '1mo'], default='1d',
                        metavar="INTERVAL",
                        help="specify day (1d), week (1wk), or month (1mo) \
                             interval [default: %(default)s]")
    parser.add_argument("--force-cache",
                        action="store_true", dest="force_cache",
                        help="force use of cached data [default: False]")
    parser.add_argument("--force-download",
                        action="store_true", dest="force_download",
                        help="force download of data [default: False]")
    parser.add_argument("--period",
                        action="store", dest="period",
                        type=int, default=10,
                        metavar="PERIOD",
                        help="set the years of data to download \
                             [default: %(default)s]")

    # Top level commands
    subparsers = parser.add_subparsers(help='description',
                                       metavar="command",
                                       dest='command')
    subparsers.required = True
    pf_parser = subparsers.add_parser('pf',
                                      help='create point and figure charts')
    pf_parser.add_argument("--box-size",
                           action="store", dest="box_size",
                           type=float, default=.01,
                           metavar="BOX_SIZE",
                           help="set the %% box size [default: %(default)s]")
    pf_parser.add_argument("--duration",
                           action="store", dest="duration",
                           type=float, default=1,
                           metavar="DURATION",
                           help="set the duration in years for the chart \
                                 [default: %(default)s]")
    pf_parser.add_argument("--method",
                           action="store",
                           dest="method",
                           choices=['HL', 'C'], default='HL',
                           metavar="METHOD",
                           help="specify High/Low (HL) or Close (C) \
                                 [default: %(default)s]")
    pf_parser.add_argument("--reversal",
                           action="store", dest="reversal",
                           type=int, default=3,
                           metavar="REVERSAL",
                           help="set the box reversal [default: %(default)s]")
    pf_parser.add_argument("--style",
                           action="store_true", dest="style",
                           help="use color and style in terminal output \
                                 [default: False]")
    pf_parser.add_argument("--trend-lines",
                           action="store_true", dest="trend_lines",
                           help="draw support and resistance lines \
                                 [default: False]")
    pf_parser.add_argument("symbol", metavar='SYMBOL',
                           help='the symbol of the security to chart')

    return parser


def __process_options(options):
    debug = options.debug
    interval = options.interval
    force_download = options.force_download
    force_cache = options.force_cache
    period = options.period

    box_size = options.box_size
    duration = options.duration
    method = options.method
    reversal = options.reversal
    style = options.style
    trend_lines = options.trend_lines
    symbol = options.symbol

    security = Security(symbol, force_download, force_cache,
                        interval, period, debug)
    chart = PFChart(security, box_size, duration, method,
                    reversal, style, trend_lines, debug)
    chart.create_chart(dump=True)


if __name__ == "__main__":
    main()
