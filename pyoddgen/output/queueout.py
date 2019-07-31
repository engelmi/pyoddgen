import logging
from queue import Queue

from pyoddgen.output.recordwriter import RecordWriter


class QueueWriter(RecordWriter):

    def __init__(self, output_folder, record_name="data", queue_size=20):
        """
        Constructor.
        :param queue_size: Size of the in-memory queue for the generated data.
        """
        super(QueueWriter, self).__init__(output_folder, record_name)
        self.data_queue = Queue(maxsize=queue_size)

    def write_data(self, record, blocking=True):
        """

        :param record:
        :param blocking:
        :return:
        """
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
