from os import getcwd
from os.path import join

from pyoddgen.generators.basegen import BaseGenerator
from pyoddgen.generators.objdetgen import ObjectDetectionGenerator
from pyoddgen.datastructures.gendataobjdet import ObjectDetectionDataRecord
from pyoddgen.output.filewriter.jsonrecordwriter import JSONRecordWriter
from pyoddgen.serializable import Serializable
from pyoddgen.tools.distribution import Distribution


class ProjectConfiguration(Serializable):

    def __init__(self):
        self.base_dir = getcwd()
        self.project_dir = join(self.base_dir, "project-1")
        self.generator_config_list = []

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
        self.number_of_pastes_per_background_distribution_method = Distribution.Method.UNIFORM

    # todo: implement
    def is_valid(self):
        return True
