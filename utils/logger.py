import os, logging,sys,traceback
from logging.handlers import RotatingFileHandler
import logging_json

def createLogger(log_name, log_level, log_dir, log_fname, log_size, log_backup):
    try:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        full_path = "{}/{}".format(log_dir, log_fname)

        handler = RotatingFileHandler(full_path, maxBytes=log_size,backupCount=log_backup)
        formatter = logging_json.JSONFormatter(fields={
            "time": "time",
            "level":"level",
            "thread_name": "threadName",
            "process_name": "processName",
            "message":"message"
        })
        #formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(created).6f %(message)s", datefmt='%Y/%d/%m %H:%M:%S')
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        handler.flush = sys.stdout.flush
        logger.addHandler(handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        console_handler.flush = sys.stdout.flush
        logger.addHandler(console_handler)
    except Exception as e:
        traceback.print_exc()
        print ("Failed to create logger {}".format(str(e)))
    return logger

def readable2Bytes(fileSz):
    currSymbol = fileSz[-1]
    n = int(fileSz[:-1])
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if currSymbol == s:
            value = n*prefix[s]
            return value
    return n

def getLogLevel(level):
    if level=='info':
        return logging.INFO
    else:
        return logging.DEBUG

