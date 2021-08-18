#!/usr/bin/env python3
"""Script to create multiple point and figure charts. Good to look at the same charts frequently."""
from argparse import ArgumentParser
from pypf.chart import PFChart
from pypf.instrument import YahooSecurity


def main():
    """Program entry."""
    debug = False
    interval = 'd'
    force_download = False
    force_cache = False
    period = 10

    box_size = .01
    method = 'hl'
    reversal = 3
    style = True
    trend_lines = True
    indent = 3

    truncate = 50
    duration = 4

    symbols = [['spy',duration], ['dia',duration], ['qqq',duration], ['bac',duration], ['bk',duration]]


    for pf in symbols:
        symbol = pf[0]
        duration = pf[1]
        security = YahooSecurity(symbol, force_download, force_cache,
                                 period, debug)
        chart = PFChart(security, box_size, duration, interval, method,
                        reversal, style, trend_lines, debug, indent, truncate)
        chart.create_chart()
        print(chart.chart)


if __name__ == "__main__":
    main()
