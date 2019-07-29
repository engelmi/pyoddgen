import logging
import tensorflow as tf
from os.path import join, exists

from pyoddgen.output.recordwriter import RecordWriter
from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class TFRecordWriter(RecordWriter):
    """
    Class to write generated data records to a TensorFlow .record file.
    """

    def __init__(self, output_folder, record_type, record_name="data"):
        """
        Constructor.
        :param output_folder: Output directory for the .record file.
        :param record_name: Output name for the .record file.
        """
        super(TFRecordWriter, self).__init__(record_type)
        if not exists(output_folder):
            raise Exception("Output folder does not exist!")
        self.output_folder = output_folder
        self.record_name = record_name
        self.tf_writer = tf.python_io.TFRecordWriter(join(output_folder, record_name + '.record'))

    def write_data(self, record):
        """
        Writes a record entry to the defined .record file.
        """
        if not isinstance(record, self.record_type):
            raise Exception("Record parameter '" + str(record) + "' must be of type '" + str(type(GeneratedDataRecord)) + "'!")
        try:
            self.tf_writer.write(record.to_tf_record().SerializeToString())
        except Exception as e:
            logging.error('Error occurred while writing tf record: ' + str(e))

    def __del__(self):
        if hasattr(self, "tf_writer") and self.tf_writer is not None:
            try:
                self.tf_writer.close()
            except Exception as e:
                logging.error("Exception while closing TFRecordWriter: " + str(e))
