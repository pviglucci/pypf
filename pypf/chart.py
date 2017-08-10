"""Classes to generate point and figure charts."""
from abc import ABCMeta
from abc import abstractmethod
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from pypf.terminal_format import bold
from pypf.terminal_format import red
from pypf.terminal_format import underline


class PFChartBase(metaclass=ABCMeta):
    """Base class for point and figure charts."""

    TWOPLACES = Decimal('0.01')

    def __init__(self, period=1, box_size=.01, reversal=3):
        """Initialize common functionality."""
        self.period = period
        self.box_size = Decimal(box_size)
        self.reversal = int(reversal)

        self.historical_data = []
        self.chart_data = []
        self.scale = OrderedDict()
        self.high_field = None
        self.low_field = None
        self.close_field = None
        self.date_field = None

        self.current_signal = None
        self.current_status = None
        self.current_action = None
        self.current_move = None
        self.current_column_index = None
        self.current_scale_index = None
        self.current_scale_value = None
        self.current_direction = None
        self.current_close = None

        self.chart_meta_data = OrderedDict()

    def create_chart(self, dump=False):
        """Populate the data and create the chart."""
        self._set_historical_data()
        self._set_price_fields()
        self._set_scale()
        self._set_chart_data()
        if dump:
            chart = self._get_chart()
            print(chart)

    def _get_chart(self):
        self._set_current_state()
        chart = ""
        chart += "\n"
        chart += self._get_chart_title()

        index = len(self.chart_data[0]) - 1
        first = True
        scale_right = None
        while index >= 0:
            for column in self.chart_data:
                if index in column:
                    if first:
                        scale_value = column[index]
                        if index == self.current_scale_index:
                            scale_left = (red(bold('{:7.2f}'
                                          .format(scale_value))))
                            scale_right = (red(bold('<< '))
                                           + red(bold('{:.2f}'
                                                 .format(self.current_close))))
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

    def _get_scale_index(self, value, direction):
        index = 0
        while index < len(self.scale):
            if self.scale[index] == value:
                return index
            elif self.scale[index] > value:
                if direction == 'x':
                    return index - 1
                else:
                    return index
            index += 1

    def _set_chart_data(self):
        self.chart_data = []
        self.chart_meta_data = OrderedDict()
        self.chart_data.append(self.scale)

        column = OrderedDict()
        column_index = 1
        direction = 'x'
        index = None
        month = None
        signal = 'none'
        prior_high_index = len(self.scale) - 1
        prior_low_index = 0

        for row in self.historical_data:
            day = self.historical_data[row]
            action = 'none'
            move = 0
            current_month = self._get_month(day[self.date_field])

            if index is None:
                # First day - set the starting index based
                # on the high and 'x' direction
                index = self._get_scale_index(day[self.high_field], 'x')
                column[index] = ['x', day[self.date_field]]
                month = current_month
                continue

            if direction == 'x':
                scale_index = self._get_scale_index(day[self.high_field], 'x')

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
                                                 day[self.date_field]]
                            else:
                                column[index] = ['x', day[self.date_field]]
                            first = False
                        else:
                            column[index] = ['x', day[self.date_field]]
                    month = current_month
                else:
                    # check for reversal
                    scale_index = self._get_scale_index(day[self.low_field],
                                                        'o')
                    if index - scale_index >= self.reversal:
                        # reversal
                        action = 'reverse x->o'
                        move = index - scale_index

                        if signal != 'sell' and scale_index < prior_low_index:
                            signal = 'sell'

                        prior_high_index = index
                        self.chart_data.append(column)
                        column_index += 1
                        column = OrderedDict()
                        direction = 'o'
                        first = True
                        while index > scale_index:
                            index -= 1
                            if first:
                                if current_month != month:
                                    column[index] = [current_month,
                                                     day[self.date_field]]
                                else:
                                    column[index] = ['d', day[self.date_field]]
                                first = False
                            else:
                                column[index] = ['d', day[self.date_field]]
                        month = current_month
                    else:
                        # no reversal - reset the scale_index
                        scale_index -= 1
            else:
                # in an 'o' column
                scale_index = self._get_scale_index(day[self.low_field], 'o')
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
                                                 day[self.date_field]]
                            else:
                                column[index] = ['o', day[self.date_field]]
                            first = False
                        else:
                            column[index] = ['o', day[self.date_field]]
                    month = current_month
                else:
                    # check for reversal
                    scale_index = self._get_scale_index(day[self.high_field],
                                                        'x')
                    if scale_index - index >= self.reversal:
                        # reversal
                        action = 'reverse o->x'
                        move = scale_index - index

                        if signal != 'buy' and scale_index > prior_high_index:
                            signal = 'buy'

                        prior_low_index = index
                        self.chart_data.append(column)
                        column_index += 1
                        column = OrderedDict()
                        direction = 'x'
                        first = True
                        while index < scale_index:
                            index += 1
                            if first:
                                if current_month != month:
                                    column[index] = [current_month,
                                                     day[self.date_field]]
                                else:
                                    column[index] = ['u', day[self.date_field]]
                                first = False
                            else:
                                column[index] = ['u', day[self.date_field]]
                        month = current_month
                    else:
                        # no reversal - reset the scale_index
                        scale_index += 1

            # Store the meta data for the day
            status = self._get_status(signal, direction)
            scale_value = (self.scale[scale_index]
                           .quantize(PFChartBase.TWOPLACES))
            prior_high = self.scale[prior_high_index]
            prior_low = self.scale[prior_low_index]
            self._store_base_metadata(day, signal, status, action, move,
                                      column_index, scale_index, scale_value,
                                      direction, prior_high, prior_low)

        self.chart_data.append(column)

        if len(self.chart_data[1]) < self.reversal:
            self.chart_data.pop(1)

        return self.chart_data

    def _set_current_state(self):
        current_meta_index = next(reversed(self.chart_meta_data))
        current_meta = self.chart_meta_data[current_meta_index]
        self.current_signal = current_meta['signal']
        self.current_status = current_meta['status']
        self.current_action = current_meta['action']
        self.current_move = current_meta['move']
        self.current_column_index = current_meta['column_index']
        self.current_scale_index = current_meta['scale_index']
        self.current_scale_value = current_meta['scale_value']
        self.current_direction = current_meta['direction']

    def _store_base_metadata(self, day, signal, status, action, move,
                             column_index, scale_index, scale_value,
                             direction, prior_high, prior_low):
        date_value = day['Date']
        self.chart_meta_data[date_value] = {}
        self.chart_meta_data[date_value]['signal'] = signal
        self.chart_meta_data[date_value]['status'] = status
        self.chart_meta_data[date_value]['action'] = action
        self.chart_meta_data[date_value]['move'] = move
        self.chart_meta_data[date_value]['column_index'] = column_index
        self.chart_meta_data[date_value]['scale_index'] = scale_index
        self.chart_meta_data[date_value]['scale_value'] = scale_value
        self.chart_meta_data[date_value]['direction'] = direction
        self.chart_meta_data[date_value]['prior_high'] = prior_high
        self.chart_meta_data[date_value]['prior_low'] = prior_low
        self._store_custom_metadata(day)

    @staticmethod
    def _get_month(date_value):
        datetime_object = datetime.strptime(date_value, '%Y-%m-%d')
        month = str(datetime_object.month)
        if month == '10':
            month = 'A'
        elif month == '11':
            month = 'B'
        elif month == '12':
            month = 'C'
        return bold(red(month))

    @staticmethod
    def _get_status(signal, direction):
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

    @abstractmethod
    def _get_chart_title(self):
        pass

    @abstractmethod
    def _set_historical_data(self):
        pass

    @abstractmethod
    def _set_price_fields(self):
        pass

    @abstractmethod
    def _set_scale(self):
        pass

    @abstractmethod
    def _store_custom_metadata(self, day):
        pass


class PFChart(PFChartBase):
    """Point and figure chart."""

    def __init__(self, security, period=1,
                 box_size=.01, reversal=3, method='HL'):
        """Initialize point and figure chart."""
        super().__init__(period, box_size, reversal)
        self.security = security
        self.method = method
        self.current_date = ''
        self.current_open = ''
        self.current_high = ''
        self.current_low = ''
        self.current_close = ''

        self.open_field = None
        self.volume_field = None

    def _get_chart_title(self):
        self._set_current_prices()
        title = ""
        title = title + "  " + bold(underline(self.security.symbol))
        title = (title
                 + "  ({:} o: {:.2f} h: {:.2f} l: {:.2f} c: {:.2f}"
                 .format(self.current_date, self.current_open,
                         self.current_high, self.current_low,
                         self.current_close)
                 + ")\n")

        title = (title
                 + "  "
                 + str((self.box_size * 100).quantize(PFChartBase.TWOPLACES))
                 + "% box, ")
        title = title + str(self.reversal) + " box reversal, "
        title = title + str(self.method) + " method\n"
        title = (title
                 + "  signal: "
                 + bold(self.current_signal)
                 + " status: " + bold(self.current_status)
                 + "\n\n")
        return title

    def _set_current_prices(self):
        day = next(reversed(self.historical_data))
        current_day = self.historical_data[day]
        self.current_date = current_day[self.date_field]
        self.current_open = (current_day[self.open_field]
                             .quantize(PFChartBase.TWOPLACES))
        self.current_high = (current_day[self.high_field]
                             .quantize(PFChartBase.TWOPLACES))
        self.current_low = (current_day[self.low_field]
                            .quantize(PFChartBase.TWOPLACES))
        self.current_close = (current_day[self.close_field]
                              .quantize(PFChartBase.TWOPLACES))

    def _set_historical_data(self):
        if len(self.security.historical_data) == 0:
            self.security.populate_data()

        days = int(self.period * 252)
        if len(self.security.historical_data) > days:
            offset = len(self.security.historical_data) - days
            i = 0
            while i < offset:
                self.security.historical_data.popitem(False)
                i += 1
            self.historical_data = self.security.historical_data
        else:
            self.historical_data = self.security.historical_data

    def _set_price_fields(self):
        if self.method == 'HL':
            self.high_field = 'High'
            self.low_field = 'Low'
        else:
            self.high_field = 'Close'
            self.low_field = 'Close'
        self.open_field = 'Open'
        self.close_field = 'Close'
        self.volume_field = 'Volume'
        self.date_field = 'Date'

    def _set_scale(self):
        row = next(iter(self.historical_data))
        day = self.historical_data[row]
        highest = day[self.high_field]
        lowest = day[self.low_field]

        for row in self.historical_data:
            day = self.historical_data[row]
            if day[self.high_field] > highest:
                highest = day[self.high_field]
            if day[self.low_field] < lowest:
                lowest = day[self.low_field]

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

        self.scale = OrderedDict()
        for index, scale_value in enumerate(temp_scale):
            self.scale[index] = scale_value

    def _store_custom_metadata(self, date_value):
        pass
