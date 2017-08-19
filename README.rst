====
pypf
====

Simple set of classes that can be used to generate point and figure charts.
The package also includes a script (pf.py) that can be used to create charts
at the command line.

Installation
------------

Install using pip::

    $ pip3 install pypf

Usage
-----

To use in a program, simply do::

    from pypf.chart import PFChart
    from pypf.instrument import Security
    security = Security(symbol, force_download, force_cache, interval, period)
    chart = PFChart(security, duration, box_size, reversal, method, style)
    chart.create_chart(dump=True)

To use at the command line::

    $ pf.py pf --pf-period 1 --pf-box-size .01 --pf-reversal 3 AAPL

pf.py supports the following arguments::

    usage: pf.py [-h] [-v] [--interval INTERVAL] [--force-cache]
                 [--force-download] [--period PERIOD]
                 command ...

    positional arguments:
      command              description
        pf                 create point and figure charts

    optional arguments:
      -h, --help           show this help message and exit
      -v, --verbose        increase status messages to stdout
      --interval INTERVAL  specify day (1d), week (1wk), or month (1mo) interval
                           [default: 1d]
      --force-cache        force use of cached data [default: False]
      --force-download     force download of data [default: False]
      --period PERIOD      set the years of data to download [default: 10]

The pf command supports the following arguments::

    usage: pf.py pf [-h] [--box-size BOX_SIZE] [--duration DURATION]
                    [--method METHOD] [--reversal REVERSAL] [--style]
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
