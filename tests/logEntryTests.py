import unittest

from logEntry import LogEntry
 
 
class TestLogEntry(unittest.TestCase):
         
    def test_parse_log_1(self):
        line = '188.45.108.168 - - [12/Dec/2015:19:44:09 +0100] "GET /images/stories/raith/almhuette_raith.jpg HTTP/1.1" 200 43300 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; Android 4.4.2; de-at; SAMSUNG GT-I9301I Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36" "-"'
        entry = LogEntry(line)
        self.assertEqual(entry.clientIp,'188.45.108.168')
        self.assertEqual(entry.clientId, '-')
        self.assertEqual(entry.userName, '-')
        self.assertEqual(entry.requestLine, 'GET /images/stories/raith/almhuette_raith.jpg HTTP/1.1')
        self.assertEqual(entry.requestUrl, '/images/stories/raith/almhuette_raith.jpg')
        self.assertEqual(entry.urlSection, '/images/')
        self.assertEqual(entry.statusCode, 200)
        self.assertEqual(entry.sizeBytes, 43300)
        
    def test_parse_log_2(self):
        line = 'hmu4.cs.auckland.ac.nz - - [09/Feb/2016:02:50:20 -0500] "GET /docs/GCDOAR/EnergyStar.html HTTP/1.0" 200 6829'
        entry = LogEntry(line)
        self.assertEqual(entry.clientIp, 'hmu4.cs.auckland.ac.nz')
        self.assertEqual(entry.clientId, '-')
        self.assertEqual(entry.userName, '-')
        self.assertEqual(entry.requestLine, 'GET /docs/GCDOAR/EnergyStar.html HTTP/1.0')
        self.assertEqual(entry.requestUrl, '/docs/GCDOAR/EnergyStar.html')
        self.assertEqual(entry.urlSection, '/docs/')
        self.assertEqual(entry.statusCode, 200)
        self.assertEqual(entry.sizeBytes, 6829)
        
    def test_parse_log_3(self):
        line = '2607:f0d0:1002:0051:0000:0000:0000:0004 - - [23/Jan/2016:15:41:52 +0100] "POST /administrator/index.php HTTP/1.1" 200 "-" "-" "-" "-"'            
        entry = LogEntry(line)
        self.assertEqual(entry.clientIp, '2607:f0d0:1002:0051:0000:0000:0000:0004')
        self.assertEqual(entry.clientId, '-')
        self.assertEqual(entry.userName, '-')
        self.assertEqual(entry.requestLine, 'POST /administrator/index.php HTTP/1.1')
        self.assertEqual(entry.requestUrl, '/administrator/index.php')
        self.assertEqual(entry.urlSection, '/administrator/')
        self.assertEqual(entry.statusCode, 200)
        self.assertEqual(entry.sizeBytes, 0)

if __name__ == '__main__':
    unittest.main()