#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Result log for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""
import os
import tempfile
import datetime
import time

class ResultLog(object):
    """
        File based logging for Surveying Calculations
        Events & calculation results are logged into this file
    """
    resultlog_lessage = ""
    
    def __init__(self, logfile):
        """ initialize log file if neccessary
            :param logfile: name of the log file it will be created if neccessary, messages are appended to the end
        """
        try:
            f = open(logfile, "a")
        except(IOError):
            logfile = os.path.join(tempfile.gettempdir(), "SurveyingCalculation.log")
            f = open(logfile, "a")
        f.close()
        self.logfile = logfile

    def reset(self):
        """
            Delete log file
        """
        try:
            os.remove(self.logfile)
        except(OSError):
            pass

    def write(self, msg = ""):
        """
            Write simple message to log
            :param msg: message to write
        """
        try:
            f = open(self.logfile, "a")
        except (IOError):
            return
        try:
            f.write(msg + '\n')
        except (IOError):
            f.close()
            return
        try:
            f.close()
        except (IOError):
            pass

    def write_log(self, msg):
        """
            Write log message with date & time
            :param msg: message to write
        """
        d = time.strftime("%Y-%m-%d %H:%M:%S",
            datetime.datetime.now().timetuple())
        self.write(d + " - " + msg)
        