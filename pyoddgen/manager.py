from pyoddgen.tools.directory import import_on_runtime
from pyoddgen.config import ProjectConfiguration, GeneratorConfiguration


class GeneratorManager(object):

    def __init__(self, project_config):
        if not isinstance(project_config, ProjectConfiguration):
            raise Exception("Configuration of project must be of type '" + str(ProjectConfiguration) + "'! Got '" + str(type(project_config)) + "' instead.")
        is_valid, msg = project_config.check_validity()
        if not is_valid:
            raise Exception("Project configuration is not valid: " + msg)
        self.project_config = project_config
        self.project_config.setup_project_directory_structure()

        self.generator_config = self.project_config.fields["generator_config"]
        if not isinstance(self.generator_config, GeneratorConfiguration):
            raise Exception("Configuration of generator must be of type '" + str(ProjectConfiguration) + "'! Got '" + str(type(self.generator_config)) + "' instead.")
        self.generator_config.setup_generator_directory(self.project_config.fields["project_dir"])
        self.generator = self.setup_project_generator()

    def setup_project_generator(self):
        if isinstance(self.generator_config, GeneratorConfiguration):
            generator_module_import = "pyoddgen.generators." + self.generator_config.fields["generator"][0]
            generator_class_import = self.generator_config.fields["generator"][1]
            generator_class = import_on_runtime(generator_module_import, generator_class_import)
            return generator_class(self.generator_config, self.project_config.fields["project_dir"])
        return None

    def start_generation(self):
        print("starting generation...")

        print("end of generation")
