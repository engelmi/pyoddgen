from os import getcwd
from os.path import join

from pyoddgen.tools.directory import create_directory, create_directories, delete_directory
from pyoddgen.generators.basegen import BaseGenerator
from pyoddgen.generators.objdetgen import ObjectDetectionGenerator
from pyoddgen.datastructures.gendataobjdet import ObjectDetectionDataRecord
from pyoddgen.output.jsonrecordwriter import JSONRecordWriter
from pyoddgen.serializable import Serializable
from pyoddgen.tools.distribution import Distribution


class ProjectConfiguration(Serializable):

    def __init__(self):
        self.base_dir = getcwd()
        self.project_dir = join(self.base_dir, "project-1")
        self.generator_config_list = []

    def setup_project_directory_structure(self):
        # clean up existing project and re-create it
        delete_directory(self.project_dir)
        create_directory(self.project_dir)

    def setup_generator_directory_structures(self):
        for generator in self.generator_config_list:
            generator.setup_generator_directory(self.project_dir)

    # todo: implement
    def is_valid(self):
        return True


class GeneratorConfiguration(Serializable):

    def __init__(self):
        self.generator_class = BaseGenerator
        self.generator_name = "sample-base-generator"

        # directories
        self.generator_dir = self.generator_name
        self.resource_dir = join(self.generator_dir, "resources")
        self.output_dir = join(self.generator_dir, "output")

        # files
        self.generated_data_log = join(self.generator_dir, "generated_data_log.csv")
        self.used_distributions_file = join(self.generator_dir, "distributions.csv")

        # generation
        self.batch_size = 100

        # writer
        self.data_writer = JSONRecordWriter
        self.data_record_type = ObjectDetectionDataRecord

        # log
        self.generated_data_log_enabled = True

    def setup_generator_directory(self, project_dir):
        generator_dir = join(project_dir, self.generator_dir)
        _, ex = delete_directory(generator_dir)
        if ex is not None:
            raise Exception("Error on deleting directory '" + generator_dir + "'!", ex)

        resource_dir = join(project_dir, self.config.resource_dir)
        output_dir = join(project_dir, self.config.output_dir)
        _, ex = create_directories([resource_dir, output_dir])
        if ex is not None:
            raise Exception(ex)

    # todo: implement
    def is_valid(self):
        return True


class ObjectDetectionConfiguration(GeneratorConfiguration):

    def __init__(self):
        self.generator_class = ObjectDetectionGenerator
        self.generator_name = "sample-objdet-generator"

        # directories
        self.resource_classes_dir = join(self.resource_dir, "classes")
        self.resource_backgrounds_dir = join(self.resource_dir, "backgrounds")
        self.output_plain_image_dir = join(self.output_dir, "plain_images")

        # files
        self.classes_weights_file = join(self.resource_classes_dir, "class_weights.csv")
        self.backgrounds_weights_file = join(self.resource_backgrounds_dir, "class_weights.csv")

        # generation
        self.save_generated_plain_images = True
        self.final_scale_factor = 1
        self.class_distribution_method = Distribution.Method.UNIFORM
        self.background_distribution_method = Distribution.Method.UNIFORM
        self.position_distribution_method = Distribution.Method.UNIFORM
        self.number_of_pastes_per_background_min = 0
        self.number_of_pastes_per_background_max = 15
        self.distance_between_pastes = (0, 0)
        self.number_of_pastes_per_background_distribution_method = Distribution.Method.UNIFORM

    def setup_generator_directory(self, project_dir):
        super(ObjectDetectionConfiguration, self).setup_generator_directory(project_dir)
        resource_classes_dir = join(project_dir, self.resource_classes_dir)
        resource_backgrounds_dir = join(project_dir, self.resource_backgrounds_dir)
        output_plain_image_dir = join(project_dir, self.output_plain_image_dir)
        _, ex = create_directories([resource_classes_dir, resource_backgrounds_dir, output_plain_image_dir])
        if ex is not None:
            raise Exception(ex)

    # todo: implement
    def is_valid(self):
        return True
