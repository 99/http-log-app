import sys
import getopt
import random
import os.path

from datetime import datetime, timezone
from logEntry import LogEntry
#from httpLogApp.httpLogMonitor import LogEntry


def printUsage():
    print("Usage: %s -i access_log_input -o access_log_output -c entries" % sys.argv[0])

def generateLogEntry():
    line = '188.127.233.220 - - [22/Jan/2016:09:35:54 +0100] "GET /almhuette-raith.at.tgz HTTP/1.1" 200 228'
    entry = LogEntry(line)
    now = datetime.now(timezone.utc)
    entry.timeStamp = now.astimezone()
    return entry

def getRandomLogEntry(fileName):
    line = random.choice(open(fileName).readlines())
    entry = LogEntry(line)
    now = datetime.now(timezone.utc)
    entry.timeStamp = now.astimezone()
    return entry


def writeRandomLogEntries(inFileName, outFileName, entryCount):
    count = entryCount
    while (count > 0):
        e = getRandomLogEntry(inFile)
        print (str(e))
        with open(outFile, 'a+') as outLog:
            outLog.write("".join([str(e), '\n']))
        count -= 1


if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        printUsage()
        sys.exit(2)

    try:
        myopts, args = getopt.getopt(sys.argv[1:], "o:i:c:")
    except getopt.GetoptError as e:
        print (str(e))
        printUsage()
        sys.exit(2)

    inFile = None
    outFile = None
    eCount = 1

    for o, a in myopts:
        if o == '-o':
            outFile = a
        elif o == '-i':
            inFile = a
        elif o == '-c':
            eCount = int(a)

    if (not os.path.exists(inFile)):
        print('Input access_log_input file: %s does not exist' % (inFile))
        sys.exit(2)

    writeRandomLogEntries(inFile, outFile, eCount)
