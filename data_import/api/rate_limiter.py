import time
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.interval = 60 / requests_per_minute  # seconds between requests
        self.request_times = deque(maxlen=requests_per_minute)
    
    def wait(self):
        """Wait if necessary to maintain rate limit"""
        now = datetime.now()
        
        # Remove old requests from the queue
        while self.request_times and \
              (now - self.request_times[0]).total_seconds() > 60:
            self.request_times.popleft()
        
        # If we've made the maximum requests in the last minute, wait
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.request_times[0]).total_seconds()
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.request_times.append(now)