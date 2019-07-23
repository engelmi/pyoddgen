from PIL import Image

from pyoddgen.tools.typeconv import pil_to_byte
from pyoddgen.datastructures.gendatarecord import GeneratedDataRecord


class ObjectDetectionDataRecord(GeneratedDataRecord):
    """
    Generated data record structure for use in object detection models.
    """

    def __init__(self, pil_image, image_format, filename, xmins, xmaxs, ymins, ymaxs, classes_text, classes):
        """
        Constructor.
        :param pil_image: The image of the record as PIL Image Object.
        :param image_format: Image format of the PIL Image.
        :param filename: Name of file the PIL Image was created from.
        :param xmins: List of xmins relative to width of the pil image (0 <= xmin <= 1) of all bounding boxes.
        :param xmaxs: List of xmaxs relative to width of the pil image (0 <= xmax <= 1) of all bounding boxes.
        :param ymins: List of ymins relative to height of the pil image (0 <= ymin <= 1) of all bounding boxes.
        :param ymaxs: List of ymaxs relative to height of the pil image (0 <= ymax <= 1) of all bounding boxes.
        :param classes_text: Class names of the respective bounding boxes.
        :param classes: Class IDs of the respective bounding boxes.
        """
        if not Image.isImageType(pil_image):
            raise Exception("Image must be of type '" + str(Image) + "'! Got '" + str(type(pil_image)) + "' instead. ")
        if not (len(self.xmins) == len(self.xmaxs) == len(self.ymins) == len(self.ymaxs) == len(self.classes_text) == len(self.classes)):
            raise Exception("Error creating tf record: Length of xmin, xmax, ymin, ymax, classes_text, classes must match!")
        # convert pil image to bytes
        self.pil_image_encoded = pil_to_byte(pil_image)
        self.pil_image_width, self.pil_image_height = pil_image.size
        self.image_format = image_format
        self.filename = filename
        self.xmins = xmins
        self.xmaxs = xmaxs
        self.ymins = ymins
        self.ymaxs = ymaxs
        self.classes_text = classes_text
        self.classes = classes

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
        filename = self.filename.encode('utf8')
        image_format = str.encode(self.image_format)
        # create tf record
        tf_record = tf.train.Example(features=tf.train.Features(feature={
            'image/height': int64_feature(self.pil_image_height),
            'image/width': int64_feature(self.pil_image_width),
            'image/filename': bytes_feature(filename),
            'image/source_id': bytes_feature(filename),
            'image/encoded': bytes_feature(self.pil_image_encoded),
            'image/format': bytes_feature(image_format),
            'image/object/bbox/xmin': float_list_feature(self.xmins),
            'image/object/bbox/xmax': float_list_feature(self.xmaxs),
            'image/object/bbox/ymin': float_list_feature(self.ymins),
            'image/object/bbox/ymax': float_list_feature(self.ymaxs),
            'image/object/class/text': bytes_list_feature(self.classes_text),
            'image/object/class/label': int64_list_feature(self.classes),
        }))
        return tf_record
