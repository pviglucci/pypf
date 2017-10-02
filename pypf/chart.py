"""Classes to generate point and figure charts."""
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

import logging
import pypf.terminal_format


class PFChart(object):
    """Base class for point and figure charts."""

    TWOPLACES = Decimal('0.01')

    def __init__(self, instrument, box_size=.01, duration=1.0, method='hl',
                 reversal=3, style=False, trend_lines=False,
                 debug=False):
        """Initialize common functionality."""
        self._log = logging.getLogger(self.__class__.__name__)
        if debug is True:
            self._log.setLevel(logging.DEBUG)
            self._log.debug(self)

        self.instrument = instrument
        self.box_size = Decimal(box_size).quantize(PFChart.TWOPLACES)
        self.duration = Decimal(duration).quantize(PFChart.TWOPLACES)
        self.method = method
        self.reversal = int(reversal)
        self.style_output = style
        self.trend_lines = trend_lines

    @property
    def box_size(self):
        """Get the box_size."""
        return self._box_size

    @box_size.setter
    def box_size(self, value):
        self._box_size = value
        self._log.debug('set self._box_size to ' + str(self._box_size))

    @property
    def chart(self):
        """Get the chart."""
        return self._chart

    @property
    def chart_meta_data(self):
        """Get the chart meta data."""
        return self._chart_meta_data

    @property
    def duration(self):
        """Get the duration."""
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
        self._log.debug('set self._duration to ' + str(self._duration))

    @property
    def instrument(self):
        """Get the instrument."""
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = value
        self._log.debug('set self._instrument to ' + str(self._instrument))

    @property
    def method(self):
        """Get the method."""
        return self._method

    @method.setter
    def method(self, value):
        if value not in ["hl", "c"]:
            raise ValueError("incorrect method: "
                             "valid methods are hl, c")
        self._method = value
        self._log.debug('set self._method to ' + self._method)

    @property
    def reversal(self):
        """Get the reversal."""
        return self._reversal

    @reversal.setter
    def reversal(self, value):
        self._reversal = value
        self._log.debug('set self._reversal to ' + str(self._reversal))

    @property
    def style_output(self):
        """Get the style_output."""
        return self._style_output

    @style_output.setter
    def style_output(self, value):
        self._style_output = value
        self._log.debug('set self._style_output to ' + str(self._style_output))

    @property
    def trend_lines(self):
        """Get the trend_lines."""
        return self._trend_lines

    @trend_lines.setter
    def trend_lines(self, value):
        self._trend_lines = value
        self._log.debug('set self._trend_lines to ' + str(self._trend_lines))

    def create_chart(self):
        """Populate the data and create the chart."""
        self._initialize()
        self._set_historical_data()
        self._set_price_fields()
        self._set_scale()
        self._set_chart_data()
        self._chart = self._get_chart()

    def _get_chart(self):
        self._set_current_state()
        chart = ""
        chart += "\n"
        chart += self._get_chart_title()

        index = len(self._chart_data[0]) - 1
        first = True
        scale_right = None
        while index >= 0:
            for column in self._chart_data:
                if index in column:
                    if first:
                        scale_value = column[index]
                        if index == self._current_scale_index:
                            scale_left = (self._style('red',
                                          self._style('bold', '{:7.2f}'))
                                          .format(scale_value))
                            scale_right = (self._style('red',
                                           self._style('bold', '<< '))
                                           + self._style('red',
                                                         self._style('bold',
                                                                     '{:.2f}'))
                                           .format(self._current_close))
                        else:
                            scale_left = '{:7.2f}'.format(scale_value)
                            scale_right = '{:.2f}'.format(scale_value)
                        chart = chart + scale_left + '| '
                        first = False
                    else:
                        chart = chart + ' ' + column[index][0]
                else:
                    chart += '  '

            chart += '   |' + scale_right
            chart += "\n"
            index -= 1
            first = True
        return chart

    def _get_chart_title(self):
        self._set_current_prices()
        title = ""
        title = title + "  " + self._style('bold',
                                           self._style('underline',
                                                       self.instrument.symbol))
        title = (title
                 + "  ({:} o: {:.2f} h: {:.2f} l: {:.2f} c: {:.2f}"
                 .format(self._current_date, self._current_open,
                         self._current_high, self._current_low,
                         self._current_close)
                 + ")\n")

        title = (title
                 + "  "
                 + str((self.box_size * 100).quantize(PFChart.TWOPLACES))
                 + "% box, ")
        title = title + str(self.reversal) + " box reversal, "
        title = title + str(self.method) + " method\n"
        title = (title
                 + "  signal: "
                 + self._style('bold', self._current_signal)
                 + " status: " + self._style('bold', self._current_status)
                 + "\n\n")
        return title

    def _get_month(self, date_value):
        datetime_object = datetime.strptime(date_value, '%Y-%m-%d')
        month = str(datetime_object.month)
        if month == '10':
            month = 'A'
        elif month == '11':
            month = 'B'
        elif month == '12':
            month = 'C'
        return self._style('bold', self._style('red', month))

    def _get_scale_index(self, value, direction):
        index = 0
        while index < len(self._scale):
            if self._scale[index] == value:
                return index
            elif self._scale[index] > value:
                if direction == 'x':
                    return index - 1
                else:
                    return index
            index += 1

    def _get_status(self, signal, direction):
        if signal == 'buy' and direction == 'x':
            status = 'bull confirmed'
        elif signal == 'buy' and direction == 'o':
            status = 'bull correction'
        elif signal == 'sell' and direction == 'o':
            status = 'bear confirmed'
        elif signal == 'sell' and direction == 'x':
            status = 'bear correction'
        else:
            status = 'none'
        return status

    def _set_chart_data(self):
        self._log.info('generating chart')
        self._chart_data = []
        self._chart_meta_data = OrderedDict()
        self._support_lines = []
        self._resistance_lines = []
        self._chart_data.append(self._scale)

        column = OrderedDict()
        column_index = 1
        direction = 'x'
        index = None
        month = None
        signal = 'none'
        prior_high_index = len(self._scale) - 1
        prior_low_index = 0

        for row in self._historical_data:
            day = self._historical_data[row]
            action = 'none'
            move = 0
            current_month = self._get_month(day[self._date_field])

            if index is None:
                # First day - set the starting index based
                # on the high and 'x' direction
                index = self._get_scale_index(day[self._high_field], 'x')
                column[index] = ['x', day[self._date_field]]
                month = current_month
                continue

            if direction == 'x':
                scale_index = self._get_scale_index(day[self._high_field], 'x')

                if scale_index > index:
                    # new high
                    action = 'x'
                    move = scale_index - index

                    if signal != 'buy' and scale_index > prior_high_index:
                        signal = 'buy'

                    first = True
                    while index < scale_index:
                        index += 1
                        if first:
                            if current_month != month:
                                column[index] = [current_month,
                                                 day[self._date_field]]
                            else:
                                column[index] = ['x', day[self._date_field]]
                            first = False
                        else:
                            column[index] = ['x', day[self._date_field]]
                    month = current_month
                else:
                    # check for reversal
                    x_scale_index = scale_index
                    scale_index = self._get_scale_index(day[self._low_field],
                                                        'o')
                    if index - scale_index >= self.reversal:
                        # reversal
                        action = 'reverse x->o'
                        move = index - scale_index

                        if signal != 'sell' and scale_index < prior_low_index:
                            signal = 'sell'

                        prior_high_index = index
                        self._resistance_lines.append([column_index,
                                                       prior_high_index + 1])
                        self._chart_data.append(column)
                        column_index += 1
                        column = OrderedDict()
                        direction = 'o'
                        first = True
                        while index > scale_index:
                            index -= 1
                            if first:
                                if current_month != month:
                                    column[index] = [current_month,
                                                     day[self._date_field]]
                                else:
                                    column[index] = ['d',
                                                     day[self._date_field]]
                                first = False
                            else:
                                column[index] = ['d', day[self._date_field]]
                        month = current_month
                    else:
                        # no reversal - reset the scale_index
                        scale_index = x_scale_index
            else:
                # in an 'o' column
                scale_index = self._get_scale_index(day[self._low_field], 'o')
                if scale_index < index:
                    # new low
                    action = 'o'
                    move = index - scale_index

                    if signal != 'sell' and scale_index < prior_low_index:
                        signal = 'sell'

                    first = True
                    while index > scale_index:
                        index -= 1
                        if first:
                            if current_month != month:
                                column[index] = [current_month,
                                                 day[self._date_field]]
                            else:
                                column[index] = ['o', day[self._date_field]]
                            first = False
                        else:
                            column[index] = ['o', day[self._date_field]]
                    month = current_month
                else:
                    # check for reversal
                    o_scale_index = scale_index
                    scale_index = self._get_scale_index(day[self._high_field],
                                                        'x')
                    if scale_index - index >= self.reversal:
                        # reversal
                        action = 'reverse o->x'
                        move = scale_index - index

                        if signal != 'buy' and scale_index > prior_high_index:
                            signal = 'buy'

                        prior_low_index = index
                        self._support_lines.append([column_index,
                                                    prior_low_index - 1])
                        self._chart_data.append(column)
                        column_index += 1
                        column = OrderedDict()
                        direction = 'x'
                        first = True
                        while index < scale_index:
                            index += 1
                            if first:
                                if current_month != month:
                                    column[index] = [current_month,
                                                     day[self._date_field]]
                                else:
                                    column[index] = ['u',
                                                     day[self._date_field]]
                                first = False
                            else:
                                column[index] = ['u', day[self._date_field]]
                        month = current_month
                    else:
                        # no reversal - reset the scale_index
                        scale_index = o_scale_index

            # Store the meta data for the day
            status = self._get_status(signal, direction)
            scale_value = (self._scale[scale_index]
                           .quantize(PFChart.TWOPLACES))
            prior_high = self._scale[prior_high_index]
            prior_low = self._scale[prior_low_index]
            self._store_base_metadata(day, signal, status, action, move,
                                      column_index, scale_index, scale_value,
                                      direction, prior_high, prior_low)

        self._chart_data.append(column)

        if len(self._chart_data[1]) < self.reversal:
            self._chart_data.pop(1)
            for line in self._support_lines:
                line[0] = line[0] - 1
            for line in self._resistance_lines:
                line[0] = line[0] - 1

        if self.trend_lines:
            self._set_trend_lines()

        return self._chart_data

    def _initialize(self):
        self._chart = None
        self._chart_data = []
        self._chart_meta_data = OrderedDict()
        self._historical_data = []
        self._scale = OrderedDict()

        self._current_date = None
        self._current_open = None
        self._current_high = None
        self._current_low = None
        self._current_close = None

        self._date_field = None
        self._open_field = None
        self._high_field = None
        self._low_field = None
        self._close_field = None
        self._volume_field = None

        self._current_signal = None
        self._current_status = None
        self._current_action = None
        self._current_move = None
        self._current_column_index = None
        self._current_scale_index = None
        self._current_scale_value = None
        self._current_direction = None
        self._support_lines = []
        self._resistance_lines = []

    def _is_complete_line(self, start_point, line_type='support'):
        c_index = start_point[0]
        s_index = start_point[1]
        while c_index < len(self._chart_data):
            if s_index in self._chart_data[c_index]:
                return False
            c_index += 1
            if line_type == 'support':
                s_index += 1
            else:
                s_index -= 1
        if c_index - start_point[0] > 2:
            return True
        else:
            return False

    def _set_trend_lines(self):
        for start_point in self._support_lines:
            c_index = start_point[0]
            s_index = start_point[1]
            if self._is_complete_line(start_point, 'support'):
                while c_index < len(self._chart_data):
                    self._chart_data[c_index][s_index] = [self._style('bold',
                                                          self._style('blue',
                                                                      '.')),
                                                          '']
                    c_index += 1
                    s_index += 1

        for start_point in self._resistance_lines:
            c_index = start_point[0]
            s_index = start_point[1]
            if self._is_complete_line(start_point, 'resistance'):
                while c_index < len(self._chart_data):
                    self._chart_data[c_index][s_index] = [self._style('bold',
                                                          self._style('blue',
                                                                      '.')),
                                                          '']
                    c_index += 1
                    s_index -= 1

    def _set_current_prices(self):
        day = next(reversed(self._historical_data))
        current_day = self._historical_data[day]
        self._current_date = current_day[self._date_field]
        self._current_open = (current_day[self._open_field]
                              .quantize(PFChart.TWOPLACES))
        self._current_high = (current_day[self._high_field]
                              .quantize(PFChart.TWOPLACES))
        self._current_low = (current_day[self._low_field]
                             .quantize(PFChart.TWOPLACES))
        self._current_close = (current_day[self._close_field]
                               .quantize(PFChart.TWOPLACES))

    def _set_current_state(self):
        current_meta_index = next(reversed(self._chart_meta_data))
        current_meta = self._chart_meta_data[current_meta_index]
        self._current_signal = current_meta['signal']
        self._current_status = current_meta['status']
        self._current_action = current_meta['action']
        self._current_move = current_meta['move']
        self._current_column_index = current_meta['column_index']
        self._current_scale_index = current_meta['scale_index']
        self._current_scale_value = current_meta['scale_value']
        self._current_direction = current_meta['direction']

    def _set_historical_data(self):
        self._log.info('setting historical data')
        if len(self.instrument.daily_historical_data) == 0:
            self.instrument.populate_data()

        if self.instrument.interval == 'd':
            days = int(self.duration * 252)
            self._historical_data = self.instrument.daily_historical_data
        elif self.instrument.interval == 'w':
            days = int(self.duration * 52)
            self._historical_data = self.instrument.weekly_historical_data
        elif self.instrument.interval == 'm':
            days = int(self.duration * 12)
            self._historical_data = self.instrument.monthly_historical_data

        if len(self._historical_data) > days:
            offset = len(self._historical_data) - days
            i = 0
            while i < offset:
                self._historical_data.popitem(False)
                i += 1

    def _set_price_fields(self):
        if self.method == 'hl':
            self._high_field = 'High'
            self._low_field = 'Low'
        else:
            self._high_field = 'Close'
            self._low_field = 'Close'
        self._open_field = 'Open'
        self._close_field = 'Close'
        self._volume_field = 'Volume'
        self._date_field = 'Date'

    def _set_scale(self):
        row = next(iter(self._historical_data))
        day = self._historical_data[row]
        highest = day[self._high_field]
        lowest = day[self._low_field]

        for row in self._historical_data:
            day = self._historical_data[row]
            if day[self._high_field] > highest:
                highest = day[self._high_field]
            if day[self._low_field] < lowest:
                lowest = day[self._low_field]

        temp_scale = []
        current = Decimal(.01)
        temp_scale.append(current)

        while current < highest:
            value = current + (current * self.box_size)
            temp_scale.append(value)
            current = value

        slice_point = 0
        for index, scale_value in enumerate(temp_scale):
            if scale_value > lowest:
                slice_point = index - 1
                break
        temp_scale = temp_scale[slice_point:]

        self._scale = OrderedDict()
        for index, scale_value in enumerate(temp_scale):
            self._scale[index] = scale_value

    def _store_base_metadata(self, day, signal, status, action, move,
                             column_index, scale_index, scale_value,
                             direction, prior_high, prior_low):
        date_value = day['Date']
        self._chart_meta_data[date_value] = {}
        self._chart_meta_data[date_value]['signal'] = signal
        self._chart_meta_data[date_value]['status'] = status
        self._chart_meta_data[date_value]['action'] = action
        self._chart_meta_data[date_value]['move'] = move
        self._chart_meta_data[date_value]['column_index'] = column_index
        self._chart_meta_data[date_value]['scale_index'] = scale_index
        self._chart_meta_data[date_value]['scale_value'] = scale_value
        self._chart_meta_data[date_value]['direction'] = direction
        self._chart_meta_data[date_value]['prior_high'] = (prior_high
                                                           .quantize(
                                                               PFChart
                                                               .TWOPLACES))
        self._chart_meta_data[date_value]['prior_low'] = (prior_low
                                                          .quantize(
                                                              PFChart
                                                              .TWOPLACES))
        self._chart_meta_data[date_value]['date'] = day['Date']
        self._chart_meta_data[date_value]['open'] = (day['Open']
                                                     .quantize(
                                                         PFChart
                                                         .TWOPLACES))
        self._chart_meta_data[date_value]['high'] = (day['High']
                                                     .quantize(
                                                         PFChart
                                                         .TWOPLACES))
        self._chart_meta_data[date_value]['low'] = (day['Low']
                                                    .quantize(
                                                        PFChart
                                                        .TWOPLACES))
        self._chart_meta_data[date_value]['close'] = (day['Close']
                                                      .quantize(
                                                          PFChart
                                                          .TWOPLACES))
        self._chart_meta_data[date_value]['volume'] = day['Volume']
        self._store_custom_metadata(day)

    def _store_custom_metadata(self, day):
        pass

    def _style(self, style, message):
        if self.style_output:
            method = getattr(pypf.terminal_format, style)
            return method(message)
        else:
            return message
