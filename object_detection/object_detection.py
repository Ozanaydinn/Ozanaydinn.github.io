import tensorflow as tf
import numpy as np
import cv2

from tensorflow.keras import Model
from tensorflow.keras.layers import (
    Add,
    Concatenate,
    Conv2D,
    Input,
    Lambda,
    LeakyReLU,
    UpSampling2D,
    ZeroPadding2D,
    BatchNormalization
)
from tensorflow.keras.regularizers import l2

class ObjectDetect:

    def __init__(self, image):
        self.image = image

    def load_darknet_weights(self, model, weights_file):
        '''
        Helper function used to load darknet weights.
        
        :param model: Object of the Yolo v3 model
        :param weights_file: Path to the file with Yolo V3 weights
        '''
        
        #Open the weights file
        wf = open(weights_file, 'rb')
        major, minor, revision, seen, _ = np.fromfile(wf, dtype=np.int32, count=5)

        #Define names of the Yolo layers (just for a reference)    
        layers = ['yolo_darknet',
                'yolo_conv_0',
                'yolo_output_0',
                'yolo_conv_1',
                'yolo_output_1',
                'yolo_conv_2',
                'yolo_output_2']

        for layer_name in layers:
            sub_model = model.get_layer(layer_name)
            for i, layer in enumerate(sub_model.layers):
            
                
                if not layer.name.startswith('conv2d'):
                    continue
                    
                #Handles the special, custom Batch normalization layer
                batch_norm = None
                if i + 1 < len(sub_model.layers) and \
                        sub_model.layers[i + 1].name.startswith('batch_norm'):
                    batch_norm = sub_model.layers[i + 1]

                filters = layer.filters
                size = layer.kernel_size[0]
                in_dim = layer.input_shape[-1]

                if batch_norm is None:
                    conv_bias = np.fromfile(wf, dtype=np.float32, count=filters)
                else:
                    # darknet [beta, gamma, mean, variance]
                    bn_weights = np.fromfile(
                        wf, dtype=np.float32, count=4 * filters)
                    # tf [gamma, beta, mean, variance]
                    bn_weights = bn_weights.reshape((4, filters))[[1, 0, 2, 3]]

                # darknet shape (out_dim, in_dim, height, width)
                conv_shape = (filters, in_dim, size, size)
                conv_weights = np.fromfile(
                    wf, dtype=np.float32, count=np.product(conv_shape))
                # tf shape (height, width, in_dim, out_dim)
                conv_weights = conv_weights.reshape(
                    conv_shape).transpose([2, 3, 1, 0])

                if batch_norm is None:
                    layer.set_weights([conv_weights, conv_bias])
                else:
                    layer.set_weights([conv_weights])
                    batch_norm.set_weights(bn_weights)

        assert len(wf.read()) == 0, 'failed to read all data'
        wf.close()
    

    yolo_anchors = np.array([(10, 13), (16, 30), (33, 23), (30, 61), (62, 45),
                            (59, 119), (116, 90), (156, 198), (373, 326)],
                            np.float32) / 416

    yolo_anchor_masks = np.array([[6, 7, 8], [3, 4, 5], [0, 1, 2]])
        
    def DarknetConv(self, x, filters, kernel_size, strides=1, batch_norm=True):
        '''
        Call this function to define a single Darknet convolutional layer
        
        :param x: inputs
        :param filters: number of filters in the convolutional layer
        :param kernel_size: Size of kernel in the Conv layer
        :param strides: Conv layer strides
        :param batch_norm: Whether or not to use the custom batch norm layer.
        '''
        #Image padding
        if strides == 1:
            padding = 'same'
        else:
            x = ZeroPadding2D(((1, 0), (1, 0)))(x)  # top left half-padding
            padding = 'valid'
            
        #Defining the Conv layer
        x = Conv2D(filters=filters, kernel_size=kernel_size,
                strides=strides, padding=padding,
                use_bias=not batch_norm, kernel_regularizer=l2(0.0005))(x)
        
        if batch_norm:
            x = BatchNormalization()(x)
            x = LeakyReLU(alpha=0.1)(x)
        return x

    def DarknetResidual(self, x, filters):
        '''
        Call this function to define a single DarkNet Residual layer
        
        :param x: inputs
        :param filters: number of filters in each Conv layer.
        '''
        prev = x
        x = self.DarknetConv(x, filters // 2, 1)
        x = self.DarknetConv(x, filters, 3)
        x = Add()([prev, x])
        return x
    
    
    def DarknetBlock(self, x, filters, blocks):
        '''
        Call this function to define a single DarkNet Block (made of multiple Residual layers)
        
        :param x: inputs
        :param filters: number of filters in each Residual layer
        :param blocks: number of Residual layers in the block
        '''
        x = self.DarknetConv(x, filters, 3, strides=2)
        for _ in range(blocks):
            x = self.DarknetResidual(x, filters)
        return x

    def Darknet(self, name=None):
        '''
        The main function that creates the whole DarkNet.
        '''
        x = inputs = Input([None, None, 3])
        x = self.DarknetConv(x, 32, 3)
        x = self.DarknetBlock(x, 64, 1)
        x = self.DarknetBlock(x, 128, 2)  # skip connection
        x = x_36 = self.DarknetBlock(x, 256, 8)  # skip connection
        x = x_61 = self.DarknetBlock(x, 512, 8)
        x = self.DarknetBlock(x, 1024, 4)
        return tf.keras.Model(inputs, (x_36, x_61, x), name=name)

    def YoloConv(self, filters, name=None):
        '''
        Call this function to define the Yolo Conv layer.
        
        :param filters: number of filters for the conv layer
        :param name: name of the layer
        '''
        def yolo_conv(x_in):
            if isinstance(x_in, tuple):
                inputs = Input(x_in[0].shape[1:]), Input(x_in[1].shape[1:])
                x, x_skip = inputs

                # concat with skip connection
                x = self.DarknetConv(x, filters, 1)
                x = UpSampling2D(2)(x)
                x = Concatenate()([x, x_skip])
            else:
                x = inputs = Input(x_in.shape[1:])

            x = self.DarknetConv(x, filters, 1)
            x = self.DarknetConv(x, filters * 2, 3)
            x = self.DarknetConv(x, filters, 1)
            x = self.DarknetConv(x, filters * 2, 3)
            x = self.DarknetConv(x, filters, 1)
            return Model(inputs, x, name=name)(x_in)
        return yolo_conv

    def YoloOutput(self, filters, anchors, classes, name=None):
        '''
        This function defines outputs for the Yolo V3. (Creates output projections)
        
        :param filters: number of filters for the conv layer
        :param anchors: anchors
        :param classes: list of classes in a dataset
        :param name: name of the layer
        '''
        def yolo_output(x_in):
            x = inputs = Input(x_in.shape[1:])
            x = self.DarknetConv(x, filters * 2, 3)
            x = self.DarknetConv(x, anchors * (classes + 5), 1, batch_norm=False)
            x = Lambda(lambda x: tf.reshape(x, (-1, tf.shape(x)[1], tf.shape(x)[2],
                                                anchors, classes + 5)))(x)
            return tf.keras.Model(inputs, x, name=name)(x_in)
        return yolo_output

    def yolo_boxes(self, pred, anchors, classes):
        '''
        Call this function to get bounding boxes from network predictions
        
        :param pred: Yolo predictions
        :param anchors: anchors
        :param classes: List of classes from the dataset
        '''
        
        # pred: (batch_size, grid, grid, anchors, (x, y, w, h, obj, ...classes))
        grid_size = tf.shape(pred)[1]
        #Extract box coortinates from prediction vectors
        box_xy, box_wh, objectness, class_probs = tf.split(
            pred, (2, 2, 1, classes), axis=-1)

        #Normalize coortinates
        box_xy = tf.sigmoid(box_xy)
        objectness = tf.sigmoid(objectness)
        class_probs = tf.sigmoid(class_probs)
        pred_box = tf.concat((box_xy, box_wh), axis=-1)  # original xywh for loss

        # !!! grid[x][y] == (y, x)
        grid = tf.meshgrid(tf.range(grid_size), tf.range(grid_size))
        grid = tf.expand_dims(tf.stack(grid, axis=-1), axis=2)  # [gx, gy, 1, 2]

        box_xy = (box_xy + tf.cast(grid, tf.float32)) / \
            tf.cast(grid_size, tf.float32)
        box_wh = tf.exp(box_wh) * anchors

        box_x1y1 = box_xy - box_wh / 2
        box_x2y2 = box_xy + box_wh / 2
        bbox = tf.concat([box_x1y1, box_x2y2], axis=-1)

        return bbox, objectness, class_probs, pred_box

    def yolo_nms(self, outputs, anchors, masks, classes):
        # boxes, conf, type
        b, c, t = [], [], []

        for o in outputs:
            b.append(tf.reshape(o[0], (tf.shape(o[0])[0], -1, tf.shape(o[0])[-1])))
            c.append(tf.reshape(o[1], (tf.shape(o[1])[0], -1, tf.shape(o[1])[-1])))
            t.append(tf.reshape(o[2], (tf.shape(o[2])[0], -1, tf.shape(o[2])[-1])))

        bbox = tf.concat(b, axis=1)
        confidence = tf.concat(c, axis=1)
        class_probs = tf.concat(t, axis=1)

        scores = confidence * class_probs
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(bbox, (tf.shape(bbox)[0], -1, 1, 4)),
            scores=tf.reshape(
            scores, (tf.shape(scores)[0], -1, tf.shape(scores)[-1])),
            max_output_size_per_class=100,
            max_total_size=100,
            iou_threshold=0.5,
            score_threshold=0.6
        )

        return boxes, scores, classes, valid_detections


    def YoloV3(self, size=None, channels=3, anchors=yolo_anchors,
            masks=yolo_anchor_masks, classes=80):
    
        x = inputs = Input([size, size, channels], name='input')

        x_36, x_61, x = self.Darknet(name='yolo_darknet')(x)

        x = self.YoloConv(512, name='yolo_conv_0')(x)
        output_0 = self.YoloOutput(512, len(masks[0]), classes, name='yolo_output_0')(x)

        x = self.YoloConv(256, name='yolo_conv_1')((x, x_61))
        output_1 = self.YoloOutput(256, len(masks[1]), classes, name='yolo_output_1')(x)

        x = self.YoloConv(128, name='yolo_conv_2')((x, x_36))
        output_2 = self.YoloOutput(128, len(masks[2]), classes, name='yolo_output_2')(x)

        boxes_0 = Lambda(lambda x: self.yolo_boxes(x, anchors[masks[0]], classes),
                        name='yolo_boxes_0')(output_0)
        boxes_1 = Lambda(lambda x: self.yolo_boxes(x, anchors[masks[1]], classes),
                        name='yolo_boxes_1')(output_1)
        boxes_2 = Lambda(lambda x: self.yolo_boxes(x, anchors[masks[2]], classes),
                        name='yolo_boxes_2')(output_2)

        outputs = Lambda(lambda x: self.yolo_nms(x, anchors, masks, classes),
                        name='yolo_nms')((boxes_0[:3], boxes_1[:3], boxes_2[:3]))

        return Model(inputs, outputs, name='yolov3')

    def search_phone(self):

        result = { "phone": False, "person": 0}

        yolo = self.YoloV3()

        import sys
        self.load_darknet_weights(yolo, 'models/yolov3.weights')
        self.image = np.array(self.image)
        self.image = self.image[:,:,:3]
        self.image = cv2.resize(self.image, (320, 320))
        self.image = self.image.astype(np.float32)
        self.image = np.expand_dims(self.image, 0)
        self.image = self.image / 255
        class_names = [c.strip() for c in open("models/classes.TXT").readlines()]
        boxes, scores, classes, nums = yolo(self.image)
        count=0
        for i in range(nums[0]):
            if int(classes[0][i] == 0):
                result["person"] += 1
            if int(classes[0][i] == 67):
                result["phone"] = True
                
        return result
