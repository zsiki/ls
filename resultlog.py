#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: resultlog
    :platform: Linux, Windows
    :synopsis: main module

.. moduleauthor:: Zoltan Siki <siki@agt.bme.hu>
"""
import datetime
import time

from PyQt4.QtCore import QDir, QFile, QIODevice, QTextStream

class ResultLog(object):
    """ File based logging for Surveying Calculations. Events & calculation results are logged into this file.
    """
    resultlog_message = ""
    
    def __init__(self, logfile, repeat_count=3):
        """ initialize log file if the given file cannot be opened for output then a SurveyingCalculation.log file in the temperary directory will be used

            :param logfile: name of the log file it will be created if neccessary, messages will be appended to the end
            :param repeat_count: retry count on fail accessing log file
        """
        self.repeat_count = repeat_count   # retry count for i/o operations
        self.set_log_path(logfile)

    def set_log_path(self, log_path):
        for i in range(self.repeat_count * 2):
            f = QFile( log_path )
            if not f.open(QIODevice.Append | QIODevice.Text):
                f = None
                if i == self.repeat_count:
                    log_path = QDir.temp().absoluteFilePath("SurveyingCalculation.log")
        f.close()
        self.logfile = log_path

    def reset(self):
        """ Delete content of log file
        """
        for i in range(self.repeat_count):
            if QFile(self.logfile).remove():
                break

    def write(self, msg = ""):
        """ Write a  simple message to log

            :param msg: message to write
        """
        for i in range(self.repeat_count):
            f = QFile( self.logfile )
            if not f.open(QIODevice.Append | QIODevice.Text):
                continue
            stream = QTextStream(f)                
            stream << (msg+'\n')
            break
        f.close()

    def write_log(self, msg):
        """ Write log message with date & time

            :param msg: message to write
        """
        d = time.strftime("%Y-%m-%d %H:%M:%S",
            datetime.datetime.now().timetuple())
        self.write(d + " - " + msg)
