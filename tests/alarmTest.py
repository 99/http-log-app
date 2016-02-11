import unittest
import threading
import time
import sys

from logEntry import LogEntry
from httpLogGenerator import generateLogEntry
from collections import deque
from httpLogAlarm import AlarmThread
from io import StringIO


class TestAlarmThread(unittest.TestCase):
    """Setups an alarm thread and changes the average window of traffic to be only 5 seconds. Generates
        5 log entries and registers them as hits by putting them on the alarmQueue. The output of the 
        thread is redirected into a StringIO and that is checked to verify that the alarm message was 
        properly written"""
        
    def test_alert_1(self):
        out = StringIO()
        lock = threading.Lock()
        alarmQueue = deque()
        reqPerSec = 0.5;
        alarmPeriodSec = 5;
        
        thread1 = AlarmThread(reqPerSec, alarmPeriodSec, alarmQueue, lock, out=out)
        thread1.start()        
        
        time.sleep(1)
        
        for _ in range(alarmPeriodSec):
            entry = generateLogEntry()
            lock.acquire()
            alarmQueue.append(entry)
            lock.release()
                
        time.sleep(alarmPeriodSec * 2)
        
        output = out.getvalue()
        lines = output.split('\n')
        
        self.assertTrue("High traffic generated an alert" in lines[0]) 
        self.assertTrue("High traffic alert recovered" in lines[1]) 
        
if __name__ == '__main__':
    unittest.main()