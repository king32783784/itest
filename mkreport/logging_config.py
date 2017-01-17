import logging, logging.handlers
import sys
from subprocess import Popen, PIPE
 

class Logging_Config():
    @staticmethod
    def setlogger(loggername, logfile):
        # create logger with 'loggername'
        logger = logging.getLogger('%s' % loggername)
        # set logger Level DEBUG
        logger.setLevel(logging.DEBUG)
        #create file handler which logs even debug messages
        fh = logging.FileHandler('%s' % logfile)
        # set FileHandler Level DEBUG
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level 
        ch = logging.StreamHandler()
        # set console handeler Level ERROR
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # set FileHandler format
        fh.setFormatter(formatter)
        # set console formatter
        ch.setFormatter(formatter)
        # add the handler to the logger
        logger.addHandler(fh)
 #       logger.addHandler(ch)


class StreamToLogger():
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.DEBUG):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

#Logging_Config.setlogger('Perfcpu', 'perfcpu.log')
#stdout_logger = logging.getLogger('Perfcpu')
#sl = StreamToLogger(stdout_logger, logging.INFO)
#sys.stdout = sl

#stderr_logger = logging.getLogger('Perfcpu')
#sl = StreamToLogger(stderr_logger, logging.ERROR)
#sys.stderr = sl

#test = Popen(["dmesg"], stdout=PIPE)
#print test.communicate()[0]
#print stdout
