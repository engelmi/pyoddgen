from pyoddgen.serializable import Serializable


class GeneratedDataRecord(Serializable):
    """
    Generated data record structure.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(GeneratedDataRecord, self).__init__()

    def to_json_record(self):
        """
        Abstract method. Converts the generated data record to serializable json record
        :return: The created, serializable json record.
        """
        raise NotImplementedError("Must be implemented!")

    def to_tf_record(self):
        """
        Abstract method. Converts the generated data record into the .record format used by TensorFlow.
        :return: The created .record object.
        """
        raise NotImplementedError("Must be implemented!")
