import csv
from enum import Enum


class CSVFile(object):
    """
    CSV file representation to easily write to and read from csv files.
    """

    class Variant(Enum):
        NONE = (0, None)
        LOG = (1, ["timestamp", "generated_data_id", "background_id", "background_width", "background_height", "class_id", "xmin", "ymin", "xmax", "ymax"])
        CLASSES = (1, ["id", "class_id", "image_file", "weight"])
        BACKGROUNDS = (1, ["id", "background_id", "image_file", "weight"])
        DISTRIBUTIONS = (1, ["id", "group", "distribution"])

    def __init__(self, file, variant=Variant.NONE):
        """
        Constructor.
        """
        if not isinstance(variant, CSVFile.Variant):
            raise Exception("Variant must be of type '" + str(CSVFile.Variant) + "'! Got '" + str(type(variant)) + "' instead.")
        self.variant = variant
        self.columns = variant.value[1]
        self.file = file
        self.delimiter = ";"
        self.quotechar = "'"
        self.lineterminator = "\n"

    def write_rows(self, rows, append=True):
        """
        Writes the rows to the linked csv file.
        :param rows: The rows to write to file.
        :param append: Appends the rows to the linked file if True. Otherwise, the file gets overwritten.
        :return: Number of rows written to file.
        """
        openmode = "a"
        if not append:
            openmode = "w"
        num_written_lines = 0
        with open(self.file, openmode) as cls2lblfile:
            csvwriter = csv.writer(cls2lblfile, delimiter=self.delimiter, quotechar=self.quotechar, lineterminator=self.lineterminator)
            if self.variant == CSVFile.Variant.NONE:
                for row in rows:
                    csvwriter.writerow(row)
                    num_written_lines += 1
            else:
                for row in rows:
                    if len(row) == len(self.columns):
                        csvwriter.writerow(row)
                        num_written_lines += 1
        return num_written_lines

    def read_rows(self):
        """
        Reads all rows from the linked csv file.
        :return: List of all rows (not parsed or processed).
        """
        rows = []
        with open(self.file, "r") as cls2lblfile:
            csvreader = csv.reader(cls2lblfile, delimiter=self.delimiter, quotechar=self.quotechar, lineterminator=self.lineterminator)
            for row in csvreader:
                rows.append(row)
        return rows
