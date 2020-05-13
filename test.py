import numpy as np
from numpy import loadtxt
import tensorflow as tf
import h5py
import cv2
model = tf.keras.models.load_model('MNIST_model.h5')
model.summary()
#categories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def prepare(filepath):
    new_array = cv2.imread(filepath)
    new_array = new_array.reshape(-1, 28, 28, 1)
    new_array = new_array.astype('float32')
    new_array = 255 - new_array
    return new_array / 255.0


prediction = model.predict([prepare('image.png')])

#print(np.argmax(prediction[0]))
print("X=%s, Probability=%s" % (np.argmax(prediction[0]), prediction[0][np.argmax(prediction[0])]*100))
