"""
trading-server is a multi-asset, multi-strategy, event-driven execution
and backtesting platform (OEMS) for trading common markets.

Copyright (C) 2020  Sam Breznikar <sam@sdbgroup.io>

Licensed under GNU General Public License 3.0 or later.

Some rights reserved. See LICENSE.md, AUTHORS.md.
"""

from dateutil import parser
from datetime import datetime


class Event(object):
    """
    Base class for various system events.
    """


class MarketEvent(Event):
    """
    Wrapper for new market data. Consumed by Strategy object to
    produce Signal events.
    """

    DTFMT = '%Y-%m-%d %H:%M'

    DTFMT = '%Y-%m-%d %H:%M'

    def __init__(self, exchange, bar):
        self.type = 'MARKET'
        self.exchange = exchange
        self.bar = bar

    def __str__(self):
        return "MarketEvent - Exchange: %s, Symbol: %s, TS: %s, Close: %s" % (
            self.exchange, self.bar['symbol'],
            self.get_datetime(), self.bar['close'])

    def get_bar(self):
        return self.bar

    def get_exchange(self):
        return self.exchange

    def get_datetime(self):
        return datetime.fromtimestamp(
            self.bar['timestamp']).strftime(self.DTFMT),


class SignalEvent(Event):
    """
    A trade signal. Consumed by Portfolio to produce Order events.
    """

    def __init__(self, symbol, datetime, signal_type):
        self.type = 'SIGNAL'
        self.symbol = symbol            # Ticker code.
        self.datetime = datetime
        self.signal_type = signal_type  # LONG, SHORT.


class OrderEvent(Event):
    """
    Contains order details to be sent to a broker/exchange.
    """

    def __init__(self, symbol, exchange, order_type, quantity):
        self.type = 'ORDER'
        self.symbol = symbol            # Instrument ticker.
        self.exchange = exchange        # Source exchange.
        self.order_type = order_type    # MKT, LMT, SMKT, SLMT.
        self.quantity = quantity        # Integer.

    def __str__(self):
        return "OrderEvent - Symbol: %s, Type: %s, Qty: %s, Direction: %s" % (
            self.symbol, self.order_type, self.quantity, self.direction)


class FillEvent(Event):
    """
    Holds transaction data including fees/comissions, slippage, brokerage,
    actual fill price, timestamp, etc.
    """

    def __init__(self, timestamp, symbol, exchange, quantity,
                 direction, fill_cost, commission=None):
        self.type = 'FILL'
        self.timestamp = timestamp     # Fill timestamp
        self.symbol = symbol           # Instrument ticker
        self.exchange = exchange       # Source exchange
        self.quantity = quantity       # Position size.
        self.fill_cost = fill_cost     # USD value of fees.

        # use BitMEX taker fees as placeholder
        if commission is None:
            self.commission = (fill_cost / 100) * 0.075
        else:
            self.commission = commission

    def calculate_commission(self):
        """
        """
