from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras import optimizers
from keras import callbacks
from datetime import datetime
import Read

#####################
# Load data from csvs
top_words = 15000
(X_train, y_train), (X_test, y_test), top_words = Read.load_data()
print(type(top_words))
print(top_words)

max_words = 1000
X_train = sequence.pad_sequences(X_train, maxlen=max_words)
X_test = sequence.pad_sequences(X_test, maxlen=max_words)

#Setting up tensorboard
logdir="logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = callbacks.TensorBoard(log_dir=logdir)

# create the model
model = Sequential()
model.add(Embedding(top_words, 32, input_length=max_words))
model.add(Flatten())
model.add(Dense(500, activation='relu'))
model.add(Dense(250, activation='relu'))
model.add(Dense(250, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
optim = optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)
model.compile(loss='binary_crossentropy', optimizer=optim, metrics=['accuracy'])
print(model.summary())

# Fit the model
model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test), 
        epochs=6, 
        batch_size=64, 
        verbose=0,
        callbacks=[tensorboard_callback],)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)

print("Accuracy: %.2f%%" % (scores[1]*100))

model.save('Models/my_model.h5')