"""Module initialization."""
import logging

logging.basicConfig(format=('%(levelname)-8s'
                            + '%(name)10s:'
                            + '%(lineno)4d '
                            + '%(funcName)22s() -- '
                            + '%(message)s'),
                    level=logging.WARNING)
