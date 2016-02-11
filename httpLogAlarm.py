import threading
import time
import sys


from collections import deque
from datetime import datetime, timezone
from httpLogSettings import WAIT_PERIOD_S


class AlarmThread (threading.Thread):
    '''Background thread to cache recent results and alert if over a threshold for an average time'''
    def __init__(self, threshold, period, q, lock, out=sys.stdout):
        threading.Thread.__init__(self)
        self.threshold = threshold
        self.period = period
        self.q = q
        self.lock = lock
        self.out = out

    def run(self):
        process_alarm(self.threshold, self.period, self.q, self.lock, self.out)


def process_alarm(threshold, period, q, lock, out):
    alarm = False

    while(True):
        lock.acquire()
        cachedCount = len(q)

        if (alarm is False and (cachedCount/period) > threshold):
            alarm = True
            out.write('High traffic generated an alert - hits = %d, triggered at %s\n' % (cachedCount, str(datetime.now())))
            lock.release()
        elif (alarm is True and (cachedCount/period) < threshold):
            alarm = False
            out.write('High traffic alert recovered at %s\n' % (str(datetime.now())))
            lock.release()
        elif (cachedCount > 0):
            entry = q.popleft()
            delta = datetime.now(timezone.utc) - entry.timeStamp

            if (delta.total_seconds() > period):
                # print ("%s: Queue size = %s" % (threadName, len(q)))
                lock.release()
            else:
                q.appendleft(entry)
                lock.release()
                # print ("%s: Queue size = %s" % (threadName, len(q)))
                time.sleep(WAIT_PERIOD_S)
        else:
            lock.release()
            time.sleep(WAIT_PERIOD_S)
