import re
from datetime import datetime

# logEntry = 'hmu4.cs.auckland.ac.nz [29:23:57:35] "GET /docs/GCDOAR/EnergyStar.html HTTP/1.0" 200 6829'


DATE_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


class LogEntry:
    '''Class to parse and represent a single line in an HTTP access log'''

    def __init__(self, logString):
        self.rawString = logString
        logArr = list(map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', logString)))

        self.clientIp = logArr[0]
        self.clientId = logArr[1]
        self.userName = logArr[2]
        self.timeStamp = datetime.strptime(logArr[3], DATE_FORMAT)
        self.requestLine = logArr[4]

        self.requestUrl = self.requestLine.split()[1]

        if (self.requestUrl == "/"):
            self.urlSection = self.requestUrl
        else:
            tokens = self.requestUrl.split('/')
            self.urlSection = "".join(['/', tokens[1], '/'])

        self.statusCode = num(logArr[5])
        self.sizeBytes = num(logArr[6])

        if (len(logArr) == 9):
            self.referer = logArr[7]
            self.userAgent = logArr[8]

    def __str__(self):
        return " ".join([self.clientIp,
                         self.clientId,
                         self.userName,
                         "".join(['[', self.timeStamp.strftime(DATE_FORMAT), ']']),
                         "".join(['"', self.requestLine, '"']),
                         str(self.statusCode),
                         str(self.sizeBytes)
                        ])


def num(s):
    if (s.isdigit()):
        try:
            return int(s)
        except ValueError:
            return float(s)
    else:
        return 0
