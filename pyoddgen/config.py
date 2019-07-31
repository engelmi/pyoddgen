from os import getcwd
from os.path import join

from pyoddgen.tools.directory import create_directory, create_directories, delete_directory
from pyoddgen.serializable import Serializable
from pyoddgen.tools.distribution import Distribution


class ProjectConfiguration(Serializable):

    def __init__(self):
        self.fields = dict()
        self.fields["base_dir"] = ""
        self.fields["project_dir"] = ""
        self.fields["generator_config"] = None

    def setup_project_directory_structure(self):
        # clean up existing project and re-create it
        delete_directory(self.fields["project_dir"])
        create_directory(self.fields["project_dir"])

    # todo: implement
    def check_validity(self):
        return True, ""


class GeneratorConfiguration(Serializable):

    def __init__(self):
        self.fields = dict()
        self.fields["generator"] = ("", "")

        # directories
        self.fields["generator_dir"] = ""
        self.fields["resource_dir"] = ""
        self.fields["output_dir"] = ""

        # files
        self.fields["generated_data_log_file"] = ""
        self.fields["used_distributions_file"] = ""

        # generation
        self.fields["batch_size"] = -1

        # writer
        self.fields["data_writer"] = ("", "")
        self.fields["data_record_type"] = ("", "")

        # log
        self.fields["generated_data_log_file_enabled"] = None

    def setup_generator_directory(self, project_dir):
        generator_dir = join(project_dir, self.fields["generator_dir"])
        delete_directory(generator_dir, force=True)

        resource_dir = join(project_dir, self.fields["resource_dir"])
        output_dir = join(project_dir, self.fields["output_dir"])
        _, ex = create_directories([resource_dir, output_dir])
        if ex is not None:
            raise Exception(ex)

    # todo: implement
    def check_validity(self):
        return True, ""


class ObjectDetectionConfiguration(GeneratorConfiguration):

    def __init__(self):
        super(ObjectDetectionConfiguration, self).__init__()

        # directories
        self.fields["resource_classes_dir"] = ""
        self.fields["resource_backgrounds_dir"] = ""
        self.fields["output_plain_image_dir"] = ""

        # files
        self.fields["class_weights_file"] = ""
        self.fields["backgrounds_weights_file"] = ""

        # generation
        self.fields["save_generated_plain_images"] = None
        self.fields["final_scale_factor"] = 0
        self.fields["class_distribution_method"] = None
        self.fields["background_distribution_method"] = None
        self.fields["position_distribution_method"] = None
        self.fields["number_of_pastes_per_background_min"] = -1
        self.fields["number_of_pastes_per_background_max"] = -1
        self.fields["distance_between_pastes"] = -1
        self.fields["number_of_pastes_per_background_distribution_method"] = None

    def setup_generator_directory(self, project_dir):
        super(ObjectDetectionConfiguration, self).setup_generator_directory(project_dir)
        resource_classes_dir = join(project_dir, self.fields["resource_classes_dir"])
        resource_backgrounds_dir = join(project_dir, self.fields["resource_backgrounds_dir"])
        output_plain_image_dir = join(project_dir, self.fields["output_plain_image_dir"])
        _, ex = create_directories([resource_classes_dir, resource_backgrounds_dir, output_plain_image_dir])
        if ex is not None:
            raise Exception(ex)

    # todo: implement
    def check_validity(self):
        return True, ""


def create_default_project_config():
    config = ProjectConfiguration()
    config.fields["base_dir"] = getcwd()
    config.fields["project_dir"] = join(config.fields["base_dir"], "project-1")
    config.fields["generator_config"] = create_default_object_detection_config()
    return config


def create_default_generator_config():
    config = GeneratorConfiguration()
    config.fields["generator"] = ("basegen", "BaseGenerator")
    # directories
    config.fields["generator_dir"] = config.fields["generator"][0]
    config.fields["resource_dir"] = join(config.fields["generator_dir"], "resources")
    config.fields["output_dir"] = join(config.fields["generator_dir"], "output")
    # files
    config.fields["generated_data_log_file"] = join(config.fields["generator_dir"], "generated_data_log_file.csv")
    config.fields["used_distributions_file"] = join(config.fields["generator_dir"], "distributions.csv")
    # generation
    config.fields["batch_size"] = 100
    # writer
    config.fields["data_writer"] = ("filewriter.jsonrecordwriter", "JSONRecordWriter")
    config.fields["data_record_type"] = ("basedatarecord", "BaseDataRecord")
    # log
    config.fields["generated_data_log_file_enabled"] = True
    return config


def create_default_object_detection_config():
    config = ObjectDetectionConfiguration()
    config.fields["generator"] = ("objdetgen", "ObjectDetectionGenerator")
    # directories
    config.fields["generator_dir"] = config.fields["generator"][0]
    config.fields["resource_dir"] = join(config.fields["generator_dir"], "resources")
    config.fields["output_dir"] = join(config.fields["generator_dir"], "output")
    config.fields["resource_classes_dir"] = join(config.fields["resource_dir"], "classes")
    config.fields["resource_backgrounds_dir"] = join(config.fields["resource_dir"], "backgrounds")
    config.fields["output_plain_image_dir"] = join(config.fields["output_dir"], "plain_images")
    # files
    config.fields["generated_data_log_file"] = join(config.fields["generator_dir"], "generated_data_log_file.csv")
    config.fields["used_distributions_file"] = join(config.fields["generator_dir"], "distributions.csv")
    config.fields["class_weights_file"] = join(config.fields["resource_classes_dir"], "class_weights.csv")
    config.fields["backgrounds_weights_file"] = join(config.fields["resource_backgrounds_dir"], "class_weights.csv")
    # generation
    config.fields["batch_size"] = 100
    config.fields["save_generated_plain_images"] = True
    config.fields["final_scale_factor"] = 1
    config.fields["class_distribution_method"] = Distribution.Method.UNIFORM
    config.fields["background_distribution_method"] = Distribution.Method.UNIFORM
    config.fields["position_distribution_method"] = Distribution.Method.UNIFORM
    config.fields["number_of_pastes_per_background_min"] = 0
    config.fields["number_of_pastes_per_background_max"] = 15
    config.fields["distance_between_pastes"] = (0, 0)
    config.fields["number_of_pastes_per_background_distribution_method"] = Distribution.Method.UNIFORM
    # writer
    config.fields["data_writer"] = ("filewriter.jsonrecordwriter", "JSONRecordWriter")
    config.fields["data_record_type"] = ("objectdetectionrecord", "ObjectDetectionDataRecord")
    # log
    config.fields["generated_data_log_file_enabled"] = True
    return config
