import sys
import getopt
import time
import os.path
import threading
import queue

from httpLogAnalytics import AnalyticsThread
from httpLogAlarm import AlarmThread
from logEntry import LogEntry
from collections import deque
from httpLogSettings import WAIT_PERIOD_S, ALARM_AVERAGE_PERIOD_S, ALARM_REQUESTS_PER_S, ANALYTICS_UPDATE_S


def follow(f):
    '''Source http://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file'''
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(1/100)
            continue
        yield line


def printUsage():
    print("Usage: %s -i http_access_log" % sys.argv[0])


if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        printUsage()
        sys.exit(2)

    try:
        myopts, args = getopt.getopt(sys.argv[1:], "i:")
    except getopt.GetoptError as e:
        print (str(e))
        printUsage()
        sys.exit(2)

    logFile = ""
    for o, a in myopts:
        if o == '-i':
            logFile = a

    if (not os.path.exists(logFile)):
        print ('Input http-access-log file "%s" does not exist' % (logFile))
        sys.exit(2)

    lock = threading.Lock()
    alarmQueue = deque()
    analyticsQueue = queue.Queue()

    thread1 = AlarmThread(ALARM_REQUESTS_PER_S, ALARM_AVERAGE_PERIOD_S, alarmQueue, lock)
    thread2 = AnalyticsThread(ANALYTICS_UPDATE_S, analyticsQueue, lock)

    thread1.start()
    thread2.start()

    logFile = open(logFile, "r")
    logLines = follow(logFile)
    for line in logLines:
        entry = LogEntry(line)
        lock.acquire()
        analyticsQueue.put(entry)
        alarmQueue.append(entry)
        lock.release()
