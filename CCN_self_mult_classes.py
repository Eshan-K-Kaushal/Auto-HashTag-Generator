from tensorflow.keras import models, layers, losses, optimizers, metrics
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import cv2
import os

training = ImageDataGenerator(1/255)
validation = ImageDataGenerator(1/255)

training_dataset = training.flow_from_directory('Images/computer_vision_mult/training', target_size=(400,350), batch_size=4, class_mode='categorical')
validation_dataset = training.flow_from_directory('Images/computer_vision_mult/validation', target_size=(400,350), batch_size=4, class_mode='categorical')

model = tf.keras.models.Sequential([
    #1
    layers.Convolution2D(16, (2,2), activation='relu', input_shape=(400, 350, 3)),
    layers.MaxPooling2D(2,2),
    #2
    layers.Convolution2D(32, (2, 2), activation='relu'),
    layers.MaxPooling2D(2, 2),
    #3
    layers.Convolution2D(64, (2, 2), activation='relu'),
    layers.MaxPooling2D(2, 2),
    #4
    layers.Convolution2D(64 , (2, 2), activation='relu'),
    layers.MaxPooling2D(2, 2),
    #flatten
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(4, activation='softmax') #output is going to be according to the number of classes
])

model.compile(optimizer=RMSprop(lr = 0.001), loss = 'categorical_crossentropy', metrics=['accuracy'])
fitting = model.fit(training_dataset, epochs=5, validation_data=validation_dataset)
print(training_dataset.class_indices)

testing_dataset = 'Images/computer_vision_mult/testing'

human = ['#beauty', '#face', '#inshape', '#aesthetics', '#love', '#beauty', '#muscles', '#shred']
truck = ['#ram', '#dodge', '#ford', '#truck', '#suv', '#1500']
car = ['#car', '#srt', '#dodge', '#sports', '#race']
flower = ['#aesthetics', '#nature', '#photography']

for imgg in os.listdir(testing_dataset):
    img = image.load_img(testing_dataset + '//' + imgg, target_size=(400, 350))
    # plt.imshow(img)
    # plt.show()

    X = image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    images = np.vstack([X])

    pred = model.predict(images)
    #pred_max = [np.max(pred1) for pred1 in pred]
    pred_label = [np.argmax(pred1) for pred1 in pred]
    print(pred_label)
    if pred_label == [0]:
        print('Its a car')
        with open('Auto_HashTag_Detector.txt', 'a') as f:
            f.write('The Hashtags are:\n')
            for ht in car:
                f.write(ht)
                f.write('\t')
            f.write('\n')
        f.close()

    elif pred_label == [1]:
        print('Its a flower')
        with open('Auto_HashTag_Detector.txt', 'a') as f:
            f.write('The Hashtags are:\n')
            for ht in flower:
                f.write(ht)
                f.write('\t')
            f.write('\n')
        f.close()

    elif pred_label == [2]:
        print('Its a human')
        with open('Auto_HashTag_Detector.txt', 'a') as f:
            f.write('The Hashtags are:\n')
            for ht in human:
                f.write(ht)
                f.write('\t')
            f.write('\n')
        f.close()

    elif pred_label == [3]:
        print('Its a truck')
        with open('Auto_HashTag_Detector.txt', 'a') as f:
            f.write('The Hashtags are:\n')
            for ht in truck:
                f.write(ht)
                f.write('\t')
            f.write('\n')
        f.close()


#print('Confusion Matrix - \n', tf.math.confusion_matrix(labels=testing_dataset, predictions=pred))


