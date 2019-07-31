from os.path import exists


class RecordWriter(object):
    """
    Base class for writing generated data records to file.
    """

    def __init__(self, output_folder, record_name="data"):
        """
        Constructor.
        """
        if not exists(output_folder):
            raise Exception("Output folder '" + output_folder + "' does not exist!")
        self.output_folder = output_folder
        self.record_name = record_name

    def write_data(self, record):
        raise Exception("Method must be implemented!")
