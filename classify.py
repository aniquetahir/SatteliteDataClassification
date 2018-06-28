# -*- coding: utf-8 -*-
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Dropout, Flatten, LeakyReLU
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
import keras as K
import numpy as np

from sklearn.preprocessing import OneHotEncoder
import os

images_dir = "./letters/"

# Read the labels and filenames
data = np.genfromtxt('letters.txt', dtype='|U16', delimiter=',',skip_header=1)

labels = data[:,1:2]

# perform one hot encoding for the labels
onehEncoder = OneHotEncoder()
labels = onehEncoder.fit_transform(labels)

# Get the image files
filepaths = data[:,2]

filepaths = np.array([images_dir+str(x.strip()) for x in filepaths])

def load_data(paths):
    images = []
    for path in paths:
        image = load_img(path, grayscale=True, target_size=(32,32,))
        image_array = img_to_array(image)/255
        print(image_array.shape)
        images.append(image_array)
    return np.array(images)


x = load_data(filepaths)


# Create model
my_model = Sequential()

layers = [
    Conv2D(128,(2,2),input_shape=(32,32,1), strides=2 ),
    LeakyReLU(alpha=0.02),
    Dropout(0.3),
    Conv2D(128, (3, 3),strides=2 ),
    LeakyReLU(alpha=0.02),
    Dropout(0.3),
    Conv2D(128, (3, 3),strides=2),
    LeakyReLU(alpha=0.02),
    Dropout(0.3),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(33, activation='softmax')
]

for layer in layers:
    my_model.add(layer)

print(x.shape)

my_model.compile(optimizer='adam', loss=K.losses.categorical_crossentropy, metrics=['accuracy'])
my_model.fit(x, labels, epochs=200,batch_size=28)




