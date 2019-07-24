import os
import logging

from pyoddgen.writer.recordwriter import RecordWriter
from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class JSONRecordWriter(RecordWriter):
    """
    Class to write generated data records to a json-like file.
    """

    def __init__(self, output_folder, record_type, record_name="data"):
        """
        Constructor.
        :param output_folder: Output directory for the .record file.
        :param record_name: Output name for the .record file.
        """
        super(JSONRecordWriter, self).__init__(output_folder, record_type)
        self.record_name = record_name
        with open(os.path.join(self.output_folder, self.record_name), "w") as f:
            f.write("[]")
        self.file_handle = open(os.path.join(self.output_folder, self.record_name), "r+")

    def __del__(self):
        """
        Custom Finalizer. Used to close the file handle.
        """
        if self.file_handle is not None:
            try:
                self.file_handle.close()
            except Exception as ex:
                raise Exception("Could not close file handle to '" + self.record_name + "'!", ex)

    def write_data(self, record):
        """
        Writes a record entry to the defined .record file.
        """
        if not isinstance(record, self.record_type):
            raise Exception("Record parameter '" + str(record) + "' must be of type '" + str(type(GeneratedDataRecord)) + "'!")
        try:
            insert_pos = os.fstat(self.file_handle.fileno()).st_size - 1
            self.file_handle.seek(insert_pos)
            self.file_handle.write(record.to_json_record())
            self.file_handle.write("]")
        except Exception as ex:
            logging.error('Error occurred while writing json record: ' + str(ex))
