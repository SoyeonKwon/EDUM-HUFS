import numpy as np
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utilsM as vis_util

class Obj_detection():
    def __init__(self,sess,detection_boxes, detection_scores, detection_classes, num_detections,image_tensor,frame_expanded,cam):
        self.sess = sess
        self.detection_boxes = detection_boxes
        self.detection_scores = detection_scores
        self.detection_classes = detection_classes
        self.num_detections = num_detections
        self.image_tensor = image_tensor
        self.frame_expanded = frame_expanded
        self.cam = cam

    def run(self,category_index):
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: self.frame_expanded})
        vis_util.visualize_boxes_and_labels_on_image_array(
            self.cam.frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            self.cam,
            use_normalized_coordinates=True,
            min_score_thresh=0.60)
