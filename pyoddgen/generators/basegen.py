import time
import datetime

from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class BaseGenerator(object):

    def __init__(self):
        pass

    def log_generated_data(self, generated_data_record):
        if not isinstance(generated_data_record, GeneratedDataRecord):
            raise Exception("Generated data record to log must be of type '" + str(generated_data_record) + "'!")
        rows = []
        log_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

