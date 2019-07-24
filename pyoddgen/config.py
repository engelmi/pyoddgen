from os.path import join

from pyoddgen.serializable import Serializable
from pyoddgen.tools.distribution import Distribution


class ProjectConfiguration(Serializable):

    def __init__(self):
        self.project_dir = ""

        self.generator_config_list = []


class GeneratorConfiguration(Serializable):

    def __init__(self):
        self.generator_class = ""
        self.generator_name = ""

        # directories
        self.generator_dir = self.generator_name
        self.resource_dir = join(self.generator_dir, "resources")
        self.resource_classes_dir = join(self.resource_dir, "classes")
        self.resource_backgrounds_dir = join(self.resource_dir, "backgrounds")
        self.output_dir = join(self.generator_dir, "output")

        # files
        self.generated_data_log = join(self.generator_dir, "generated_data_log.csv")
        self.used_distributions_file = join(self.generator_dir, "distributions.csv")
        self.classes_weights_file = join(self.resource_classes_dir, "class_weights.csv")
        self.backgrounds_weights_file = join(self.resource_backgrounds_dir, "class_weights.csv")

        # generation
        self.batch_size = 100
        self.save_generated_raw_images = True
        self.final_scale_factor = 1
        self.class_distribution_method = Distribution.Method.UNIFORM
        self.background_distribution_method = Distribution.Method.UNIFORM
        self.position_distribution_method = Distribution.Method.UNIFORM
        self.number_of_pastes_per_background_min = 0
        self.number_of_pastes_per_background_max = 15
        self.number_of_pastes_per_background_distribution_method = Distribution.Method.UNIFORM

        # log
        self.generated_data_log_enabled = True
