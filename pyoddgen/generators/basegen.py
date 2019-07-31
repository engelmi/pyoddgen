import os

from pyoddgen.tools.csvfile import CSVFile
from pyoddgen.config import GeneratorConfiguration
from pyoddgen.tools.directory import import_on_runtime


class BaseGenerator(object):

    def __init__(self, config, project_dir):
        if not isinstance(config, GeneratorConfiguration):
            raise Exception("Configuration for generator must be of type '" + str(GeneratorConfiguration) + "'! "
                            "Got '" + str(type(config)) + "' instead. ")
        ret, msg = config.check_validity()
        if not ret:
            raise Exception("Invalid generator config: " + msg)
        if not os.path.exists(project_dir):
            raise Exception("Project directory '" + project_dir + "' does not exist or is invalid!")
        self.project_dir = project_dir
        self.config = config
        self.data_id = 0
        self.csv_log_file = None
        if self.config.fields["generated_data_log_file_enabled"]:
            self.csv_log_file = CSVFile(os.path.join(self.project_dir, self.config.fields["generated_data_log_file"]))
            self.csv_log_file.write_rows([self.get_log_header()], append=False)
        self.data_writer = self.setup_configured_data_writer()
        self.data_record_type = self.setup_configured_data_record_type()

    def setup_configured_data_writer(self):
        data_writer_module_import = "pyoddgen.output." + self.config.fields["data_writer"][0]
        data_writer_class_import = self.config.fields["data_writer"][1]
        data_writer_class = import_on_runtime(data_writer_module_import, data_writer_class_import)
        return data_writer_class(os.path.join(self.project_dir, self.config.fields["output_dir"]))

    def setup_configured_data_record_type(self):
        record_type_module_import = "pyoddgen.datastructures." + self.config.fields["data_record_type"][0]
        record_type_class_import = self.config.fields["data_record_type"][1]
        return import_on_runtime(record_type_module_import, record_type_class_import)

    def get_log_header(self):
        raise NotImplementedError("Method must be implemented!")

    def log_generated_data(self, generated_data_record):
        raise NotImplementedError("Method must be implemented!")

    def generate_next(self):
        raise NotImplementedError("Method must be implemented!")

    def generate_next_n(self, n):
        for _ in range(n):
            self.generate_next()

    def next_data_id(self):
        self.data_id += 1
        return self.data_id

    def write_generated_data(self, generated_data):
        self.data_writer.write_data(generated_data)


