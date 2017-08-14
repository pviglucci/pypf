====
pypf
====

Simple set of classes that can be used to generate point and figure charts.
The package also includes a command line script (pf.py) that can be used
to create charts at the command line.

Installation
------------

    # pip3 install pypf

Usage
-----

To use in a program, simply do:

    >>> from pypf.chart import PFChart
    >>> from pypf.instrument import Security
    >>> security = Security(symbol, force_download, force_cache)
    >>> chart = PFChart(security, pf_period, pf_box_size, pf_reversal, pf_method, style_output)
    >>> chart.create_chart(dump=True)

To use at the command line:

    # pf.py pf --pf-period 1 --pf-box-size .01 --pf-reversal 3 AAPL

pf.py supports the following arguments:

    usage: pf.py [-h] [-v] [--force-cache] [--force-download] command ...

    positional arguments:
      command           description
        pf              create point and figure charts

    optional arguments:
      -h, --help        show this help message and exit
      -v, --verbose     increase status messages to stdout
      --force-cache     force use of cached data [default: False]
      --force-download  force download of data [default: False]

The pf command supports the following arguments:

    usage: pf.py pf [-h] [--pf-box-size SIZE] [--pf-method METHOD]
                [--pf-period PERIOD] [--pf-reversal REVERSAL] [--style]
                SYMBOL

    positional arguments:
    SYMBOL                the symbol of the security to chart

    optional arguments:
    -h, --help            show this help message and exit
    --pf-box-size SIZE    set the % box size [default: 0.01]
    --pf-method METHOD    specify High/Low (HL) or Close (C) [default: HL]
    --pf-period PERIOD    set the period [default: 1]
    --pf-reversal REVERSAL
                        set the % reversal [default: 3]
    --style               Use color and style in terminal output [default: False]
