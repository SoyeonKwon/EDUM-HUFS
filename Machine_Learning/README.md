Object Detection
=============
How to install and run the object detection
-----------
### Install reference guide link
  + How To Install TensorFlow: [https://www.youtube.com/watch?v=RplXYjxgZbw](http://hyper/)
  + How To Train an Object Detection Classifier Using TensorFlow 1.5: [https://www.youtube.com/watch?v=Rgpfk6eYxJA](http://hyper/)
  + Please follow the order with this links
#### 1. Install Python(Requires Python 3.4, 3.5, or 3.6), Anaconda
#### 2. Install GPU driver, CUDA V9.0, and CuDNN v7.0 (for latest version of tensorflow)
#### 3. Check environment variables
    Make sure adding the following paths;bin, libnvvp, libx64
#### 4. Create and activate venv using anaconda prompt
```
C:\> conda create -n tensorflow1 pip python=3.5
```
  Then, activate the environment by issuing:
```
C:\> activate tensorflow1
```
#### 5. Install tensorflow-gpu (This installation for venv)
  ```
  pip install --ignore-installed --upgrade tensorflow-gpu
  ```
#### 6. Download this tutorial's repository from GitHub and move to venv directory
  [Link]: https://github.com/tensorflow/models "Download"
  After moving this files, move Machine_Learning too.
  
  <https://github.com/jy016011/ICE_CAP/tree/master/Machine_Learning>
#### 7. Install the other necessary packages
```
(tensorflow1) C:\> conda install -c anaconda protobuf
(tensorflow1) C:\> pip install pillow
(tensorflow1) C:\> pip install lxml
(tensorflow1) C:\> pip install Cython
(tensorflow1) C:\> pip install jupyter
(tensorflow1) C:\> pip install matplotlib
(tensorflow1) C:\> pip install pandas
(tensorflow1) C:\> pip install opencv-python
```
(Note: The ‘pandas’ and ‘opencv-python’ packages are not needed by TensorFlow, but they are used in the Python scripts to generate TFRecords and to work with images, videos, and webcam feeds.)

#### 8. Configure PYTHONPATH environment variable
```
(tensorflow1) C:\> set PYTHONPATH=C:\tensorflow1\models;C:\tensorflow1\models\research;C:\tensorflow1\models\research\slim
```
(Note: Every time the "tensorflow1" virtual environment is exited, the PYTHONPATH variable is reset and needs to be set up again.)

(Note: If you don't want to set PATH everytime, add PATH to system path)

#### 9. Compile Protobufs and run setup.py
```
protoc --python_out=. .\object_detection\protos\anchor_generator.proto .\object_detection\protos\argmax_matcher.proto .\object_detection\protos\bipartite_matcher.proto .\object_detection\protos\box_coder.proto .\object_detection\protos\box_predictor.proto .\object_detection\protos\eval.proto .\object_detection\protos\faster_rcnn.proto .\object_detection\protos\faster_rcnn_box_coder.proto .\object_detection\protos\grid_anchor_generator.proto .\object_detection\protos\hyperparams.proto .\object_detection\protos\image_resizer.proto .\object_detection\protos\input_reader.proto .\object_detection\protos\losses.proto .\object_detection\protos\matcher.proto .\object_detection\protos\mean_stddev_box_coder.proto .\object_detection\protos\model.proto .\object_detection\protos\optimizer.proto .\object_detection\protos\pipeline.proto .\object_detection\protos\post_processing.proto .\object_detection\protos\preprocessor.proto .\object_detection\protos\region_similarity_calculator.proto .\object_detection\protos\square_box_coder.proto .\object_detection\protos\ssd.proto .\object_detection\protos\ssd_anchor_generator.proto .\object_detection\protos\string_int_label_map.proto .\object_detection\protos\train.proto .\object_detection\protos\keypoint_box_coder.proto .\object_detection\protos\multiscale_anchor_generator.proto .\object_detection\protos\graph_rewriter.proto
```
Finish Setup using this command.
```
(tensorflow1) C:\tensorflow1\models\research> python setup.py build
(tensorflow1) C:\tensorflow1\models\research> python setup.py install
```
#### 10. Extract install files directory and move all
 [Goto]: https://github.com/jy016011/ICE_CAP/tree/master/Machine_Learning/Install%20Files "Follow the guide"
### LAST. Run the detection.py if server is ready!
  If webcam is connected and server is ready, run the detection.py


Source
-------------
<https://github.com/tensorflow/models#tensorflow-models>

<https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/>
