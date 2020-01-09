# 参考

- [https://github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) An Open Source Machine Learning Framework for Everyone
- [https://github.com/jikexueyuanwiki/tensorflow-zh](https://github.com/jikexueyuanwiki/tensorflow-zh) 谷歌全新开源人工智能系统 TensorFlow 官方文档中文版
- [https://tensorflow.google.cn/](https://tensorflow.google.cn/)

```bash
pip3 install --upgrade tensorflow
ERROR: Could not find a version that satisfies the requirement tensorflow (from versions: none)
ERROR: No matching distribution found for tensorflow
# 查看python版本
python.exe -V
Python 3.8.0
# 查看tensorflow支持的python版本
https://tensorflow.google.cn/install/pip

Python 3.6 CPU-only  https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-2.0.0-cp36-cp36m-manylinux2010_x86_64.whl
Python 3.6 GPU support  https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.0.0-cp36-cp36m-manylinux2010_x86_64.whl
Python 3.7 CPU-only  https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-2.0.0-cp37-cp37m-manylinux2010_x86_64.whl
Python 3.7 GPU support  https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.0.0-cp37-cp37m-manylinux2010_x86_64.whl
```

## 安装`tensorflow`

```bash
#下载CPU版本的`tensorflow`
pip3 install --upgrade tensorflow

# 支持GPU版本（如果你有NVIDIA的显卡，可以考虑开启这个）
pip3 install --upgrade tensorflow-gpu
```

### MNIST 数据下载

[Yann LeCun's MNIST page](http://yann.lecun.com/exdb/mnist/) 提供了训练集与测试集数据的下载。
|文件|内容|
|-------------------------|----------------------------|
|train-images-idx3-ubyte.gz|训练集图片 - 55000 张 训练图片, 5000 张 验证图片|
|train-labels-idx1-ubyte.gz|训练集图片对应的数字标签|
|t10k-images-idx3-ubyte.gz|测试集图片 - 10000 张 图片|
|t10k-labels-idx1-ubyte.gz|测试集图片对应的数字标签|

### `input_data.py`文件用于训练和测试的 MNIST 数据集的源码

[github 源码](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/tutorials/mnist)

```python
# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Functions for downloading and reading MNIST data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import os
import tempfile

import numpy
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets
```

### 运行测试程序

```python
import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
import tensorflow as tf
x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x,W) + b)
y_ = tf.placeholder("float", [None,10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
```

```bash
$ python learn1.py

2019-09-02 12:57:00.639996: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
Extracting MNIST_data/train-images-idx3-ubyte.gz
Extracting MNIST_data/train-labels-idx1-ubyte.gz
Extracting MNIST_data/t10k-images-idx3-ubyte.gz
Extracting MNIST_data/t10k-labels-idx1-ubyte.gz
0.9165
```
