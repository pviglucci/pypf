#!/usr/bin/env python3
"""Script to create point and figure charts at the command line."""
from argparse import ArgumentParser
from pypf.chart import PFChart
from pypf.instrument import GoogleSecurity
from pypf.instrument import YahooSecurity


def main():
    """Program entry."""
    parser = __get_option_parser()
    options = parser.parse_args()
    __process_options(options)


def __get_option_parser():
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug",
                        action="store_true", dest="debug",
                        help="print debug messages to stderr")
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
    parser.add_argument("--provider",
                        action="store",
                        dest="provider",
                        choices=['google', 'yahoo'], default='yahoo',
                        metavar="PROVIDER",
                        help="specify the data provider (yahoo or google) \
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
    pf_parser.add_argument("--dump-meta-data",
                           action="store_true", dest="dump_meta_data",
                           help="print chart meta data to stdout \
                                 [default: False]")
    pf_parser.add_argument("--duration",
                           action="store", dest="duration",
                           type=float, default=1,
                           metavar="DURATION",
                           help="set the duration in years for the chart \
                                 [default: %(default)s]")
    pf_parser.add_argument("--interval",
                           action="store",
                           dest="interval",
                           choices=['d', 'w', 'm'], default='d',
                           metavar="INTERVAL",
                           help="specify day (d), week (w), or month (m) \
                                 interval [default: %(default)s]")
    pf_parser.add_argument("--method",
                           action="store",
                           dest="method",
                           choices=['hl', 'c'], default='hl',
                           metavar="METHOD",
                           help="specify High/Low (hl) or Close (c) \
                                 [default: %(default)s]")
    pf_parser.add_argument("--reversal",
                           action="store", dest="reversal",
                           type=int, default=3,
                           metavar="REVERSAL",
                           help="set the box reversal [default: %(default)s]")
    pf_parser.add_argument("--indent",
                           action="store", dest="indent",
                           type=int, default=3,
                           metavar="INDENT",
                           help="set the indent of the chart [default: %(default)s]")
    pf_parser.add_argument("--truncate",
                           action="store", dest="truncate",
                           type=int, default=50,
                           metavar="TRUNCATE",
                           help="truncate the chart to fixed number of columns [default: %(default)s]")
    pf_parser.add_argument("--style",
                           action="store_true", dest="style",
                           help="use color and style in terminal output \
                                 [default: False]")
    pf_parser.add_argument("--suppress-chart",
                           action="store_true", dest="suppress_chart",
                           help="do not print the chart to stdout \
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
    indent = options.indent
    truncate = options.truncate

    if options.provider == 'google':
        security = GoogleSecurity(symbol, force_download, force_cache,
                                  period, debug)
    else:
        security = YahooSecurity(symbol, force_download, force_cache,
                                 period, debug)
    chart = PFChart(security, box_size, duration, interval, method,
                    reversal, style, trend_lines, debug, indent, truncate)
    chart.create_chart()
    if options.suppress_chart is False:
        print(chart.chart)
    if options.dump_meta_data is True:
        for day in chart.chart_meta_data:
            print(chart.chart_meta_data[day])

if __name__ == "__main__":
    main()
