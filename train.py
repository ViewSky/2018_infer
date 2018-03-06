#coding=utf-8
# pylint: disable=C0111,too-many-arguments,too-many-instance-attributes,too-many-locals,redefined-outer-name,fixme
# pylint: disable=superfluous-parens, no-member, invalid-name

import sys
sys.path.insert(0, "../../python")
import mxnet as mx
import numpy as np
import cv2, random
from io import BytesIO
from genplate import *


class OCRBatch(object):
    def __init__(self, data_names, data, label_names, label):
        self.data = data
        self.label = label
        self.data_names = data_names
        self.label_names = label_names

    @property
    def provide_data(self):
        return [(n, x.shape) for n, x in zip(self.data_names, self.data)]

    @property
    def provide_label(self):
        return [(n, x.shape) for n, x in zip(self.label_names, self.label)]

def rand_range(lo,hi):
    return lo+r(hi-lo);


def gen_rand():
    name = "";
    label= [];
    label.append(rand_range(0,31));
    label.append(rand_range(41,65));
    for i in xrange(5):
        label.append(rand_range(31,65))

    name+=chars[label[0]]
    name+=chars[label[1]]
    for i in xrange(5):
        name+=chars[label[i+2]]
    return name,label



def gen_sample(genplate, width, height):
    num,label = gen_rand()
    img = genplate.generate(num)
    img = cv2.resize(img, (width, height))
    img = np.multiply(img, 1/255.0)
    img = img.transpose(2, 0, 1)

    return label, img

class OCRIter(mx.io.DataIter):
    def __init__(self, count, batch_size, num_label, height, width):
        super(OCRIter, self).__init__()
        self.genplate = GenPlate("./font/platech.ttf",'./font/platechar.ttf','./NoPlates')
        self.batch_size = batch_size
        self.count = count
        self.height = height
        self.width = width
        self.provide_data = [('data', (batch_size, 3, height, width))]
        self.provide_label = [('softmax_label', (self.batch_size, num_label))]
        print "start"
    def __iter__(self):

        for k in range(self.count / self.batch_size):
            data = []
            label = []
            for i in range(self.batch_size):
                num, img = gen_sample(self.genplate, self.width, self.height)
                data.append(img)
                label.append(num)

            data_all = [mx.nd.array(data)]
            label_all = [mx.nd.array(label)]
            data_names = ['data']
            label_names = ['softmax_label']
            data_batch = OCRBatch(data_names, data_all, label_names, label_all)
            yield data_batch

    def reset(self):
        pass

def get_ocrnet():
    data = mx.symbol.Variable('data')
    label = mx.symbol.Variable('softmax_label')
    conv1 = mx.symbol.Convolution(data=data, kernel=(5,5), num_filter=32)
    pool1 = mx.symbol.Pooling(data=conv1, pool_type="max", kernel=(2,2), stride=(1, 1))
    relu1 = mx.symbol.Activation(data=pool1, act_type="relu")

    conv2 = mx.symbol.Convolution(data=relu1, kernel=(5,5), num_filter=32)
    pool2 = mx.symbol.Pooling(data=conv2, pool_type="avg", kernel=(2,2), stride=(1, 1))
    relu2 = mx.symbol.Activation(data=pool2, act_type="relu")

    # conv3 = mx.symbol.Convolution(data=relu2, kernel=(3,3), num_filter=32)
    # pool3 = mx.symbol.Pooling(data=conv3, pool_type="avg", kernel=(2,2), stride=(1, 1))
    # relu3 = mx.symbol.Activation(data=pool3, act_type="relu")
    #
    # conv4 = mx.symbol.Convolution(data=relu3, kernel=(3,3), num_filter=32)
    # pool4 = mx.symbol.Pooling(data=conv4, pool_type="avg", kernel=(2,2), stride=(1, 1))
    # relu4 = mx.symbol.Activation(data=pool4, act_type="relu")

    flatten = mx.symbol.Flatten(data = relu2)
    fc1 = mx.symbol.FullyConnected(data = flatten, num_hidden = 120)
    fc21 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do21 = mx.symbol.Dropout(data=fc21,name='do21',p=0.25)
    fc22 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do22 = mx.symbol.Dropout(data=fc21,name='do22',p=0.25)
    fc23 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do23 = mx.symbol.Dropout(data=fc21,name='do23',p=0.25)
    fc24 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do24 = mx.symbol.Dropout(data=fc21,name='do24',p=0.25)
    fc25 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do25 = mx.symbol.Dropout(data=fc21,name='do25',p=0.25)
    fc26 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do26 = mx.symbol.Dropout(data=fc21,name='do26',p=0.25)
    fc27 = mx.symbol.FullyConnected(data = fc1, num_hidden = 65)
    do27 = mx.symbol.Dropout(data=fc21,name='do27',p=0.25)
    fc2 = mx.symbol.Concat(*[do21, do22, do23, do24,do25,do26,do27], dim = 0)
    #fc2 = mx.symbol.Concat(*[fc21, fc22, fc23, fc24,fc25,fc26,fc27], dim = 0)
    label = mx.symbol.transpose(data = label)
    label = mx.symbol.Reshape(data = label, target_shape = (0, ))
    return mx.symbol.SoftmaxOutput(data = fc2, label = label, name = "softmax")


def Accuracy(label, pred):
    label = label.T.reshape((-1, ))
    hit = 0
    total = 0
    for i in range(pred.shape[0] / 7):
        ok = True
        for j in range(7):
            k = i * 7 + j
            if np.argmax(pred[k]) != int(label[k]):
                ok = False
                break
        if ok:
            hit += 1
        total += 1
    return 1.0 * hit / total


def train():
    import logging
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=head)

    model_prefix = 'cnn-ocr'
    checkpoint = mx.callback.do_checkpoint(model_prefix)

    batch_size = 8
    data_train = OCRIter(500000, batch_size, 7, 30, 120)
    data_test = OCRIter(1000, batch_size,7, 30, 120)
    network = get_ocrnet()
    devs = [mx.gpu(i) for i in range(1)]
    model = mx.mod.Module(network)
    model.bind(data_shapes=data_train.provide_data,label_shapes=data_test.provide_label)
    model.init_params(initializer=mx.init.Xavier(rnd_type='gaussian', factor_type="in", magnitude=2.34))
###load epoch
    sym, arg_params, aux_params = mx.model.load_checkpoint("cnn-ocr",25)

    model.set_params(arg_params, aux_params, allow_missing=True)

    #mod.set_params(new_args, aux_params, allow_missing=True)

    model.fit(data_train, eval_data = data_test,
            eval_metric = Accuracy, batch_end_callback=mx.callback.Speedometer(batch_size, 50),
            #optimizer = 'sgd',
            optimizer_params={'learning_rate':0.0001,'wd':0.00001,'momentum':0.9},
            num_epoch = 100, epoch_end_callback = checkpoint)

    #model.save("cnn-ocr")

    print gen_rand()


if __name__ == '__main__':
#load

    train();
