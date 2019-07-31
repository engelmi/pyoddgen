import time
import datetime

from pyoddgen.generators.basegen import BaseGenerator
from pyoddgen.config import ObjectDetectionConfiguration
from pyoddgen.tools.distribution import Distribution
from pyoddgen.datastructures.objectdetectionrecord import ObjectDetectionDataRecord


class ObjectDetectionGenerator(BaseGenerator):

    def __init__(self, config, project_dir):
        if not isinstance(config, ObjectDetectionConfiguration):
            raise Exception("Configuration for generator must be of type '" + str(ObjectDetectionConfiguration) + "'! "
                            "Got '" + str(type(config)) + "' instead. ")
        super(ObjectDetectionGenerator, self).__init__(config, project_dir)
        self.background_distribution = Distribution(config.fields["background_distribution_method"])
        self.class_distribution = Distribution(config.fields["class_distribution_method"])
        self.position_distribution = Distribution(config.fields["position_distribution_method"])
        self.paste_no_distribution = Distribution(config.fields["number_of_pastes_per_background_distribution_method"])

    def get_log_header(self):
        return ["Time"] + [ObjectDetectionDataRecord.mandatory_fields[i] for i in range(len(ObjectDetectionDataRecord.mandatory_fields))]

    def log_generated_data(self, generated_data_record):
        if not isinstance(generated_data_record, ObjectDetectionDataRecord):
            raise Exception("Generated data record to log must be of type '" + str(ObjectDetectionDataRecord) + "'!")
        ret, msg = generated_data_record.check_validity()
        if not ret:
            raise Exception("Generated data record is not valid: " + msg)
        log_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        rows = [[log_time] + [generated_data_record.data_dict[ObjectDetectionDataRecord.mandatory_fields[i]] for i in range(len(ObjectDetectionDataRecord.mandatory_fields))]]
        self.csv_log_file.write_rows(rows)

    def generate_next(self):
        return ObjectDetectionDataRecord()

    def select_background(self):
        pass

    def select_classes(self):
        pass

    def select_positions(self, background_dims, num_classes):
        pos_x_randoms = []
        pos_y_randoms = []
        bck_x, bck_y = background_dims
        dist_cls_x, dist_cls_y = self.config.distance_between_pastes
        num_of_retries = 10
        while len(pos_x_randoms) < num_classes:
            for i in range(num_of_retries):
                next_x = int(self.background_distribution.next(calc_distance=False)*bck_x)
                next_y = int(self.background_distribution.next(calc_distance=False)*bck_y)
                valid = True
                for j in range(len(pos_x_randoms)):
                    valid = ((pos_x_randoms[j] - next_x) >= dist_cls_x) and ((pos_y_randoms[j] - next_y) >= dist_cls_y)
                    if not valid:
                        break
                if valid or i == num_of_retries - 1:
                    pos_x_randoms.append(next_x)
                    pos_y_randoms.append(next_y)
        return zip(pos_x_randoms, pos_y_randoms)

    def apply_modifications_to_background(self, background):
        pass

    def apply_modifications_to_classes(self, classes):
        pass
