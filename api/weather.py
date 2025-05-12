from datetime import date

class Weather:
    date = date.today()
    day_weather = ""
    night_weather = ""
    high_temperature = 0
    low_temperature = 0

    def __init__(self,d,d_w,n_w,h_t,l_t):
        self.date=d
        self.day_weather=d_w
        self.night_weather=n_w
        self.high_temperature=h_t
        self.low_temperature=l_t
