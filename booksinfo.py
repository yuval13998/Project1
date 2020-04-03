
from decimal import getcontext, Decimal

class BooksExtra():
    """docstring for ."""

    def __init__(self, existrev, existlike, likecount, avRate, rate):
        self.existrev = existrev
        self.existlike = existlike
        self.likecount = likecount
        goodreads = float(avRate)
        self.avRate =  float("{:.1f}".format(goodreads))
        self.rate = float("{:.1f}".format(rate))
        x = float("{:.1f}".format((goodreads+rate)/2))
        if self.rate != 0 and self.avRate != 0:
            self.totalrate = x
        elif self.rate == 0 and self.avRate != 0:
            self.totalrate = self.avRate
        elif self.rate == 0 and self.avRate == 0:
            self.totalrate = x
        else:
            self.totalrate = self.rate
