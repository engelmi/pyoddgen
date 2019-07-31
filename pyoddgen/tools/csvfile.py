import csv


class CSVFile(object):
    """
    CSV file representation to easily write to and read from csv files.
    """

    def __init__(self, file):
        """
        Constructor.
        """
        self.file = file
        self.delimiter = ";"
        self.quotechar = "'"
        self.lineterminator = "\n"

    def write_rows(self, rows, append=True):
        """
        Writes the rows to the linked csv file.
        :param rows: The rows to write to file.
        :param append: Appends the rows to the linked file if True. Otherwise, the file gets overwritten.
        """
        mode = "a"
        if not append:
            mode = "w"
        with open(self.file, mode) as f:
            csvwriter = csv.writer(f, delimiter=self.delimiter, quotechar=self.quotechar, lineterminator=self.lineterminator)
            for row in rows:
                csvwriter.writerow(row)

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
