from tensorflow import keras as KER
import numpy as np
import tensorflow as tf
from numpy.random import seed
tf.random.set_seed(2)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import datetime
import os

# Generate a simple net using "Sequential", which just adds each new layer in sequence, from
# input to output. "Dense" just gives the regular densely-connected NN-layer
class NeuralNetCritic:
    #Declare network
    def __init__(self, alpha_c, lamda, gam, dimNN, input_layer_size): 

        # Sequential neural network
        self.model = Sequential() #sequential stacks the layers automatically
        self.model.add(Dense(input_layer_size, activation='relu', input_dim=input_layer_size))#relu forenkler funksjonen
        for dim in dimNN: #hidden layers
            self.model.add(Dense(dim, activation='relu')) 

        #Add single value outputlayer ( V(s) )
        self.model.add(Dense(1))

        #Declare eligibilities 
        self.eligibilities = []
        self.reset_eligibilities()

        #using adagrad as optimizer
        adagrad = tf.keras.optimizers.Adagrad(learning_rate=alpha_c)
        self.model.compile(optimizer=adagrad,loss=tf.keras.losses.MeanSquaredError(), run_eagerly = True)
         
         #Store values for easy access in eventual use
        self.gam = gam
        self.lamda = lamda
        self.alpha_c = alpha_c

    # Make the shape of eligibilities the same as the models trainable weight
    def reset_eligibilities(self):
        self.eligibilities = []
        params = self.model.trainable_variables
        for i in range(len(params)):
            self.eligibilities.append(tf.zeros_like(params[i])) #returns same size with elements set to zero

    # Forumulate the error as given in "Implementing the Actor-Critic Model of Reinforcement Learning.pdf"
    #remember s is last state, and s_prime is (next) state
    def calc_td_error(self, r, s_prime,s):
        td_error = r + self.gam * self.values(s_prime) - self.values(s)
        return td_error

    # return the model's current valuation of given s_prime
    def values(self, s_prime):
        s_prime = [tf.strings.to_number(bin, out_type=tf.dtypes.int32) for bin in s_prime] # convert to array
        s_prime = tf.convert_to_tensor(np.expand_dims(s_prime, axis=0))
        return self.model(s_prime).numpy()[0][0]

    #Find loss then use the modified gradients to construct weights 
    #based on Keiths fit innner loop in presentation from basics of KERAS 
    # make gradients and apply them
    def fit(self, r, s, s_prime, td_error): #runs multiple times from loop in actor-critic alghorithm, inspiration from splitGD
        params = self.model.trainable_variables
        train_inputs, train_targets = self.split_training_data(s, s_prime)
        with tf.GradientTape() as tape: #need to because we have eligibility traces
            target = tf.add(r, tf.multiply(self.gam, self.model(train_targets)))
            prediction = self.model(train_inputs)
            loss = self.model.loss(target, prediction)
            gradients = tape.gradient(loss, params) #main function, computes all gradients, derivatives of loss
            gradients = self.modify_gradients(gradients, td_error) #modify gradients using td_error, why have we have to convert data
            self.model.optimizer.apply_gradients(zip(gradients, params)) #apply the gradients

    # Here we convert the inputs and targets to tensors, for use in tf models
    def split_training_data(self, inputs, targets):
        inputs = [tf.strings.to_number(bin, out_type=tf.dtypes.float32) for bin in inputs]  # convert to array
        targets = [tf.strings.to_number(bin, out_type=tf.dtypes.float32) for bin in targets] # convert to array
        inputs = tf.convert_to_tensor(np.expand_dims(inputs, axis=0))
        targets = tf.convert_to_tensor(np.expand_dims(targets, axis=0))
        return inputs, targets
    
    #We base the gradients[i] on,"Implementing the Actor-Critic Model of Reinforcement Learning.pdf" as this is our 
    #understanding. ∂L/∂w_i =−2δ(∂V(s)/∂w_i) <=> (∂V(s)/∂w_i) = ∂L/∂w_i * 1/2
    def modify_gradients(self, gradients, td_error):
        for i in range(len(gradients)):
            gradients[i] = gradients[i] * 1/(2*td_error) #from formula in actor critic model
            self.eligibilities[i] = tf.add(self.eligibilities[i], gradients[i]) # adjust eligibilities with current gradient
            gradients[i] = self.alpha_c* self.eligibilities[i]* td_error # Should alpha_c be applied here? this formula says so, wi ←wi+αδei
        return gradients

