from timeit import default_timer as timer

Infinity = 10000
NoMove = [0, 0, -1]


class CheckAbort:
    def __init__(self, avail_time):
        self._avail_time = avail_time
        self._start_time = timer()

    def do_abort(self):
        if self._avail_time == 0:
            return False
        return timer() - self._start_time >= self._avail_time
