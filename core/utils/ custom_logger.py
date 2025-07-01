import sys
import json
import logging
from datetime import datetime, timezone
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            
            log_record["timestamp"]= datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


logger = logging.getLogger(__name__)

# stream_formatter=logging.Formatter('%(asctime)-15s | %(levelname)-8s | %(message)s')
log_formatter=CustomJsonFormatter('%(timestamp)s | %(level)s | %(name)s | %(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("tango.log")

stream_handler.setFormatter(log_formatter)
file_handler.setFormatter(log_formatter)

logger.setLevel(logging.DEBUG)
logger.handlers = [
    stream_handler, 
    # file_handler
    ]
