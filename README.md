# Multilog

Inspired by https://github.com/acschaefer/duallog
Contains quite a lot of modifications though

This module contains a class "setup" that sets up dual (or triple) logging.
All log messages are sent to both the console and a logfile, and possibly a seperate debug-file

Log messages are generated via the "logging" package.

Example 1:
```
    >>> import multilog
    >>> logging = multilog.setup()
    >>> logging.info('Test message')
    >>> logging.warning('Test warning')
```
This will log "Test message" and "Test warning" to the file "log/multilog.log" and "Test warning" to the console
If this is run from a python script, the log file will by default be named log/<script name>.log

- Log levels for both console and file logging can be set on init
```
import logging
import multilog

logging = multilog.setup(minLevel=logging.INFO, fileLevel=logging.DEBUG)
```
- This will cause any log with level INFO and higher to be logged to the console
- Also, any log with level INFO and higher is logged to "log/<script name>.log"
- DEBUG-messages (and higher) goes to "log/<script name>-debug.log"



