import csv


class CSVFile(object):
    """
    CSV file representation to easily write to and read from csv files.
    """

    def __init__(self, file):
        """
        Constructor.
        """
        self.delimiter = ";"
        self.quotechar = "'"
        self.lineterminator = "\n"
        self.file = file

    def write_rows(self, rows, append=True):
        """
        Writes the rows to the linked csv file.
        :param rows: The rows to write to file.
        :param append: Appends the rows to the linked file if True. Otherwise, the file gets overwritten.
        """
        openmode = "a"
        if not append:
            openmode = "w"
        with open(self.file, openmode) as cls2lblfile:
            csvwriter = csv.writer(cls2lblfile, delimiter=self.delimiter, quotechar=self.quotechar, lineterminator=self.lineterminator)
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
