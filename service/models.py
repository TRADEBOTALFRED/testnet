from django.db import models
from django.utils import timezone

# from service.tasks import demo_task

PRICE_MAX_DIGITS = 10
PRICE_DEC_PLACES = 5


class Market(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=120, default='')

    def __str__(self):
        return self.name


class Timeframe(models.Model):
    name = models.CharField(max_length=16)
    minutes = models.IntegerField(default=1)

    def __str__(self):
        return "{0} ({1} min)".format(self.name, self.minutes)

    def seconds(self):
        return self.minutes * 60


class Pair(models.Model):
    name = models.CharField(max_length=80)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} {1}".format(self.name, self.market)


class PairIndex(models.Model):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)
    timeframe = models.ForeignKey(Timeframe, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.pair, self.timeframe)


class PairData(models.Model):
    pair_index = models.ForeignKey(PairIndex, on_delete=models.CASCADE,db_index=True)
    high_price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DEC_PLACES)
    low_price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DEC_PLACES)
    open_price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DEC_PLACES)
    close_price = models.DecimalField(max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DEC_PLACES)
    volume = models.DecimalField(max_digits=12, decimal_places=6)
    open_time = models.DateTimeField(default=timezone.now,db_index=True)
    close_time = models.DateTimeField(default=timezone.now)

    def create_from(candle):
        return PairData.objects.create(pair_index=candle.pair_index, open_time=candle.open_time, close_time=candle.close_time,
                                       open_price=candle.open_price, high_price=candle.high_price,
                                       low_price=candle.low_price, close_price=candle.close_price, volume=candle.volume)
        # self.open_time = candle.open_time
        # self.close_time = candle.close_time
        # self.open_price = candle.open_price
        # self.high_price = candle.high_price
        # self.low_price = candle.low_price
        # self.close_price = candle.close_price
        # self.volume = candle.volume

    def __str__(self):
        return "Pair: {0}, low={1}, high={2}, open={3}, close={4}, volume={5}, time: {6} - {7}". \
            format(self.pair_index, self.low_price, self.high_price, self.open_price, self.close_price, self.volume,
                   self.open_time, self.close_time)
