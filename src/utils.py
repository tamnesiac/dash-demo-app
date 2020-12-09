import time

def kelvin2celsius(kelvin):
    return kelvin - 273.15

def epoch2time(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))