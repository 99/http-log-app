# HTTP log monitoring console program

* Create a simple console program that monitors HTTP traffic on your machine:

* Consume an actively written-to w3c-formatted HTTP access log

* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what's before the second '/' in a URL. i.e. the section for "http://my.site.com/pages/create' is "http://my.site.com/pages"), as well as interesting summary statistics on the traffic as a whole.

* Make sure a user can keep the console app running and monitor traffic on their machine

* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”

* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered

* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.

* Write a test for the alerting logic

* Explain how you’d improve on this application design

## Setup

Tested with Python 3.5. Works best if setup within a virtualenv.

```shell
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
```
## Running

Main python files are httpLogMonitor.py and httpLogGenerator.py. They can be run directly from the command line but for your convenience a couple of helper shell scripts are included.

```shell
$ ./generate_log.sh -> creates one log in the local access.log file
$ ./run_monitor.sh -> monitors the access.log file and prints out analytics and alarms
$ ./run_tests.sh -> runs tests
```


## Improvements

* Statistics could aggregate data by ip/user and give a better estimate of unique visitors and unique page counts
* Instead of simply showing the data in a console/terminal, the daemon could upload the information to an API that stores the information and makes it accessible from anywhere
* The application could be daemonized and be made to run on computer startup
