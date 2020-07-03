#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Multilog

Inspired by https://github.com/acschaefer/duallog
Contains quite a lot of modifications though

This module contains a class "setup" that sets up dual (or triple) logging.
All log messages are sent to both the console and a logfile, and possibly a seperate debug-file

Log messages are generated via the "logging" package.

Example 1:
    >>> import multilog
    >>> logging = multilog.setup()
    >>> logging.info('Test message')
    >>> logging.warning('Test warning')

This will log "Test message" and "Test warning" to the file "log/multilog.log" and "Test warning" to the console
If this is run from a python script, the log file will by default be named log/<script name>.log

- Log levels for both console and file logging can be set on init

import logging
import multilog

logging = multilog.setup(minLevel=logging.INFO, fileLevel=logging.DEBUG)

- This will cause any log with level INFO and higher to be logged to the console
- Also, any log with level INFO and higher is logged to "log/<script name>.log"
- DEBUG-messages (and higher) goes to "log/<script name>-debug.log"


"""



import os
import sys
import logging
import logging.handlers

from datetime import datetime




class setup():
    def __init__(self, name=None, logDir='log', logFile=None, minLevel=logging.WARNING, rotation='size', keep=10, fileLevel=logging.INFO, maxBytes=(1024*1024)):
        self.script_name = os.path.basename(sys.argv[0])
        self.file_msg_format    = '%(asctime)s %(levelname)-8s: %(message)s'
        self.console_msg_format = '%(asctime)s %(levelname)-8s: %(message)s'

        # Validate the given directory.
        self.log_dir = os.path.normpath(logDir)

        if name:
            self.log_id = name
        elif logFile:
            self.log_id = logFile
        else:
            self.log_id = os.path.splitext(self.script_name)[0]
        if self.log_id is None:
            self.log_id = "multilog"

        self.file_name_format = '{}.log'.format(self.log_id)
        self.debug_name_format = "{}-debug.log".format(self.log_id)
        self.file_log_level = fileLevel
        self.console_log_level = minLevel
        self.rotation = rotation
        self.max_bytes = maxBytes

        self.keep_log_files = keep
        self.keep_debug_files = 2

        self.debug_name = None
        self.file_name = None

        self.log_start_time = datetime.now()

        self.logger = None
        self.start_logger()



    def start_logger(self):
        self.logger = logging.getLogger(self.log_id)
        if len(self.logger.handlers) == 0:
            self.setup_logger()
            self.info('Logging to console with level {}'.format(self.console_log_level))
            self.info('Logging to file {}'.format(self.file_name))
            self.info('Debug to file {}'.format(self.debug_name))
            self.info('--------------------------------------')
            self.info('        Starter {}'.format(self.script_name))
            self.info('        {}'.format(self.log_start_time))
            self.info('--------------------------------------')


    def setup_logger(self):
        self.logger.setLevel(logging.DEBUG)

        # Create a folder for the logfiles.
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Set up special debug-file if needed
        # We just keep a few of these, and rotate them at midnight
        # And we dont want to clutter the regular logs with debug info
        if self.file_log_level < logging.INFO:
            self.debug_name = os.path.join(self.log_dir, self.debug_name_format)
            debug_handler = logging.handlers.TimedRotatingFileHandler(filename=self.debug_name, when='midnight', backupCount=self.keep_debug_files)
            debug_handler.setLevel(logging.DEBUG)

            debug_formatter = logging.Formatter(self.file_msg_format)
            debug_handler.setFormatter(debug_formatter)
            self.logger.addHandler(debug_handler)
            self.file_log_level = logging.INFO

        self.file_name = os.path.join(self.log_dir, self.file_name_format)
        # Set up logging to the logfile.
        if self.rotation == 'daily':
            file_handler = logging.handlers.TimedRotatingFileHandler(filename=self.file_name, when='midnight', backupCount=self.keep_log_files)
        elif self.rotation == 'hourly':
            file_handler = logging.handlers.TimedRotatingFileHandler(filename=self.file_name, when='H', backupCount=self.keep_log_files)
        else:
            file_handler = logging.handlers.RotatingFileHandler(filename=self.file_name, maxBytes=self.max_bytes, backupCount=self.keep_log_files)

        file_handler.setLevel(self.file_log_level)
        file_formatter = logging.Formatter(self.file_msg_format)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Set up logging to the console.
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.console_log_level)
        stream_formatter = logging.Formatter(self.console_msg_format)
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)


    def debug(self, string):
        self.logger.debug(string)

    def info(self, string):
        self.logger.info(string)

    def warning(self, string):
        self.logger.warning(self._orange(string))

    def error(self, string):
        self.logger.error(self._red(string))

    def critical(self, string):
        self.logger.critical(self._redbg(string))

    def important(self, string):
        self.logger.info(self._bold(string))




    def _bold(self, s):
        return "\033[1m{}\033[0m".format(s)

    def _red(self, s):
        return "\033[91m{}\033[0m".format(s)

    def _green(self, s):
        return "\033[92m{}\033[0m".format(s)

    def _orange(self, s):
        return "\033[93m{}\033[0m".format(s)

    def _cyan(self, s):
        return "\033[96m{}\033[0m".format(s)

    def _redbg(self, s):
        return "\033[101m{}\033[0m".format(s)


