import logging, os, datetime,threading,pytz,traceback
from django.conf import settings

logger = logging.getLogger("reader")

def log(request,_id, req, res, err):
    try:
        tz = pytz.timezone(settings.TIME_ZONE)
        message = {"method": request.method,  "user": request.user.__str__(), \
            "ID":_id ,"request" :str(req), "response": str(res), "host":request.get_host(),  "path":request.path, "error":err}
        pid = os.getpid()
        thread = threading.get_ident()
        log_dict = {}
        now = datetime.datetime.now(tz = tz)
        if err:
            logger.error({"time": now,
                "level":"ERROR",
                "thread_name": thread,
                "process_name": pid,
                "message":message})
        else:
            logger.info({"time": now,
                    "level":"INFO",
                    "thread_name": thread,
                    "process_name": pid,
                    "message":message})
    except Exception as ex:
        logger.critical({"time": datetime.datetime.now(),
                    "level":"CRITICAL",
                    "thread_name": threading.get_ident(),
                    "process_name": os.getpid(),
                    "message":f"Unable to log: {traceback.format_exc()}"})

            