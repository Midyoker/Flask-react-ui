import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import matplotlib.pyplot as plt

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the training and validation data directories
train_dir = os.path.join(script_dir, 'train')
val_dir = os.path.join(script_dir, 'val')

# Initialize the CNN model
classifier = Sequential()
classifier.add(Convolution2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Convolution2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Flatten())
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=4, activation='softmax'))

# Compile the model
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Create data generators for training and validation data
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(train_dir, target_size=(64, 64), batch_size=32, class_mode='categorical')
test_set = test_datagen.flow_from_directory(val_dir, target_size=(64, 64), batch_size=32, class_mode='categorical')

# Train the model
csv_logger = tf.keras.callbacks.CSVLogger(os.path.join(script_dir, 'metrics.csv'))

classifier.fit(training_set, steps_per_epoch=175, epochs=2,
               validation_data=test_set, validation_steps=5, callbacks=[csv_logger])

# Save the trained model
model_path = os.path.join(script_dir, 'terrain_model.h5')
classifier.save(model_path)

# Plot and save the training metrics
fig = plt.figure(0)
var = pd.read_csv(os.path.join(script_dir, 'metrics.csv'))
x = var['epoch']
e1 = var['accuracy']
e2 = var['loss']
y1 = list(e1)
y2 = list(e2)
plt.plot(x, y1, color='g', linestyle='dashed', marker='o', label="accuracy")
plt.plot(x, y2, color='r', linestyle='dashed', marker='o', label="loss")
plt.xlabel('epoch')
plt.ylabel('Accuracy and Loss')
plt.title('Graph Of Accuracy')
plt.legend()
graph_path = os.path.join(script_dir, 'graph.jpg')
fig.savefig(graph_path)

# Close the plot to prevent showing it
plt.close(fig)

# Print the path to the saved graph image
print("Graph image saved at:", graph_path)
