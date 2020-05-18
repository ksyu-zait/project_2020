def testing(image):
    import numpy as np
    from numpy import loadtxt
    import tensorflow as tf
    import h5py
    import cv2
    model = tf.keras.models.load_model('MNIST_model.h5')
    model.summary()

    def prepare(image):
        ptr = image.bits()
        ptr.setsize(28 * 28 * 1)
        new_array = np.frombuffer(ptr, np.uint8).reshape((28, 28, 1))
        new_array = new_array.reshape(-1, 28, 28, 1)
        new_array = new_array.astype('float32')
        new_array = 255 - new_array
        return new_array / 255.0

    prediction = model.predict([prepare(image)])
    a = [0, 0]
    a[0] = np.argmax(prediction[0])
    a[1] = prediction[0][np.argmax(prediction[0])] * 100
    return a[0], round(a[1], 2)


if __name__ == '__main__':
    print(testing('image.png'))
