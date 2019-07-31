from pyoddgen.serializable import Serializable


class GeneratedDataRecord(Serializable):
    """
    Generated data record structure.
    """

    mandatory_fields = ["data_id"]

    def __init__(self, data_dict):
        """
        Constructor.
        :param data_dict: Dictionary containing the data of an object detection record.
        """
        super(GeneratedDataRecord, self).__init__()
        self.data_dict = data_dict

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

    def check_validity(self):
        if self.data_dict is None:
            return False, "data_dict must not be None!"
        if not isinstance(self.data_dict, dict):
            return False, "data_dict must be of type dict!"
        return True, ""
