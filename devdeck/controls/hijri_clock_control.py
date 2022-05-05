import threading
from datetime import datetime
from time import sleep
import math
from devdeck_core.controls.deck_control import DeckControl
from isodate import D_ALT_BAS
from hijri_converter import Hijri, Gregorian


def decimal_time(babylonian_time):
    t = babylonian_time
    t_s = (t.hour * 60 + t.minute) * 60 + t.second
    d_s = 24 * 60 * 60
    ratio = t_s / d_s
    shifted = ratio * 10
    hours = math.floor(shifted)
    minutes = math.floor((shifted - hours) * 100)
    seconds = math.floor((((shifted - hours) * 100) - minutes) * 100)
    return "%s:%s:%s" % (hours, str(minutes).zfill(2), str(seconds).zfill(2))

def hijri_date(gregorian_date):
    d = gregorian_date
    return Gregorian(d.year, d.month, d.day).to_hijri().isoformat()

print(hijri_date(datetime.now().date()))

class HijriClockControl(DeckControl):

    def __init__(self, key_no, **kwargs):
        super().__init__(key_no, **kwargs)
        self.thread = None
        self.running = False

    def initialize(self):
        self.thread = threading.Thread(target=self._update_display)
        self.running = True
        self.thread.start()

    def _update_display(self):
        while self.running is True:
            with self.deck_context() as context:
                now = datetime.now()

                with context.renderer() as r:
                    r.text(decimal_time(now.time()))\
                        .center_horizontally() \
                        .center_vertically(-100) \
                        .font_size(150)\
                        .end()
                    r.text(hijri_date(now.date())) \
                        .center_horizontally() \
                        .center_vertically(100) \
                        .font_size(75) \
                        .end()
            sleep(1)


    def dispose(self):
        self.running = False
        if self.thread:
            self.thread.join()

