from tensorflow import keras as KER
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow.keras.models as KMOD
import tensorflow.keras.layers as KLAY
import tensorflow.keras.callbacks as KCALL
import datetime
import os


# Generate a simple net using "Sequential", which just adds each new layer in sequence, from
# input to output.
class NeuralNetCritic:

    def __init__(self, alpha, lamda, gamma, hiddenLayerSizes, inputLayerSize): #fix code
        self.alpha = alpha
        self.lamda = lamda
        self.gamma = gamma
        self.eligibilities = []
        # Build model of type Sequential()
        self.model = Sequential()
        self.model.add(Dense(inputLayerSize, activation='relu', input_dim=inputLayerSize))
        for i in range(len(hiddenLayerSizes)):
            self.model.add(Dense(hiddenLayerSizes[i], activation='relu'))
        self.model.add(Dense(1))

        self.resetEligibilities()
        adagrad = tf.keras.optimizers.Adagrad(learning_rate=self.alpha)
        self.model.compile(optimizer=adagrad,loss=tf.keras.losses.MeanSquaredError(), run_eagerly = True)

    # generate eligibilities with equal shape as trainable weights
    def resetEligibilities(self):
        self.eligibilities.clear()
        for params in self.model.trainable_variables:
            self.eligibilities.append(tf.zeros_like(params))

    # decay eligibilities with factor gamma*lambda
    def updateEligibilities(self):
        for i in range(len(self.eligibilities)):
            self.eligibilities[i] = self.lamda * self.gamma * self.eligibilities[i]

    # return the model's current valuation of given state
    def stateValue(self, state):
        state = [tf.strings.to_number(bin, out_type=tf.dtypes.int32) for bin in state] # convert to array
        state = tf.convert_to_tensor(np.expand_dims(state, axis=0))
        return self.model(state).numpy()[0][0]

    # given the model's valuation of lastState and state, return td_error
    def findTDError(self, reinforcement, lastState, state):
        target = reinforcement + self.gamma * self.stateValue(state)
        td_error = target - self.stateValue(lastState)
        return td_error

    # caluclate loss and apply modified gradients to weights via model optimizer
    def fit(self, reinforcement, lastState, state, td_error):
        with tf.GradientTape() as tape:
            lastState, state, gamma, reinforcement = self.convertData(lastState, state, self.gamma, reinforcement)
            target = tf.add(reinforcement, tf.multiply(gamma, self.model(state)))
            prediction = self.model(lastState)
            loss = self.model.loss(target, prediction)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        modified_gradients = self.modify_gradients(gradients, td_error)
        self.model.optimizer.apply_gradients(zip(modified_gradients, self.model.trainable_variables))

    def modify_gradients(self, gradients, td_error):
        for j in range(len(gradients)):
            gradients[j] = gradients[j] * 1/(2*td_error) # retrieve gradient value of state w.r.t. weights
            self.eligibilities[j] = tf.add(self.eligibilities[j], gradients[j]) # adjust eligibilities with current gradient
            gradients[j] = self.eligibilities[j] * td_error # gradients to be applied by optimizer
        return gradients
    # convert input to tensors
    def convertData(self, lastState, state, gamma, reinforcement):
        lastState = [tf.strings.to_number(bin, out_type=tf.dtypes.float32) for bin in lastState]  # convert to array
        lastState = tf.convert_to_tensor(np.expand_dims(lastState, axis=0))
        state = [tf.strings.to_number(bin, out_type=tf.dtypes.float32) for bin in state]
        state = tf.convert_to_tensor(np.expand_dims(state, axis=0))
        gamma = tf.convert_to_tensor(self.gamma, dtype=tf.dtypes.float32)
        reinforcement = tf.convert_to_tensor(reinforcement, dtype=tf.dtypes.float32)
        return lastState, state, gamma, reinforcement



    """
    def __init__(self, num_classes=10,lrate=0.01,opt='SGD',loss='categorical_crossentropy',act='relu',
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
    """
    