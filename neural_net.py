from tensorflow import keras as KER
import numpy as np
import tensorflow as tf
import tensorflow.keras.models as KMOD
import tensorflow.keras.layers as KLAY
import tensorflow.keras.callbacks as KCALL
import datetime
import os


# Generate a simple net using "Sequential", which just adds each new layer in sequence, from
# input to output.
def gennet(num_classes=10,lrate=0.01,opt='SGD',loss='categorical_crossentropy',act='relu',
           conv=True,lastact='softmax'):
    opt = eval('KER.optimizers.' + opt)
    loss = eval('KER.losses.'+loss) if type(loss) == str else loss
    model = KER.models.Sequential() # The model can now be built sequentially from input to output
    if conv:  # Starting off with a convolution layer followed by max pooling
        model.add(KER.layers.Conv1D(16, kernel_size=(5)))
        model.add(KER.layers.MaxPooling1D(5))
        model.add(KER.layers.Flatten())
    model.add(KER.layers.Dense(50,activation=act))
    model.add(KER.layers.Dense(25,activation=act))
    model.add(KER.layers.Dense(num_classes,activation=lastact))
    model.compile(optimizer=opt(lr=lrate),loss=loss,metrics=[KER.metrics.categorical_accuracy])
    return model