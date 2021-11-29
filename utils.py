def time_cache(method):
    cached_res = None
    last_time = None
    def wrapper(self):
        if (last_time is None) or (self.time != last_time):
            res = method(self)
            cached_res = res
            last_time = self.time
            return res
        else:
            return cached_res
    return wrapper