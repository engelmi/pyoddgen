import logging
from queue import Queue

from pyoddgen.output.recordwriter import RecordWriter
from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class QueueWriter(RecordWriter):

    def __init__(self, record_type, queue_size=20):
        """
        Constructor.
        :param queue_size: Size of the in-memory queue for the generated data.
        """
        super(QueueWriter, self).__init__(record_type)
        self.data_queue = Queue(maxsize=queue_size)

    def write_data(self, record, blocking=True):
        """

        :param record:
        :param blocking:
        :return:
        """
        if not isinstance(record, self.record_type):
            raise Exception("Record parameter '" + str(record) + "' must be of type '" + str(type(GeneratedDataRecord)) + "'!")
        try:
            self.data_queue.put(record, block=blocking)
        except Exception as ex:
            logging.error('Error occurred while writing record to queue: ' + str(ex))

    def retrieve_data(self, blocking=True):
        """

        :param blocking:
        :return:
        """
        try:
            self.data_queue.get(block=blocking)
        except Exception as ex:
            logging.error('Error occurred while retrieving record from queue: ' + str(ex))
