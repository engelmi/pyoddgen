from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class ObjectDetectionDataRecord(GeneratedDataRecord):
    """
    Generated data record structure for use in object detection models.
    """

    GeneratedDataRecord.mandatory_fields.append("image_encoded")
    GeneratedDataRecord.mandatory_fields.append("image_width")
    GeneratedDataRecord.mandatory_fields.append("image_height")
    GeneratedDataRecord.mandatory_fields.append("image_format")
    GeneratedDataRecord.mandatory_fields.append("filename")
    GeneratedDataRecord.mandatory_fields.append("xmins")
    GeneratedDataRecord.mandatory_fields.append("xmaxs")
    GeneratedDataRecord.mandatory_fields.append("ymins")
    GeneratedDataRecord.mandatory_fields.append("ymaxs")
    GeneratedDataRecord.mandatory_fields.append("classes_text")
    GeneratedDataRecord.mandatory_fields.append("classes")

    def __init__(self, data_dict):
        """
        Constructor.
        :param data_dict: Dictionary containing the data of an object detection record. Mandatory fields are:
            - pil_image: The image of the record as PIL Image Object.
            - image_format: Image format of the PIL Image.
            - filename: Name of file the PIL Image was created from.
            - xmins: List of xmins relative to width of the pil image (0 <= xmin <= 1) of all bounding boxes.
            - xmaxs: List of xmaxs relative to width of the pil image (0 <= xmax <= 1) of all bounding boxes.
            - ymins: List of ymins relative to height of the pil image (0 <= ymin <= 1) of all bounding boxes.
            - ymaxs: List of ymaxs relative to height of the pil image (0 <= ymax <= 1) of all bounding boxes.
            - classes_text: Class names of the respective bounding boxes.
            - classes: Class IDs of the respective bounding boxes.
        """
        super(ObjectDetectionDataRecord, self).__init__(data_dict)
        self.check_validity()

    def check_validity(self):
        is_valid, msg = super(ObjectDetectionDataRecord, self).check_validity()
        if not is_valid:
            return False, msg
        for mandatory_field in self.mandatory_fields:
            if mandatory_field not in self.data_dict:
                return False, "Field '" + mandatory_field + "' is missing in data_dict!"
        if not isinstance(self.mandatory_fields["image_encoded"], bytes):
            return False, "Image must be of type '" + str(bytes) + "'! Got '" + str(type(self.mandatory_fields["image_encoded"])) + "' instead."
        if not len(self.mandatory_fields["xmins"]) == len(self.mandatory_fields["xmaxs"]) == \
               len(self.mandatory_fields["ymins"]) == len(self.mandatory_fields["ymaxs"]) == \
               len(self.mandatory_fields["classes_text"]) == len(self.mandatory_fields["classes"]):
            return False, "Length of xmin, xmax, ymin, ymax, classes_text and classes must match!"
        return True, ""

    def to_json_record(self):
        """
        Converts the generated object detection data record to serializable json.
        :return: Serializable JSON-like String.
        """
        return self.to_json_str()

    def to_tf_record(self):
        """
        Converts the generated object detection data record to TensorFlow record.
        :return: TensorFlow Record (.record format).
        """
        # locally used imports
        from pyoddgen.tools.tfdatautils import tf, int64_feature, int64_list_feature, bytes_feature, bytes_list_feature, float_list_feature
        # encode filename and format
        filename = self.mandatory_fields["filename"].encode('utf8')
        image_format = str.encode(self.mandatory_fields["image_format"])
        # create tf record
        tf_record = tf.train.Example(features=tf.train.Features(feature={
            'image/height': int64_feature(self.mandatory_fields["image_height"]),
            'image/width': int64_feature(self.mandatory_fields["image_width"]),
            'image/filename': bytes_feature(filename),
            'image/source_id': bytes_feature(filename),
            'image/encoded': bytes_feature(self.mandatory_fields["image_encoded"]),
            'image/format': bytes_feature(image_format),
            'image/object/bbox/xmin': float_list_feature(self.mandatory_fields["xmins"]),
            'image/object/bbox/xmax': float_list_feature(self.mandatory_fields["xmaxs"]),
            'image/object/bbox/ymin': float_list_feature(self.mandatory_fields["ymins"]),
            'image/object/bbox/ymax': float_list_feature(self.mandatory_fields["ymaxs"]),
            'image/object/class/text': bytes_list_feature(self.mandatory_fields["classes_text"]),
            'image/object/class/label': int64_list_feature(self.mandatory_fields["classes"]),
        }))
        return tf_record
