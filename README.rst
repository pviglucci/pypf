====
pypf
====

Simple set of classes that can be used to generate point and figure charts.
The package also includes a script (pf.py) that can be used to create charts
at the command line that look like this::

    BAC  (2017-08-25 o: 23.89 h: 24.07 l: 23.75 c: 23.77)
    1.00% box, 3 box reversal, HL method
    signal: sell status: bear correction

    25.42|                                        .           |25.42
    25.17|                                        x .         |25.17
    24.92|  d                                 x   x d .       |24.92
    24.68|  d                                 7 d 8 d u .     |24.68
    24.43|  d                                 x d u d u d .   |24.43
    24.19|  o             x   x               x d u d u d     |24.19
    23.95|  o             x d u d     x   u   x d u o   d u   |<< 23.77
    23.71|  o     x   u   x d u d     x d u d x o       d u   |23.71
    23.48|  o     u 4 u d x d 5 d x   x d u d u         o u   |23.48
    23.25|  o u   u d u d x o   d u d x d   d u         o .   |23.25
    23.02|  o u d u d   d u     d u d u     o u         .     |23.02
    22.79|  o u d u     o u     d u d u     o                 |22.79
    22.56|  o   d u     o u     d   d u                       |22.56
    22.34|      d u     o           d 6                       |22.34
    22.12|      d                   d                         |22.12
    21.90|                                                    |21.90

Installation
------------

Install using pip::

    $ pip install pypf

Usage
-----

To use in a program, simply do::

    from pypf.chart import PFChart
    from pypf.instrument import Security
    security = Security(symbol, force_download, force_cache, interval, period)
    chart = PFChart(security, duration, box_size, reversal, method, style)
    chart.create_chart(dump=True)

To use at the command line::

    $ pf.py -v pf --duration 1 --box-size .01 --reversal 3 AAPL

pf.py supports the following arguments::

    usage: pf.py [-h] [-d] [--interval INTERVAL] [--force-cache]
                 [--force-download] [--period PERIOD]
                 command ...

    positional arguments:
      command              description
        pf                 create point and figure charts

    optional arguments:
      -h, --help           show this help message and exit
      -d, --debug          print debug messages to stdout
      --interval INTERVAL  specify day (1d), week (1wk), or month (1mo) interval
                           [default: 1d]
      --force-cache        force use of cached data [default: False]
      --force-download     force download of data [default: False]
      --period PERIOD      set the years of data to download [default: 10]

The pf command supports the following arguments::

    usage: pf.py pf [-h] [--box-size BOX_SIZE] [--duration DURATION]
                    [--method METHOD] [--reversal REVERSAL] [--style]
                    [--trend-lines]
                    SYMBOL

    positional arguments:
      SYMBOL               the symbol of the security to chart

    optional arguments:
      -h, --help           show this help message and exit
      --box-size BOX_SIZE  set the % box size [default: 0.01]
      --duration DURATION  set the duration in years for the chart [default: 1]
      --method METHOD      specify High/Low (HL) or Close (C) [default: HL]
      --reversal REVERSAL  set the box reversal [default: 3]
      --style              use color and style in terminal output [default: False]
      --trend-lines        draw support and resistance lines [default: False]

License
-------

Copyright (c) 2017 Peter J. Viglucci

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
