pypf
--------
Simple set of classes that can be used to generate command line
point and figure charts. 

To use (with caution), simply do::

    >>> from pypf.chart import PFChart
    >>> from pypf.instrument import Security
    >>> security = Security(symbol, force_download, force_cache)
    >>> chart = PFChart(security, pf_period, pf_box_size, pf_reversal, pf_method)
    >>> chart.create_chart(dump=True)
