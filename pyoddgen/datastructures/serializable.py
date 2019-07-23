import json
import jsonpickle
from os.path import isfile


class Serializable(object):
    """
    Serializable object.
    """

    def __init__(self):
        """
        Empty Constructor.
        """
        pass

    def write_to_file(self, filename, override=False):
        """
        Writes the current serializable object to file.
        :param filename: Name of the target file.
        :param override: Overwrites a colliding file if True, else an exception is thrown on file name collision.
        """
        if isfile(filename) and not override:
            raise NotADirectoryError("File '" + filename + "' already exists!")
        with open(filename, "w") as f:
            json.dump(jsonpickle.encode(self), f)

    @classmethod
    def read_from_file(cls, path_to_file):
        """
        Reads a serialized object from file.
        :param path_to_file: Path to the serialized file to read.
        :return: The reconstructed object.
        """
        if not isfile(path_to_file):
            raise FileNotFoundError("Couldn't find file '" + path_to_file + "'")
        with open(path_to_file, "rb") as f:
            read_detectable = jsonpickle.decode(json.load(f))
        return read_detectable

    def to_json_str(self):
        """
        Converts the current object into a json-like string.
        :return: JSON-like String of the current object.
        """
        return jsonpickle.encode(self)

    def to_json_dict(self):
        """
        Converts the current object into a json-like dict object.
        :return: JSON-like dict of the current object.
        """
        return json.loads(self.to_json_str())
