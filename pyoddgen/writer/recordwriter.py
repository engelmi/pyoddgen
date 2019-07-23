from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class RecordWriter(object):
    """
    Base class for writing generated data records to file.
    """

    def __init__(self, output_folder, record_type):
        """
        Constructor.
        :param output_folder: Output directory for the .record file.
        """
        if not issubclass(record_type, GeneratedDataRecord):
            raise Exception("Record type must be a class inheriting '" + str(GeneratedDataRecord) + "'!")
        self.output_folder = output_folder
        self.record_type = record_type

    def write_data(self, record):
        raise Exception("Method must be implemented!")
