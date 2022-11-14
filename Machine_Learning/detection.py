import cv2
import os
import numpy as np
import tensorflow as tf
import math
# import threading
from utils import label_map_util
from utils import visualization_utilsM as vis_util
import Recognition as rec
import Frame_receive as frecv
import Object_detection as obd

if __name__ == '__main__':
    # 1.Start Initialize
    HOST = '192.168.0.66'
    # HOST= 'localhost'
    PORT = 8485
    # Ready to start machine learning
    # Load to memory
    # MODEL_NAME = 'inference_graph'
    MODEL_NAME = 'inference_graph'
    CWD_PATH = "C:/tensorflow1/models/research/object_detection"
    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')
    NUM_CLASSES = 5
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    # Load complete
    # Start connection
    frecv = frecv.Frame_recv(HOST,PORT)
    frecv.conn_init()
    # Connection complete
    # Until connection is closed
    while frecv.is_conn:
        # 2. Start receiving frame
        frecv.run()
        # Frame receive complete
        frecv.capture(frecv.index)

        # 3.Ready to start Obj detection
        frame_expanded = np.expand_dims(frecv.cam_list[frecv.index].frame, axis=0)
        obj_dt = obd.Obj_detection(sess, detection_boxes, detection_scores, detection_classes, num_detections, image_tensor,
                               frame_expanded,frecv.cam_list[frecv.index])
        # Start Obj detection
        obj_dt.run(category_index)
        # Obj detection complete. Frame is stored at object's attribute

        # 4.Start Act detection
        frecv.cam_list[frecv.index].actrec.run(frecv.cam_list[frecv.index])
        # print(frecv.cam_list[frecv.index])
        # for index in frecv.cam_list:
        #     if index.id == frecv.cam_list[i].id:
        #         index = frecv.cam_list[i]
        # End Act detection
        # Send weight
        frecv.send_weight(frecv.index)
        # Show for debugging
        # If restricted area, draw alert line
        frecv.cam_list[frecv.index].actrec.draw_line(frecv.cam_list[frecv.index])
        cv2.imshow('Object detector', frecv.cam_list[frecv.index].frame)
        # print(frecv.cam_list[frecv.index].weight)
        # print("CAM_ID: {}".format(frecv.cam_list[frecv.index].id))

            # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            frecv.conn.close()
            break