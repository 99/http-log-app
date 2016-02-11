import threading
import time

from collections import Counter
from httpLogSettings import WAIT_PERIOD_S


class AnalyticsThread(threading.Thread):
    '''Background thread to record and aggregate statistics about requests'''
    def __init__(self, updatePeriod, q, lock):
        threading.Thread.__init__(self)
        self.updatePeriod = updatePeriod
        self.q = q
        self.lock = lock
        self.overallBytes = 0
        self.overallRequests = 0
        self.sectionsCount = Counter()

    def addEntry(self, entry):
        self.overallBytes += entry.sizeBytes
        self.overallRequests += 1
        self.sectionsCount[entry.urlSection] += 1

    def printStatistics(self):
        print ("\n*********************************")
        print ("Overall Requests Counted = %d" % self.overallRequests)
        print ("Overall Bytes Downloaded = %d" % self.overallBytes)
        print ("Top 3 Sections:")
        print (self.sectionsCount.most_common(3))
        print ("*********************************\n")

    def run(self):
        count = self.updatePeriod
        while(True):
            self.lock.acquire()
            if (not self.q.empty()):
                entry = self.q.get()
                self.lock.release()
                self.addEntry(entry)
            else:
                self.lock.release()
                time.sleep(WAIT_PERIOD_S)
                count -= WAIT_PERIOD_S

            if (count == 0):
                count = self.updatePeriod
                self.printStatistics()
